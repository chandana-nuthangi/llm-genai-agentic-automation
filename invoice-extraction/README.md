# 📄 Invoice Extractor

**Turn messy invoice PDFs into clean, structured data — in one click.**

Upload an invoice, and this tool reads it with AI, pulls out the key fields (number, date, vendor, total…), shows them as a table, and lets you ask questions about the document in plain language. Built to solve a real, boring, expensive problem: manual data entry from invoices.

🔗 **Live demo:** _add your Streamlit link here once deployed_
👩‍💻 Part of my **from-floor-to-data** portfolio — warehouse operations experience meets data & AI.

---

## 🎯 The problem it solves

Small businesses drown in PDFs — invoices, delivery notes, receipts — and someone has to type all that into a spreadsheet by hand. It's slow, error-prone, and nobody enjoys it. This tool does it automatically: drop in a PDF, get structured data out, ready for Excel or a database.

## ✨ Features

- **Reads PDFs directly** — no manual copy-paste, handles German and English invoices.
- **Structured extraction** — returns clean fields as a table you can download as JSON.
- **Ask-anything Q&A** — query the invoice in natural language ("When is payment due?").
- **Deployable & free** — runs on a free AI tier, hostable on a public link.

## 🖼️ Screenshots

| Upload & extract | Structured output | Ask a question |
|---|---|---|
| ![Home](screenshots/01-home.png) | ![Extracted table](screenshots/02-extracted.png) | ![Q&A](screenshots/03-qa.png) |

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
streamlit run app.py
```

## 👩‍💻 About

I'm building data & AI tools that solve practical operational problems — bringing together 2+ years of hands-on warehouse and logistics experience (Amazon, Kuehne+Nagel) with a data science background. **From the floor to the data.**

---

_Built with Python, Streamlit & Gemini._
