# 시건축 Ubiquitous Language

시건축(See Architects) 프로젝트의 건축 도메인 용어집. DDD Ubiquitous Language 형식.

**라이브**: https://nonulti.github.io/see-architect-glossary/

[Quartz](https://quartz.jzhao.xyz) 정적 사이트, GitHub Pages 배포.

## 구조

- `content/` — 용어집 본문 (single source of truth)
  - `index.md` — 도메인 지도 + 라이프사이클
  - `00-conflicts.md` — 업계 vs MVP 충돌
  - `01-actors.md` — 사람·조직
  - `02-trades.md` — 공종 분류
  - `03-money.md` — 금액 개념 (가장 큰 챕터)
  - `04-documents.md` — 문서 종류
  - `05-progress.md` — 진행률·실행율·공정율
  - `06-project.md` — 현장·프로젝트 메타데이터
- `scripts/` — 엑셀·PDF 추출 도구 (`extract_sources.py`)
- `docs/superpowers/` — specs/plans (untracked)

## 로컬 미리보기

```bash
npm install
npx quartz build --serve
# → http://localhost:8080
```

## 배포

`main` 브랜치 push → GitHub Actions 자동 빌드 → GitHub Pages 배포.
