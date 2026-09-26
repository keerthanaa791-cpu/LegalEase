from backend.services.formatters import sanitize_text, format_docx, format_pdf, format_html_preview

def test_sanitize_text():
    assert sanitize_text("Hello — “world”") == 'Hello - "world"'

def test_docx_generation():
    data = format_docx("1. Purpose\nThis is a draft.", "NDA", terms=["Confidentiality"])
    assert data.startswith(b"PK")

def test_pdf_generation():
    data = format_pdf("1. Purpose\nThis is a draft.", "NDA")
    assert data.startswith(b"%PDF")

def test_html_escapes_content():
    html = format_html_preview("<script>alert(1)</script>")
    assert "&lt;script&gt;" in html
