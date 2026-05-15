# 🎤 InterviewGPT — AI Mock Interview Platform

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.57-red)
![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-orange)
![HuggingFace](https://img.shields.io/badge/Sentence_Transformers-all--MiniLM--L6--v2-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

An AI-powered mock interview platform that **generates personalized interview questions** based on your resume and a job description, then **evaluates your answers** (via voice or text) using advanced NLP and LLM techniques — just like a real interview, but with instant, actionable feedback.

**Try the live demo, speak your answers, and get your performance score!**

Built with ❤️ by [SyedMinhal570](https://github.com/SyedMinhal570)

---

## 🌟 Features

- 📤 **Resume Parsing (PDF)** – automatically extracts text from uploaded PDF resumes using **PyPDF2**
- 📝 **Job Description Input** – paste any target job description for tailored interview preparation
- 🧠 **AI-Generated Questions** – powered by **Google Gemini (`gemini-2.5-flash`)** to generate technical + behavioral interview questions
- 🎤 **Voice Input Support** – answer directly through your browser microphone using Streamlit’s native `st.audio_input` widget and Google Web Speech API
- ⌨️ **Text Input Option** – type or edit answers manually if voice input is unavailable
- 📊 **Multi-Factor Answer Scoring** including:
  - **Relevance Score** (semantic similarity using Sentence Transformers)
  - **Grammar Analysis**
  - **Readability Score** (Flesch Reading Ease)
  - **Keyword Match Evaluation**
- 📈 **Detailed Performance Report** – per-question analysis with overall interview score
- 💡 **Instant Improvement Feedback** – actionable suggestions to improve weak areas
- 🎨 **Modern UI Design** – glassmorphism styling with animated interactive buttons
- 🔐 **Secure API Key Management** – protected using `.env` configuration

---

## 🛠️ Tech Stack

| Area | Technology / Library |
|------|-----------------------|
| Language | Python 3.11+ |
| Web Framework | Streamlit 1.57 |
| LLM | Google Gemini API (`gemini-2.5-flash`) |
| NLP / Embeddings | HuggingFace Sentence Transformers (`all-MiniLM-L6-v2`) |
| Speech-to-Text | Google Web Speech API (`SpeechRecognition`) |
| PDF Parsing | PyPDF2 |
| Readability Analysis | `textstat` |
| Environment Management | `python-dotenv` |

---

## 📁 Project Structure

```text
InterviewGPT/
├── utils/
│   ├── __init__.py
│   ├── pdf_parser.py        # Extract text from PDF resumes
│   ├── question_gen.py     # Gemini-based question generation
│   └── evaluator.py        # Multi-factor answer evaluation
├── app.py                  # Main Streamlit application
├── .env                    # Gemini API key (not pushed to GitHub)
├── requirements.txt
├── .gitignore
└── README.md

# 🚀 Quick Start (Run Locally)

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/SyedMinhal570/InterviewGPT.git
cd InterviewGPT
```

---

## 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv venv
```

### Windows PowerShell

```bash
.\venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Set Up Gemini API Key

Get your free API key from **Google AI Studio**.

Create a `.env` file in the project root directory:

```text
GEMINI_API_KEY=your_api_key_here
```

> ⚠️ Make sure `.env` is included in `.gitignore`.

---

## 5️⃣ Launch the Application

```bash
streamlit run app.py
```

---

## 6️⃣ Open in Browser

Visit:

```text
http://localhost:8501
```

and start your AI-powered mock interview experience 🚀

---

# 🎯 How It Works

1. Upload your **resume (PDF)** and paste the **job description**
2. The system uses **Google Gemini** to generate personalized interview questions
3. Answer using:
   - 🎤 Voice input (microphone)
   - ⌨️ Text input
4. Each response is evaluated based on:
   - Relevance
   - Grammar
   - Readability
   - Keyword Matching
5. Receive a complete performance report with feedback and overall score

---

# 📸 Screenshots

Add screenshots or GIF demos here to make the repository even more impressive!

```markdown
![Demo](screenshots/demo.gif)
```

---

# 🤝 Contributing

Pull requests are welcome.

For major changes, please open an issue first to discuss what you would like to improve.

---

# 📜 License

This project is licensed under the **MIT License**.