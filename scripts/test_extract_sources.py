"""소스 추출 통합 테스트. 실제 파일을 읽어 추출 결과를 검증."""
from pathlib import Path

import pytest

from extract_sources import extract_excel, extract_pdf

SRC = Path("/Users/apple/Desktop/project/see-architect/files")


def test_extract_excel_returns_sheets():
    result = extract_excel(SRC / "현장_직접비_및_간접비_내역.xlsx")
    assert "sheets" in result
    assert len(result["sheets"]) >= 1


def test_extract_excel_includes_sheet_metadata():
    result = extract_excel(SRC / "현장_직접비_및_간접비_내역.xlsx")
    sheet = result["sheets"][0]
    assert "name" in sheet
    assert "headers" in sheet
    assert "text_cells" in sheet  # 모든 문자열 셀 (중복 제거)
    assert isinstance(sheet["text_cells"], list)


def test_extract_pdf_returns_pages():
    pdf_path = SRC / "01. 제 4회 하이콘 뉴캠퍼스 C동 리모델링공사 기성청구서(합본).pdf"
    result = extract_pdf(pdf_path)
    assert "pages" in result
    assert len(result["pages"]) >= 1


def test_extract_pdf_page_has_text():
    pdf_path = SRC / "01. 제 4회 하이콘 뉴캠퍼스 C동 리모델링공사 기성청구서(합본).pdf"
    result = extract_pdf(pdf_path)
    first_page = result["pages"][0]
    assert "page_number" in first_page
    assert "text" in first_page
    assert isinstance(first_page["text"], str)


from extract_sources import extract_mvp


def test_extract_mvp_returns_sources():
    result = extract_mvp()
    assert "claude_md" in result
    assert "types_ts" in result
    assert "domain_files" in result
    assert len(result["claude_md"]) > 100  # CLAUDE.md는 본문이 있음


def test_extract_mvp_claude_md_contains_domain_terms():
    result = extract_mvp()
    # 알려진 핵심 용어가 CLAUDE.md에 포함되어 있는지
    assert "내역서금액" in result["claude_md"]
    assert "계약금액" in result["claude_md"]
