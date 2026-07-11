# 💰 AI-Powered Expense Tracker

A smart personal finance dashboard that combines **React**, **Python Flask**, **LangChain**, and **LLMs** to not just track your expenses — but actually understand and explain them in plain English.

---

## ✨ Features

### 📂 File-Based Expense Ingestion
Upload your CSV or Excel expense files and the app automatically parses, categorizes, and loads your transactions — no manual entry required.

### 📊 Interactive Dashboard
Visual charts and breakdowns of your spending across:
- **Categories** — food, transport, utilities, entertainment, and more
- **Time periods** — daily, monthly, and custom ranges
- **50/30/20 budget rule analysis** — see at a glance how your spending maps to needs, wants, and savings

### ➕ Add / Edit / Delete Expenses
Full CRUD support for managing your transactions. Manually add expenses, correct imported entries, or remove anything that doesn't belong.

### 🔍 Category Filters
Filter your expense view by category to drill into specific spending areas and track where your money is actually going.

### 🤖 AI-Powered Financial Summary (LLM)
The highlight of the app — an LLM analyses your uploaded financial data and generates a **human-readable summary** of your spending habits, including:
- Key insights about your highest spend categories
- Budget health assessment
- Personalised observations about your financial patterns

All powered by **LangChain** with a RAG pipeline that retrieves relevant transaction context before generating the summary.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, CSS |
| Backend | Python, Flask |
| AI / LLM | LangChain, LLM API (RAG pipeline) |
| File Processing | Pandas (CSV / Excel parsing) |
| Data Visualization | Chart.js / Recharts |

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v16+)
- Python (v3.9+)
- pip

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/ShubhamDasgupta2003/Expense-Tracker.git
cd Expense-Tracker
```

#### 2. Set up the backend
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:
```env
LLM_API_KEY=your_api_key_here
```

Start the Flask server:
```bash
python app.py
```

#### 3. Set up the frontend
```bash
cd ../Expense-Tracker
npm install
npm start
```

The app will be available at `http://localhost:3000`

---

## 📖 How to Use

1. **Upload your expense file** — CSV or Excel format with your transactions.
2. **Explore the dashboard** — charts and category breakdowns load automatically.
3. **Filter & drill down** — use category filters to focus on specific spending areas.
4. **Add or edit transactions** — manually manage any entries as needed.
5. **Generate AI Summary** — click the summary button to get a plain-English analysis of your finances powered by an LLM.

---

## 📁 Project Structure

```
Expense-Tracker/
├── Expense-Tracker/         # React frontend
│   ├── src/
│   │   ├── components/      # Dashboard, charts, filters, expense list
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── backend/                 # Flask backend
│   ├── app.py               # API routes & file processing
│   ├── langchain_pipeline.py # RAG pipeline & LLM summarization
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

---

## 🧠 How the AI Summary Works

1. Your uploaded expense file is parsed and chunked into transaction segments.
2. **LangChain** builds a retrieval pipeline (RAG) over the transaction data.
3. Relevant financial context is retrieved and passed to the LLM as part of the prompt.
4. The LLM generates a natural language summary — not just numbers, but actual insights about your spending behaviour.

---

## 🎯 Why This Is Different

Most expense trackers show you charts. This one tells you what those charts *mean* — in plain English, personalised to your actual data.

---

> Built by [Shubham Dasgupta](https://github.com/ShubhamDasgupta2003)
