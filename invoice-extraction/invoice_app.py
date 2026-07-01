import os
import json

import streamlit as st
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"

FIELDS = [
    "invoice_number",
    "invoice_date",
    "due_date",
    "vendor_name",
    "total_amount",
    "currency",
]


def ask_gemini(pdf_bytes: bytes, prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
            prompt,
        ],
    )
    return response.text


def extract_fields(pdf_bytes: bytes) -> dict:
    prompt = (
        "You are an invoice data extractor. Read the attached invoice and return ONLY "
        "a JSON object (no explanation, no markdown) with exactly these keys: "
        + ", ".join(FIELDS)
        + ". If a value is missing, use null. total_amount must be a number only "
        "(no currency symbol)."
    )
    raw = ask_gemini(pdf_bytes, prompt)
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


st.set_page_config(page_title="Invoice Extractor", page_icon="📄")
st.title("📄 Invoice Extractor")
st.caption("Upload an invoice PDF → get clean structured data + ask questions about it.")

uploaded = st.file_uploader("Upload an invoice (PDF)", type="pdf")

if uploaded is not None:
    pdf_bytes = uploaded.getvalue()

    if st.button("Extract data"):
        with st.spinner("Reading the invoice..."):
            try:
                data = extract_fields(pdf_bytes)
                st.session_state["data"] = data
            except json.JSONDecodeError:
                st.error("Could not read structured data from this PDF. Try another file.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    if "data" in st.session_state:
        st.subheader("Extracted fields")
        data = st.session_state["data"]
        st.table({"Field": list(data.keys()), "Value": [str(v) for v in data.values()]})
        st.download_button(
            "Download as JSON",
            data=json.dumps(data, indent=2),
            file_name="invoice_data.json",
            mime="application/json",
        )

    st.subheader("Ask a question about this invoice")
    question = st.text_input("e.g. 'What is being charged for?' or 'When is payment due?'")
    if question:
        with st.spinner("Thinking..."):
            try:
                answer = ask_gemini(pdf_bytes, question)
                st.write(answer)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
