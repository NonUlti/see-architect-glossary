# Ubiquitous Language — Index

> 이 문서집은 `see-architect-system` 프로젝트에서 사용하는 건축 도메인 용어를
> 한 곳에 정리한 것이다. 회의·문서·코드에서 같은 단어가 같은 의미로 쓰이도록
> 하기 위한 공통 약속.
>


## 도메인 챕터

| 챕터 | 내용 | 표 행 / 상세 |
|---|---|---|
| [01-actors](./01-actors.md) | 사람·조직 (발주자·시공사·하청·현장소장) | 17 / 3 |
| [02-trades](./02-trades.md) | 공종 분류 체계 (가설·철콘·마감·설비) | 40 / 7 |
| [03-money](./03-money.md) | 금액 개념 (내역서·계약·실행·기성·유보 등) — 가장 큰 챕터 | 111 / 21 |
| [04-documents](./04-documents.md) | 문서 종류 (견적서·내역서·지급내역서·기성청구서) | 64 / 8 |
| [05-progress](./05-progress.md) | 진행률·실행율 등 진행도 개념 | 7 / 2 |
| [06-project](./06-project.md) | 현장·프로젝트 메타데이터 (현장명·사업기간·규모) | 6 / 2 |
| [00-conflicts](./00-conflicts.md) | 충돌 누적 (업계 vs MVP) | 7 conflicts |

**합계**: 표 행 245개 · 상세 섹션 43개 (6개 도메인 챕터 기준)

## 태그 마스터 리스트

태그는 4개 prefix 계열을 사용. **prefix 없는 태그는 사용하지 않는다.**

### `#개념:X` — 무엇에 관한 용어인가
- `#개념:돈` `#개념:사람` `#개념:공종` `#개념:문서` `#개념:진행` `#개념:일정`

### `#단계:X` — 라이프사이클 어느 시점
- `#단계:견적` `#단계:계약` `#단계:실행` `#단계:지급` `#단계:정산`

### `#문서:X` — 어떤 문서에 등장
- `#문서:견적서` `#문서:내역서` `#문서:지급내역서` `#문서:기성청구서` `#문서:거래명세서`

### `#주의:X` — 함정 표식
- `#주의:mvp재정의` — MVP가 업계와 다르게 정의함
- `#주의:mvp고유` — MVP에만 있는 개념, 업계 표준 없음
- `#주의:혼동주의` — 비슷한 다른 용어와 자주 혼동
- `#주의:용어다양` — 업계에서 여러 이름으로 부름

## 출처 약어

| 약어 | 자료 |
|---|---|
| `excel-신사동` | 2413 신사동 626-77 근생.xlsx |
| `excel-지급` | 지급내역서_샘플.xlsx |
| `excel-직접간접` | 현장_직접비_및_간접비_내역.xlsx |
| `excel-경비` | 현장소장_월_현장경비_샘플.xlsx |
| `pdf-기성` | 제 4회 하이콘 뉴캠퍼스 C동 기성청구서.pdf |
| `mvp` | see-architect-mvp 저장소 |
| `industry` | 외부 산업 표준 (구체 출처 괄호로 명시) |

**우선순위**: `excel-* > pdf-* > industry > mvp`

## 라이프사이클 단면 (cross-cut view)

용어가 어느 시점에 등장하는지 흐름으로 보고 싶을 때:

```
[견적/입찰]
  → [[04-documents#견적서-estimate--quotation]]
    [[04-documents#내역서-bill-of-quantities]]
    [[03-money#내역서금액-estimate-amount]]
    [[02-trades#공종]]
        ↓
[계약]
  → 도급계약, 변경계약 (cf. [[04-documents#내역서-bill-of-quantities]])
    [[03-money#계약금액-contract-amount]]
    [[03-money#선급금-advance-payment]]
    (cf. [[01-actors#하청업체-subcontractor]])
        ↓
[실행]
  → [[03-money#직접비-direct-cost]], [[03-money#간접비-indirect-cost]]
    [[03-money#현장경비-site-overhead]]
    [[03-money#예상실행금액-expected-amount]]
    현장소장 집행 (cf. 01-actors 컴팩트 표)
        ↓
[지급/정산]
  → [[04-documents#지급내역서-payment-statement]]
    [[04-documents#기성청구서-progress-billing-document]]
    [[03-money#기성-progress-payment]], [[03-money#유보금-retainage--retention]]
    [[03-money#차수-roundinstallment]]
        ↓
[측정·관리]
  → [[05-progress#진행률-schedule-progress]] ⚠️, [[03-money#실행율-cost-execution-ratio]] ⚠️
    [[05-progress#공정율-construction-progress-rate]]
    [[03-money#마진-margin]]
    [[04-documents#건축공정확인서]] (감리 확인용)
```

> ⚠️ 표시 용어는 업계·MVP 간 정의 충돌 있음 → [00-conflicts](./00-conflicts.md) 참조

## 사용 예시

회의에서 "기성"이라는 단어가 나왔다 → `03-money.md` 검색 또는
`grep -r "기성" docs/ubiquitous-language/` →
`#문서:기성청구서` 태그가 보이면 그 문서에서 어떻게 등장하는지
`04-documents.md`로 점프.

---

**Phase 1 + Phase 2 완료** — 2026-05-13
