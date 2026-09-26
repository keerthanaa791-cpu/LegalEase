# LegalEase

AI-powered legal document drafting application based on the supplied LegalEase specification.

## Architecture

- **Frontend:** Streamlit (`frontend/app.py`)
- **Backend:** FastAPI (`backend/main.py`, `backend/routes.py`)
- **AI:** Google Gemini via the current `google-genai` SDK (`backend/ai_core/gemini_generator.py`)
- **Exports:** TXT, DOCX, PDF (`backend/services/formatters.py`)
- **Tests:** pytest (`backend/tests/`)

The supplied specification describes Streamlit + FastAPI + Gemini and requires editable previews and TXT/DOCX/PDF export. This implementation follows that architecture. The original document names Gemini 1.5 Pro, but model availability changes over time; the app therefore reads `GEMINI_MODEL` from `.env` and defaults to a currently documented model.

## VS Code setup

### 1. Requirements

- Python 3.11 recommended
- VS Code
- A Gemini API key from Google AI Studio

### 2. Open project

Open this folder in VS Code:

```text
LegalEase_project/
```

### 3. Create virtual environment

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Gemini

Copy `.env.example` to `.env` and set:

```env
GEMINI_API_KEY=your_real_key
GEMINI_MODEL=gemini-3.8-flash
```

Do not commit `.env` to source control.

### 6. Start FastAPI

From the project root:

```bash
uvicorn backend.main:app --reload --port 8000
```

Check:

- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/docs

### 7. Start Streamlit

Open a second terminal, activate `.venv`, then:

```bash
streamlit run frontend/app.py
```

Open http://localhost:8501.

### 8. Test without spending Gemini credits

The formatter tests and API route tests mock the AI call:

```bash
pytest -q
```

### 9. End-to-end test

1. Start FastAPI.
2. Start Streamlit.
3. Select `NDA (Non-Disclosure Agreement)`.
4. Enter two parties.
5. Enter semicolon-separated terms.
6. Select an effective date.
7. Click **Generate Document**.
8. Edit the generated content.
9. Download TXT, DOCX, and PDF.
10. Open the generated files and verify formatting.

## API example

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "document_type":"NDA",
    "parties":"Jane Doe (Disclosing Party), TechNova Inc. (Receiving Party)",
    "terms":"Confidentiality;Return confidential material on termination;15 day termination notice",
    "effective_date":"2026-09-25",
    "branding_name":"TechNova Inc."
  }'
```

## Project tree

```text
LegalEase_project/
├── backend/
│   ├── ai_core/
│   │   └── gemini_generator.py
│   ├── services/
│   │   └── formatters.py
│   ├── tests/
│   │   ├── test_formatters.py
│   │   └── test_routes.py
│   ├── config.py
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
├── frontend/
│   └── app.py
├── assets/
│   └── logo.png
├── .streamlit/config.toml
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

## Optional branding

Replace `assets/logo.png` with your own PNG logo. DOCX/PDF export will embed it automatically when present.

## Production notes

- Put the API behind HTTPS and an authenticated gateway before exposing it publicly.
- Do not log document contents or API keys.
- Add authentication, rate limiting, persistent storage, audit logging, and jurisdiction-specific legal review before production use.
- Generated documents are drafts and should be reviewed by an appropriately qualified legal professional.
