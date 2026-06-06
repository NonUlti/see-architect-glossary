---
title: notes/ 사용 규약
status: stable
last_updated: 2026-05-21
---

# notes/

dashboard 작업 중 LLM·사용자가 발견·논의한 도메인 사실을 누적하는 임시 보관소.
백본(`content/00~06-*.md`)이 "확정된 사실"이라면 notes/는 **"백본에 넣기엔 아직 이른 모든 것"**.

설계 근거: `docs/superpowers/specs/2026-05-21-llm-wiki-design.md`

## 파일 규칙

- 경로: `content/notes/YYYY-MM-DD-<slug>.md`
- 1 페이지 = 1 주제·결정·질문
- 자유 형식이되 아래 frontmatter는 필수

```yaml
---
title: <한 줄 요약>
entity: <핵심 엔티티명, 없으면 ~>
status: draft | promoted | superseded
last_updated: YYYY-MM-DD
related:
  - "[[01-actors]]"           # 백본 wiki-link
  - "[[notes/2026-05-20-...]]"
---
```

## 5가지 흐름

| 흐름 | promote? | 예 |
|---|---|---|
| A. 결정 → promote 후보 | ✅ | 미결정 충돌을 합의로 좁힘 |
| B. 결정 보류·질문 | 결정 후 ✅ | 사용자 확인 대기 |
| C. 동의어·약어 신규 발견 | ✅ | 기존 백본 표 행 보강 |
| D. Q&A 답변 보존 | 일부 ✅ | LLM이 답변한 도메인 질문 |
| E. 구현 메모 | ❌ archive | dashboard 작업 노트 |

## 트리거

- **추가**: Claude가 제안 → 사용자 승인 후 작성. 무단 작성 금지.
- **promote**: Claude가 "백본 X 파일 Y행으로 promote 제안" → 승인 후 표 갱신, 원 notes는 `status: promoted` 로 변경.
- **archive(stale)**: `scripts/lint_wiki.py` 가 30일 이상 미수정 draft를 리포트. 사람이 보고 promote 또는 archive 결정.
- **커밋·푸시**: 사용자 명시 요청 시만.

## 공개 범위

notes/는 비공개. `quartz.config.ts` `ignorePatterns`에 `notes/**` 포함되어 GitHub Pages에는 노출되지 않음. 로컬 파일로만 Claude·사용자가 본다.
