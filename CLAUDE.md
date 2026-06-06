# Claude Code 운영 규약 — see-architect-glossary

이 repo는 시건축(See Architects) 도메인의 **단일 LLM Wiki**다. 사람용(Quartz 사이트)과 LLM용 참조가 같은 코퍼스(`content/`)를 공유한다.

설계 근거: `docs/superpowers/specs/2026-05-21-llm-wiki-design.md` (Karpathy *LLM Wiki* 모델 적용)

## 구조 한눈에

```
content/
├── index.md, 00-conflicts.md, 01~06-*.md   ← 백본 (공식·고정)
└── notes/                                  ← LLM 누적 (자유 형식, 비공개)
```

- **백본 8 파일**: 확정된 도메인 사실. 사람 검토 후 갱신.
- **notes/**: dashboard 작업 중 발견된 결정·논의·Q&A. `quartz.config.ts` `ignorePatterns`로 공개 사이트 비노출.

Raw source (immutable):
- 엑셀 4 + PDF 1: `~/Desktop/project/see-architect/files/`
- 참조 MVP 코드: `~/Desktop/git/see-architect-mvp/`

## 작업 흐름

### 1. Query — 작업 시작 시 wiki 참조
- 도메인 용어·규칙을 다룰 때 항상 `content/` 백본을 먼저 grep·Read
- 관련 notes/도 함께 확인 (`grep -r "<용어>" content/notes/`)
- wiki-link `[[...]]`를 따라 확장 읽기

### 2. Ingest — 새 사실·결정 발견 시
1. 새 도메인 사실, 결정, 사용자와의 Q&A 답변, 동의어를 발견하면
2. 사용자에게 **"이 사실을 notes/에 추가할까요?"** 제안
3. 승인 후 `content/notes/YYYY-MM-DD-<slug>.md` 작성
4. 무단 작성 금지

### 3. Promote — notes → 백본
1. notes 항목이 충분히 정착·검증되었다고 판단하면
2. **"백본 `<file>` 의 X 행으로 promote 제안"** 사용자에게 제시
3. 승인 후 백본 표/상세 갱신
4. 원 notes 페이지는 `status: promoted` + `last_updated` 갱신 (삭제하지 않음)

### 4. Lint — 주기적 건강 체크
- `python scripts/lint_wiki.py` 실행 (사용자 요청 시 또는 큰 변경 후)
- 리포트 항목: broken wiki-link / 고아 페이지 / frontmatter 오류 / 미결정 충돌 status / stale notes (30일+)
- 리포트를 사용자에게 요약 보고

### 5. 커밋·푸시
- **사용자가 명시적으로 요청한 경우에만** 수행 (자동 금지)
- 커밋 메시지는 한국어 conventional commits prefix 사용 (`feat:`, `fix:`, `chore:`, `docs:` 등)
- 잘게 나눠서 커밋 (기능 단위)
- Co-Authored-By 태그 포함, HEREDOC 방식
- 푸시는 별도 명시 요청 시

## Frontmatter 규약

모든 페이지 공통:
```yaml
---
title: <필수>
status: stable | draft | promoted | superseded
last_updated: YYYY-MM-DD
---
```

선택 키: `entity`, `related: [[...]]`, `tags: [#...]`.
Quartz는 모르는 키를 무시하므로 호환에 부담 없음.

## Quartz 빌드 검증

```bash
npx quartz build              # 출력 확인
npx quartz build --serve      # 로컬 미리보기 (http://localhost:8080)
```

빌드 후 `notes/` 가 출력에서 제외되는지 확인 필수.

## 절대 하지 말 것

- 백본 8 파일을 사용자 승인 없이 수정
- notes/ 페이지를 사용자 승인 없이 작성
- 커밋·푸시·배포를 사용자 요청 없이 실행
- raw source(엑셀·PDF) 수정 (immutable)
- `docs/superpowers/` 하위를 git에 커밋 (의도적 untracked, `.gitignore` 보호)
