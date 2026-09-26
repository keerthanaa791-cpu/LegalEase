from google import genai
from google.genai import types

from backend.config import Settings

SYSTEM_INSTRUCTION = """You are LegalEase, an AI assistant for drafting legal-document templates.
Produce a professional, clearly structured draft based only on the user-provided facts.
Do not invent names, dates, amounts, addresses, laws, citations, or obligations that were not supplied.
If a legally important fact is missing, use a clearly marked placeholder such as [TO BE COMPLETED].
This is a drafting aid, not legal advice. Do not claim that a document is legally valid in a particular jurisdiction.
Use plain text headings, numbered sections, and readable clauses. Do not use Markdown tables or code fences.
Return only the document body, without commentary about the generation process.
"""

class GeminiDocumentGenerator:
    def __init__(self, settings: Settings):
        self.settings = settings
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured")
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def generate_document(self, document_type: str, parties: str, terms: str, effective_date: str) -> str:
        clauses = [item.strip() for item in terms.split(";") if item.strip()]
        terms_block = "\n".join(f"- {item}" for item in clauses)
        prompt = f"""Draft a {document_type} using these facts.

PARTIES:
{parties}

EFFECTIVE DATE:
{effective_date}

USER-PROVIDED TERMS:
{terms_block}

Required structure:
1. Title
2. Parties and Effective Date
3. Purpose / Recitals when appropriate
4. Definitions when appropriate
5. Core obligations and rights
6. Term and termination when appropriate
7. Confidentiality / intellectual property / payment / dispute provisions only when relevant to the supplied facts
8. General provisions when appropriate
9. Signature blocks for the parties

Preserve the supplied facts exactly. Clearly mark missing material information instead of guessing.
"""
        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
                max_output_tokens=12000,
            ),
        )
        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response")
        return text
