# 🚀 AskLegal.ai Setup Guide

A complete step-by-step guide to run the AI Legal Assistant locally on Windows.

---

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.11.x** installed ([Download Python](https://www.python.org/downloads/))
- **Docker Desktop** installed ([Download Docker](https://www.docker.com/products/docker-desktop/))
- **Google Gemini API Key** (for AI responses)

---

## 🔧 Step 1: Verify Python Installation

Open PowerShell/Command Prompt and run:

```bash
python --version
```

Expected output: `Python 3.11.x`

If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/release/python-3119/).

> ⚠️ During installation, check **"Add Python to PATH"**

---

## 🐳 Step 2: Start Redis with Docker

Make sure Docker Desktop is running, then:

```bash
cd C:\Users\91948\Downloads\AskLegal.ai-AI-Legal-Assistant-main
docker-compose up -d
```

Verify Redis is running:
```bash
docker ps
```

You should see `asklegal-redis` container running on port 6379.

---

## 📁 Step 3: Navigate to Project Directory

```bash
cd C:\Users\91948\Downloads\AskLegal.ai-AI-Legal-Assistant-main
```

---

## 🌐 Step 4: Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

### Activate the virtual environment:

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate.bat
```

You should see `(venv)` prefix in your terminal.

---

## 📦 Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:

- Flask (web framework)
- LangChain + FAISS (RAG system)
- HuggingFace Transformers (InLegalBERT embeddings)
- TensorFlow (judgment prediction)
- Google Generative AI (Gemini API)
- Redis (chat storage via Docker)
- And other required packages...

> ⏳ This may take 5-10 minutes depending on your internet speed.

---

## 🔑 Step 6: Configure Environment Variables

Edit the `.env` file in the project root directory and add your Google API key:

```env
# Google Gemini API Key
GOOGLE_API_KEY=your_actual_api_key_here

# Redis Configuration (Docker - already configured)
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## 🔐 Step 7: Get Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the API key and paste it in `.env` as `GOOGLE_API_KEY`

---

## 🧠 Step 8: Download NLTK Data (Required for Text Processing)

Open Python and run:

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

---

## 🖼️ Step 9: Install Tesseract OCR (Optional - for PDF text extraction)

If you want to use the Judgment Prediction feature with scanned PDFs:

1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install it (default path: `C:\Program Files\Tesseract-OCR`)
3. Add to PATH or set in environment:

```env
TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata
```

> ℹ️ This step is optional. The app works without it for text-based PDFs.

---

## ▶️ Step 10: Run the Application

```bash
python app.py
```

Or with Flask directly:

```bash
flask run --host=0.0.0.0 --port=5000
```

### Expected Output:

```
✅ InLegalBERT tokenizer & model ready.
✅ FAISS index loaded successfully.
🚀 Starting Flask app...
 * Running on http://127.0.0.1:5000
```

---

## 🌍 Step 11: Access the Application

Open your browser and navigate to:

```
http://localhost:5000
```

or

```
http://127.0.0.1:5000
```

---

## 📱 Application Features

| Feature                 | URL         | Description                                  |
| ----------------------- | ----------- | -------------------------------------------- |
| **Legal Chatbot**       | `/`         | Ask legal questions about Indian law         |
| **Judgment Prediction** | `/predict`  | Upload case files to predict verdict         |
| **Document Generator**  | `/generate` | Generate legal documents (bail, lease, etc.) |

---

## 🔧 Troubleshooting

### Issue: `ModuleNotFoundError`

```bash
pip install <missing_module>
```

### Issue: FAISS index error

The app will automatically rebuild the FAISS index on first run.

### Issue: TensorFlow errors on Windows

```bash
pip install tensorflow-cpu>=2.15.0
```

### Issue: Redis connection error

- Verify Docker is running: `docker ps`
- Restart Redis: `docker-compose restart`
- Check Redis logs: `docker logs asklegal-redis`

### Issue: Gemini API errors

- Verify your Google API key is valid
- Check if you have remaining quota

### Issue: Port 5000 already in use

```bash
flask run --port=5001
```

---

## 🐳 Docker Commands Reference

| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start Redis in background |
| `docker-compose down` | Stop Redis |
| `docker-compose restart` | Restart Redis |
| `docker logs asklegal-redis` | View Redis logs |
| `docker ps` | List running containers |

---

## 📂 Project Structure

```
AskLegal.ai-AI-Legal-Assistant-main/
├── app.py                    # Main Flask application
├── docker-compose.yml        # Docker configuration for Redis
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── laws_raw.json             # IPC legal data
├── ipc_embed_db_inlegalbert/ # FAISS vector database
├── views/
│   ├── chatbotLegalv2.py     # Chatbot logic
│   ├── judgmentPred.py       # Judgment prediction
│   └── docGen.py             # Document generator
├── templates/                # HTML templates
├── static/                   # CSS, JS, images
└── data/                     # Additional data files
```

---

## ✅ Quick Start Checklist

- [ ] Python 3.11 installed
- [ ] Docker Desktop installed and running
- [ ] Redis started (`docker-compose up -d`)
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with Google API key
- [ ] NLTK data downloaded
- [ ] Application running (`python app.py`)
- [ ] Browser opened to `http://localhost:5000`

---

## 🎉 Done!

Your AI Legal Assistant should now be running locally. Enjoy exploring Indian law with AI! ⚖️

---

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify Docker is running and Redis container is up
3. Ensure Python 3.11.x is being used
4. Check that all dependencies are installed

**Creators:** V Kamal Jerome | Shakthireka Karthikeyan | Kopika M | Deepesh Raj AY
