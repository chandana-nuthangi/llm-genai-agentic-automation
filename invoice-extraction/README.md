# 📄 Invoice Extractor

**Turn messy invoice PDFs into clean, structured data — in one click.**

Upload an invoice, and this tool reads it with AI, pulls out the key fields (number, date, vendor, total…), shows them as a table, and lets you ask questions about the document in plain language. Built to solve a real, boring, expensive problem: manual data entry from invoices.

🔗 **Live demo:** _add your Streamlit link here once deployed_
📦 Part of [**llm-genai-agentic-automation**](https://github.com/chandana-nuthangi/llm-genai-agentic-automation) — a growing collection of AI projects built to solve real-world problems.

---

## 🎯 The problem it solves

Small businesses drown in PDFs — invoices, delivery notes, receipts — and someone has to type all that into a spreadsheet by hand. It's slow, error-prone, and nobody enjoys it. This tool does it automatically: drop in a PDF, get structured data out, ready for Excel or a database.

## ✨ Features

- **Reads PDFs directly** — no manual copy-paste, handles German and English invoices.
- **Structured extraction** — returns clean fields as a table you can download as JSON.
- **Ask-anything Q&A** — query the invoice in natural language ("When is payment due?").
- **Deployable & free** — runs on a free AI tier, hostable on a public link.

## 🖼️ Screenshots

| Upload & extract | Extracted results |
|---|---|
| ![Home](images/homepage.png) | ![Extracted table](images/results.png) |

## 🛠️ Tech stack

- **Python** — core logic
- **Streamlit** — the web interface
- **Google Gemini API** — reads the PDF and returns structured data
- **GitHub + Streamlit Community Cloud** — version control & deployment

## ⚙️ How it works

1. User uploads an invoice PDF.
2. The PDF is sent directly to the Gemini model with a prompt asking for specific fields as JSON.
3. The JSON response is parsed and shown as a table (and offered as a download).
4. A separate Q&A box sends the same PDF plus the user's question back to the model.

No separate PDF-parsing library is needed — the model reads the document itself, which keeps the code small and robust.

## 🧾 Try it out

A sample invoice is included at `samples/sample_invoice.pdf` — upload it after running the app to see the extractor in action.

## 🚀 Run it locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your free Gemini API key (get one at aistudio.google.com)
#    PowerShell:
$env:GEMINI_API_KEY = "your-key-here"
#    macOS/Linux:
export GEMINI_API_KEY="your-key-here"

# 3. Run
streamlit run invoice_app.py
```

## 👩‍💻 About

This project is part of a larger repo where I'm building practical AI and GenAI applications — each subfolder tackles a different real-world problem using LLMs and agentic workflows. More projects will be added over time.

---

_Built with Python, Streamlit & Gemini._
