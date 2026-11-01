# AI Doubt Solver – Intelligent Question Answering Chatbot

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-green.svg)](https://flask.palletsprojects.com/)
[![AI Model](https://img.shields.io/badge/AI%20Engine-Google%20Gemini-orange.svg)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/Project-College%20AI%20Mini--Capstone-purple.svg)]()

An intelligent, multi-domain academic tutor and question-answering conversational chatbot designed to help students resolve doubts instantly. Powered by Google Gemini's high-speed Large Language Model (`gemini-3.1-flash-lite`) and a clean, responsive Flask web application.

---

## 📌 Project Overview

Students often face difficulties understanding complex textbook concepts, getting stuck on mathematical derivations, debugging code, or translating between English and their regional language. **AI Doubt Solver** acts as a 24/7 personalized academic tutor that provides step-by-step explanations, clean code examples, grammar feedback, and multilingual assistance in real time (within 1–3 seconds).

---

## 🌟 Key Features

1. **General Knowledge & Science Doubts:** Delivers clear, intuitive explanations for science, history, and general knowledge concepts using easy-to-understand analogies.
2. **Step-by-Step Mathematics Solver:** Breaks down equations and word problems into structured, numbered steps with reasoning.
3. **Programming & Code Tutor:** Generates properly commented code snippets, syntax explanations, and algorithmic logic.
4. **Grammar & Spelling Correction:** Detects linguistic errors, provides the corrected sentence, and explains the underlying grammatical rule.
5. **Telugu $\leftrightarrow$ English Bilingual Translation:** Accurately translates phrases and sentences between English and Telugu while preserving context.
6. **Essays & Summaries:** Generates structured outlines, essays, and concise summaries on academic topics.
7. **Conversational Memory:** Supports multi-turn dialogue so students can ask follow-up questions (e.g., *"Can you simplify step 2?"* or *"Translate the above into Telugu"*).
8. **Modern ChatGPT-like UI:** Responsive, mobile-friendly interface with auto-expanding input, quick suggestion chips, animated typing indicator, and clean code formatting.

---

## 🧠 AI Concepts Used

- **Large Language Models (LLMs):** Leverages Google Gemini to reason through queries dynamically rather than retrieving static, pre-written answers.
- **Transformer Architecture & Self-Attention:** Understands long, multi-clause questions, code blocks, and math equations with complete semantic context.
- **Generative AI:** Dynamically creates original explanations, derivation steps, and code solutions tailored to the user's specific inputs.
- **Prompt Engineering:** Employs a custom system persona directing Gemini to act as an encouraging, patient academic tutor.
- **Natural Language Processing (NLP):** Powers grammar diagnostics and English-to-Telugu / Telugu-to-English translation.
- **Conversational AI:** Maintains session state to retain conversational context across multiple turns.

---

## 🏗️ System Architecture

```text
[ User / Student ]
       │
       ▼  (Types Doubt & clicks Send)
[ Web Browser Frontend ] (HTML5 / CSS3 / JavaScript)
       │
       ▼  (Asynchronous POST request via /ask)
[ Flask Backend Server ] (Python - app.py)
       │  ├── Validates Input & Formats JSON
       │  ├── Attaches Session History & Tutor Instructions
       │  └── Reads GEMINI_API_KEY from .env
       ▼
[ Google Gemini LLM API ] (gemini-3.1-flash-lite)
       │  └── Deep reasoning, step-by-step logic & generation
       ▼
[ AI Response returned to Flask ]
       │  └── Updates session history
       ▼
[ Frontend Formats & Displays Answer ] (1–3 second round-trip)
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python 3.9+, Flask | Application routing, session memory, and API coordination |
| **AI Engine** | Google Gemini API (`gemini-3.1-flash-lite`) | Natural language understanding, reasoning, code & translation |
| **SDK** | `google-genai` (Official Python SDK) | Secure communication with Gemini Cloud APIs |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | Responsive ChatGPT-like chat interface |
| **Configuration** | `python-dotenv` | Secure local environment variable management |

---

## 📁 Project Structure

```text
AI-Doubt-Solver/
│
├── app.py                     # Main Flask web application & API routes
├── requirements.txt           # Python dependencies (flask, google-genai, python-dotenv)
├── .env.example               # Template for environment variables (API key placeholder)
├── .gitignore                 # Excludes .env, virtual environment, and cache from Git
├── README.md                  # Project documentation & setup guide
│
├── services/
│   └── ai_service.py          # Gemini AI service class, system prompt, and context handler
│
├── templates/
│   └── index.html             # Chatbot UI template with quick-suggestion chips
│
├── static/
│   ├── css/
│   │   └── style.css          # Modern chat UI styling, animations & responsiveness
│   └── js/
│       └── script.js          # Client-side chat logic, async fetch, and Markdown renderer
│
└── tests/
    └── test_app.py            # Automated test suite for Flask endpoints & error handling
```

---

## 🚀 Installation & Setup Guide

### 1. Prerequisites
- Python 3.9 or higher installed on your machine.
- A free Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/).

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/AI-Doubt-Solver.git
cd AI-Doubt-Solver
```

### 3. Create & Activate a Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Your API Key
1. Copy the `.env.example` template to create a `.env` file:
   - **Windows:** `copy .env.example .env`
   - **macOS/Linux:** `cp .env.example .env`
2. Open `.env` and paste your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   GEMINI_MODEL=gemini-3.1-flash-lite
   FLASK_ENV=development
   FLASK_DEBUG=1
   SECRET_KEY=ai-doubt-solver-dev-secret-key-12345
   ```

### 6. Run the Application
```bash
python app.py
```
Open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🧪 Running Automated Tests

To run the automated unit test suite (verifying routes, error handling, and session management):
```bash
python -m unittest tests/test_app.py
```

---

## 🎓 Sample Demonstration Queries (For College Viva & Demo)

During your project demonstration or viva, try these sample questions to showcase each feature:

1. **Step-by-Step Mathematics:**
   > *"Solve 3x + 9 = 24 step by step"*
2. **Programming Concept & Code:**
   > *"Explain Python list comprehensions with a code example"*
3. **Telugu Translation:**
   > *"Translate 'Education is the key to success' into Telugu"*
4. **Grammar Correction:**
   > *"Correct the grammar: 'She go to market yesterday and buyed apples'"*
5. **General Knowledge / Science:**
   > *"Why is the sky blue? Explain simply"*
6. **Follow-Up Question (Conversational Memory):**
   > *"Can you give a real-life analogy for the explanation above?"*

---

## 🔒 Security & Best Practices

- **Zero Hardcoded Secrets:** The Gemini API key is loaded strictly via environment variables (`.env`).
- **Protected by `.gitignore`:** The `.env` file, virtual environments (`venv/`), and Python cache files (`__pycache__/`) are excluded from Git commits.
- **Safe Template:** `.env.example` contains only harmless placeholders.

---

## 📄 License
This project was developed for educational purposes as an AI Mini-Capstone Project.
