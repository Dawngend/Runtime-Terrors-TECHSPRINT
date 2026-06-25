# 🧠 RUNTIME TERROR: AI-Powered Study Tool for Filipino Learners

 An intelligent, pure Python web platform built to address the unique challenges of the Philippine educational landscape. This active learning companion acts as a dynamic study dashboard, leveraging a dual-API AI architecture to generate precise, format-matched flashcards and serve as a conversational tutor contextualized for Filipino learners.

---

## ✨ Features
* **Cloud-Based Multi-Account Authentication Flow:** A functional sign-up and log-in system matching user credentials against secure cloud storage, ensuring individual students can save their preferences and access their accounts concurrently.
* **Dual-API Intelligent Flashcard Engine:** A functional, two-tier AI generation process where **API 1 (Groq Llama 3.3)** acts as the primary question generator, and **API 2 (NVIDIA Qwen 122B)** serves as a real-time evaluator to screen, refine, and structure the flashcards to meet explicit formatting guidelines.
* **Format-Mimicking Upload Engine:** A feature in the "Create New Reviewer" dashboard that accepts user-uploaded sample questions. The background AI pipeline analyzes these samples and forces newly generated materials to replicate that exact layout and structure.
* **Dynamic Study Dojo & Real-Time Mastery Tracker:** Spaced-repetition quiz interface displaying progress, subject categories, and dynamic Mastery score calculations synced in real-time.
* **End-of-Round Focus Recommendations:** Options to reflash the entire deck, review missed questions, or use AI to generate a tailored *Focus Set* based on questions missed on the first attempt.
* **Online-Connected AI Tutor Chat:** Chat window supporting Taglish, English, and Tagalog language styles with optional live DuckDuckGo web-search capabilities.

---

## 💻 Technologies Used
* **Frontend & Orchestration:** Python, Streamlit
* **Backend & Database:** Supabase (PostgreSQL)
* **Vector Memory Database:** ChromaDB
* **API 1 (Primary Model):** Groq (Llama 3.3 70B Versatile)
* **API 2 (Evaluator & Format Matcher):** NVIDIA NIM (Qwen 2.5 122B Instruct)
* **Optical Character Recognition (OCR):** Tesseract OCR (via `pytesseract`)

---

## ⚙️ Step-by-Step Local Setup Instructions

Follow these instructions to run the application locally on your laptop:

### 1. Prerequisites & System Dependencies
Ensure you have the following installed on your machine:
* **Python 3.9 - 3.12**
* **Tesseract OCR (Required for PDF/Image OCR Scanning)**:
  * **Windows**: Download and run the [UB Mannheim Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki). Install it to the default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`.
  * **macOS**: Install via Homebrew:
    ```bash
    brew install tesseract
    ```
  * **Linux (Ubuntu/Debian)**: Install via apt:
    ```bash
    sudo apt update
    sudo apt install tesseract-ocr
    ```

### 2. Clone the Repository
Open your terminal (PowerShell, Command Prompt, or terminal emulator) and run:
```bash
git clone https://github.com/Dawngend/Runtime-Terrors-TECHSPRINT.git
cd Runtime-Terrors-TECHSPRINT
```

### 3. Create and Activate a Virtual Environment
Initialize a clean Python virtual environment to manage dependencies:
* **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 4. Install Dependencies
Install all the required Python libraries using pip:
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a file named `.env` in the root folder of the project (`Runtime-Terrors-TECHSPRINT/.env`) and populate it with the following keys:
```env
# --- Supabase Database Configuration ---
SUPABASE_URL="https://nelsfowiptrcurtuxoav.supabase.co"
SUPABASE_KEY="your-supabase-publishable-anon-key"

# --- AI APIs Keys ---
GROQ_API_KEY="your-groq-api-key"
NVIDIA_API_KEY="your-nvidia-api-key-for-qwen"

# --- Paths & App Settings ---
CHROMA_DB_PATH=./chroma_db
EXTRACTION_CACHE=./extraction_cache
DEBUG=True
DEFAULT_GRADE_LEVEL=10
MAX_FILE_SIZE_MB=10
```
> ⚠️ **Important**: Do not commit your `.env` file to git. It is ignored by default in `.gitignore`.

### 6. Run the System Health Check
Before launching the app, run the built-in system verification script to confirm database connectivity, vector memory setup, extraction capabilities, and AI API authentication:
```bash
# On Windows PowerShell
$env:PYTHONIOENCODING="utf-8"; python check_system.py

# On macOS/Linux
PYTHONIOENCODING=utf-8 python check_system.py
```
Look for the confirmation message:
`🎉 SYSTEM HEALTHY: All modules loaded successfully!`

### 7. Run the Web Application
Start the Streamlit development server:
```bash
streamlit run app.py
```
A browser window should automatically open to `http://localhost:8501`. If it doesn't, copy-paste the URL from your terminal.

---

## 👥 Team Members and Rules

### Team: RUNTIME TERROR
* **Jibrael D. Gumba**
* **Vinz Emmanuel B. Cruz**
* **Dawn Andrei Pamesa**

### Collaboration Rules
1. **Branching:** Do not push directly to `main`. Create isolated feature branches for your assigned tasks (e.g., `feature/auth-ui`, `bugfix/flashcard-logic`).
2. **Commits:** Write clear, concise commit messages detailing the changes made.
3. **Security:** **NEVER** commit `.env` files or hardcode API keys into the Python scripts. Always use environment variables.
4. **Merging:** Pull the latest changes from `origin main` before submitting or merging your code to avoid terminal merge conflicts. Do not force push to `main` without team consensus.
