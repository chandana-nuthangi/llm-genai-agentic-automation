# -*- coding: utf-8 -*-

import os
import json
import base64

import streamlit as st
import anthropic 

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
# The API key is read from an environment variable / secret — NEVER hard-coded.
# Locally you set it in your terminal; on Streamlit Cloud you set it in "Secrets".
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODEL = "claude-sonnet-4-6"   # accurate + affordable. Swap to claude-haiku-4-5 for cheaper/faster.

# The 6 core fields we extract. Start small — you can add more later.
FIELDS = [
    "invoice_number",
    "invoice_date",
    "due_date",
    "vendor_name",
    "total_amount",
    "currency",
]


def pdf_to_base64(uploaded_file) -> str:
    """Turn the uploaded PDF into base64 text so we can send it to the API."""
    return base64.standard_b64encode(uploaded_file.read()).decode("utf-8")


def ask_claude(pdf_b64: str, prompt: str) -> str:
    """Send the PDF + a text instruction to Claude and return the text answer."""
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_b64,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )
    # The response can have several blocks; join the text ones together.
    return "".join(block.text for block in message.content if block.type == "text")


def extract_fields(pdf_b64: str) -> dict:
    """Ask Claude to pull the invoice fields and return them as a Python dict."""
    prompt = (
        "You are an invoice data extractor. Read the attached invoice and return ONLY "
        "a JSON object (no explanation, no markdown) with exactly these keys: "
        + ", ".join(FIELDS)
        + ". If a value is missing, use null. total_amount must be a number only "
        "(no currency symbol)."
    )
    raw = ask_claude(pdf_b64, prompt)
    # Models sometimes wrap JSON in ```json ... ``` fences — strip them before parsing.
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


# ---------------------------------------------------------------------------
# User interface (Streamlit)
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Invoice Extractor", page_icon="📄")

st.title("📄 Invoice Extractor")
st.caption("Upload an invoice PDF → get clean structured data + ask questions about it.")

uploaded = st.file_uploader("Upload an invoice (PDF)", type="pdf")

if uploaded is not None:
    pdf_b64 = pdf_to_base64(uploaded)

    # --- Extraction ---
    if st.button("Extract data"):
        with st.spinner("Reading the invoice..."):
            try:
                data = extract_fields(pdf_b64)
                st.session_state["data"] = data
            except json.JSONDecodeError:
                st.error("Could not read structured data from this PDF. Try another file.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    # Show the extracted table if we have it
    if "data" in st.session_state:
        st.subheader("Extracted fields")
        data = st.session_state["data"]
        # Show as a simple two-column table: Field | Value
        st.table({"Field": list(data.keys()), "Value": [str(v) for v in data.values()]})

        # Let the user download the result as JSON (a real deliverable for a client)
        st.download_button(
            "Download as JSON",
            data=json.dumps(data, indent=2),
            file_name="invoice_data.json",
            mime="application/json",
        )

    # --- Q&A ---
    st.subheader("Ask a question about this invoice")
    question = st.text_input("e.g. 'What is being charged for?' or 'When is payment due?'")
    if question:
        with st.spinner("Thinking..."):
            try:
                answer = ask_claude(pdf_b64, question)
                st.write(answer)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
