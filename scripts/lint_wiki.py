"""LLM Wiki 건강 체크 — Karpathy lint 단계 구현.

점검 항목:
1. broken wiki-link    — [[target]] target 파일 부재
2. orphan              — 어디서도 link 안 되는 페이지 (index 제외)
3. frontmatter         — 필수 키 누락·형식 오류
4. unresolved conflict — 00-conflicts.md 의 "(미정)" 항목 수 보고
5. stale notes         — notes/ 중 last_updated 30일+ 지난 draft

사용:
    python scripts/lint_wiki.py
    python scripts/lint_wiki.py --stale-days 14

종료 코드:
    0 = 오류 없음 (경고만)
    1 = 오류 있음 (broken link, frontmatter 오류)
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT = REPO_ROOT / "content"

REQUIRED_KEYS = {"title", "status", "last_updated"}
ALLOWED_STATUS = {"stable", "draft", "promoted", "superseded"}

WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)
CONFLICT_PENDING_RE = re.compile(r"\(미정[^)]*\)")
FENCED_CODE_RE = re.compile(r"```.*?```|`[^`]*`", re.DOTALL)


def strip_code(text: str) -> str:
    """코드블록·인라인 코드 제거 (lint 시 예시 wiki-link false positive 방지)."""
    return FENCED_CODE_RE.sub("", text)


def parse_frontmatter(text: str) -> dict | None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def iter_pages() -> list[Path]:
    return [p for p in CONTENT.rglob("*.md") if p.is_file()]


def page_slug(p: Path) -> str:
    """`content/01-actors.md` -> `01-actors`, `content/notes/x.md` -> `notes/x`."""
    return p.relative_to(CONTENT).with_suffix("").as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="LLM Wiki lint")
    parser.add_argument("--stale-days", type=int, default=30)
    args = parser.parse_args()

    pages = iter_pages()
    slugs = {page_slug(p) for p in pages}
    # 백본은 폴더 없는 slug, notes는 notes/ prefix. 둘 다 매치되도록 짧은 형태도 등록.
    short_slugs = {Path(s).name for s in slugs}

    errors: list[str] = []
    warnings: list[str] = []

    referenced: set[str] = set()
    pending_conflicts = 0
    stale_notes: list[tuple[str, int]] = []
    today = date.today()

    for p in pages:
        rel = page_slug(p)
        text = p.read_text(encoding="utf-8")

        # 1. frontmatter
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"[frontmatter] {rel}: frontmatter 블록 없음")
        else:
            missing = REQUIRED_KEYS - fm.keys()
            if missing:
                errors.append(f"[frontmatter] {rel}: 필수 키 누락 {missing}")
            if fm.get("status") and fm["status"] not in ALLOWED_STATUS:
                errors.append(f"[frontmatter] {rel}: status='{fm['status']}' 허용값 아님 ({ALLOWED_STATUS})")
            last_updated = fm.get("last_updated", "")
            try:
                lu = datetime.strptime(last_updated, "%Y-%m-%d").date() if last_updated else None
            except ValueError:
                errors.append(f"[frontmatter] {rel}: last_updated='{last_updated}' 형식 오류 (YYYY-MM-DD)")
                lu = None

            # 5. stale notes
            if rel.startswith("notes/") and rel != "notes/README" and fm.get("status") == "draft" and lu:
                age = (today - lu).days
                if age >= args.stale_days:
                    stale_notes.append((rel, age))

        # 2. wiki-link 수집·검증 (코드블록 안은 무시)
        body = strip_code(text)
        for m in WIKI_LINK_RE.finditer(body):
            target = m.group(1).strip()
            # 디렉토리 없는 형태도 허용 (예: [[01-actors]])
            target_slug = target.lstrip("/")
            if target_slug in slugs or target_slug in short_slugs or f"notes/{target_slug}" in slugs:
                # 정확히 어느 슬러그로 매핑되는지 referenced에 기록
                if target_slug in slugs:
                    referenced.add(target_slug)
                elif target_slug in short_slugs:
                    # short match — 첫 매치를 사용
                    for s in slugs:
                        if Path(s).name == target_slug:
                            referenced.add(s)
                            break
            else:
                errors.append(f"[broken-link] {rel}: [[{target}]] → 대상 페이지 없음")

        # 4. 미결정 충돌 (00-conflicts.md만 해당)
        if rel == "00-conflicts":
            pending_conflicts = len(CONFLICT_PENDING_RE.findall(text))

    # 3. 고아 페이지 (index, README, notes/README 제외)
    EXEMPT = {"index", "notes/README"}
    for s in sorted(slugs):
        if s in EXEMPT:
            continue
        if s not in referenced:
            warnings.append(f"[orphan] {s}: 어디서도 link되지 않음")

    # 리포트 출력
    print(f"📊 LLM Wiki Lint Report ({today})")
    print(f"  검사 페이지: {len(pages)}")
    print()

    if errors:
        print(f"❌ 오류 {len(errors)}건")
        for e in errors:
            print(f"  {e}")
        print()
    else:
        print("✅ 오류 없음")
        print()

    if warnings:
        print(f"⚠️  경고 {len(warnings)}건")
        for w in warnings:
            print(f"  {w}")
        print()

    print(f"🔖 미결정 충돌 (00-conflicts.md '(미정)'): {pending_conflicts}건")
    print()

    if stale_notes:
        print(f"⏳ Stale notes (draft, {args.stale_days}일+): {len(stale_notes)}건")
        for slug, age in sorted(stale_notes, key=lambda x: -x[1]):
            print(f"  {slug}  ({age}일 경과)")
    else:
        print(f"⏳ Stale notes (draft, {args.stale_days}일+): 0건")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
