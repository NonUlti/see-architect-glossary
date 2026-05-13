# 시건축 Ubiquitous Language

`see-architect-system` 프로젝트의 건축 도메인 용어집. DDD Ubiquitous Language 형식.

[Quartz](https://quartz.jzhao.xyz) 정적 사이트, GitHub Pages 배포.

## 콘텐츠

- `content/index.md` — 도메인 지도 + 라이프사이클
- `content/00-conflicts.md` — 업계 vs MVP 충돌
- `content/01-actors.md` — 사람·조직
- `content/02-trades.md` — 공종 분류
- `content/03-money.md` — 금액 개념 (가장 큰 챕터)
- `content/04-documents.md` — 문서 종류
- `content/05-progress.md` — 진행률·실행율·공정율
- `content/06-project.md` — 현장·프로젝트 메타데이터

원본 마크다운: [NonUlti/see-architect-system](https://github.com/NonUlti/see-architect-system/tree/master/docs/ubiquitous-language)

## 로컬 미리보기

```bash
npm install
npx quartz build --serve
# → http://localhost:8080
```

## 배포

`main` 브랜치 push → GitHub Actions 자동 빌드 → GitHub Pages 배포.

## 콘텐츠 갱신

원본(`see-architect-system/docs/ubiquitous-language/`) 수정 → 이 repo `content/`에 복사 → push.
