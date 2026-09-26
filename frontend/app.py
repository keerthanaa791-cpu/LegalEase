import html
import os
import sys
from datetime import date
from pathlib import Path

import requests
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.services.formatters import format_docx, format_pdf, format_html_preview

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")
API_URL = os.getenv("LEGAL_EASE_API_URL", "http://localhost:8000").rstrip("/")

st.markdown("""
<style>
.legal-preview { background:#151922; color:#f4f5f7; padding:2rem; border-radius:14px; max-height:650px; overflow:auto; line-height:1.7; font-family:Georgia,serif; }
.legal-preview h3 { color:#fff; margin-top:1.2rem; }
.small-note { color:#777; font-size:.9rem; }
</style>
""", unsafe_allow_html=True)

st.title("⚖️ LegalEase")
st.caption("AI-powered legal document drafting and export")
st.info("LegalEase creates drafts and templates, not legal advice. Review important documents with a qualified lawyer before signing or relying on them.")

with st.sidebar:
    st.header("Document details")
    document_type = st.selectbox("Document type", ["Employment Contract", "Lease Agreement", "NDA (Non-Disclosure Agreement)", "Employment Offer Letter", "Freelance Work Contract", "Service Agreement", "General Agreement", "Custom"])
    if document_type == "Custom":
        document_type = st.text_input("Custom document type", placeholder="e.g. Consulting Agreement")
    parties = st.text_area("Parties involved", placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)", height=110)
    terms = st.text_area("Terms & conditions", placeholder="Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice", height=180)
    effective_date = st.date_input("Effective date", value=date.today())
    branding_name = st.text_input("Brand / company name", value="LegalEase")
    generate = st.button("Generate Document", type="primary", use_container_width=True)

if "content" not in st.session_state:
    st.session_state.content = ""
if "doc_type" not in st.session_state:
    st.session_state.doc_type = document_type
if "terms" not in st.session_state:
    st.session_state.terms = []

if generate:
    if not all([document_type.strip(), parties.strip(), terms.strip()]):
        st.error("Please complete document type, parties, and terms.")
    else:
        payload = {"document_type": document_type, "parties": parties, "terms": terms, "effective_date": effective_date.isoformat(), "branding_name": branding_name}
        with st.spinner("Generating your draft..."):
            try:
                response = requests.post(f"{API_URL}/generate", json=payload, timeout=180)
                if response.ok:
                    data = response.json(); st.session_state.content = data["content"]; st.session_state.doc_type = data["document_type"]; st.session_state.terms = data["terms"]
                    st.success("Document generated.")
                else:
                    detail = response.json().get("detail", response.text)
                    st.error(f"Backend error: {detail}")
            except requests.RequestException as exc:
                st.error(f"Could not reach FastAPI at {API_URL}. Start the backend first. Details: {exc}")

if st.session_state.content:
    st.subheader("Preview")
    st.markdown(format_html_preview(st.session_state.content), unsafe_allow_html=True)
    st.subheader("Edit document")
    st.session_state.content = st.text_area("Generated text", value=st.session_state.content, height=520, label_visibility="collapsed")

    col1, col2, col3 = st.columns(3)
    txt = st.session_state.content.encode("utf-8")
    docx = format_docx(st.session_state.content, st.session_state.doc_type, branding_name, st.session_state.terms)
    pdf = format_pdf(st.session_state.content, st.session_state.doc_type, branding_name)
    safe_name = "legalease_document"
    with col1: st.download_button("Download TXT", txt, f"{safe_name}.txt", "text/plain", use_container_width=True)
    with col2: st.download_button("Download DOCX", docx, f"{safe_name}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with col3: st.download_button("Download PDF", pdf, f"{safe_name}.pdf", "application/pdf", use_container_width=True)
else:
    st.subheader("How it works")
    st.write("1. Choose a document type. 2. Enter the parties, terms, and effective date. 3. Generate, edit, preview, and export the draft.")
