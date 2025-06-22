# pdf-qa-chatbot
Sure Pranav! Here's the full `README.md` content in **plain text format** so you can copy it **directly** and paste it into your GitHub repo manually:

---

```
# 🤖 Lexa – PDF Q&A Chatbot with Test Generator

Lexa is an AI-powered chatbot that allows users to upload a PDF (like a resume, textbook, or notes), ask questions about its content, and generate MCQ-based practice tests based on subject and difficulty.

---

## 🧠 Features

- 📄 Upload PDFs and automatically extract content.
- 💬 Ask natural language questions about the PDF.
- ⚙️ Backend powered by LangChain and FAISS vector store.
- 📝 Generate PDF-based MCQ tests from a CSV question bank.
- 🌈 Modern UI with full-screen chatbot interface and animated effects.

---

## ⚙️ Tech Stack

Frontend:
- React.js
- Tailwind CSS
- Axios

Backend:
- FastAPI
- Uvicorn
- LangChain
- HuggingFace Embeddings
- FAISS
- fpdf
- pypdf

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```

git clone [https://github.com/PranavSatya/pdf-qa-chatbot.git](https://github.com/PranavSatya/pdf-qa-chatbot.git)
cd pdf-qa-chatbot

```

---

### 2. Frontend Setup

```

cd frontend
npm install
npm start

```

Runs on: http://localhost:3000

---

### 3. Backend Setup

```

cd backend
python -m venv venv

# Activate virtual environment:

# On Windows:

venv\Scripts\activate

# On Mac/Linux:

source venv/bin/activate

pip install -r requirements.txt
uvicorn main\:app --reload

```

Runs on: http://localhost:8000

---

## 📂 Folder Structure

```

pdf-qa-chatbot/
├── frontend/              # React UI
├── backend/               # FastAPI server
│   ├── main.py            # API endpoints
│   ├── qa\_engine.py       # PDF indexing & question answering
│   ├── test\_generator.py  # Test generation logic
│   └── uploads/           # Uploaded PDFs
├── generated\_pdfs/        # Output test PDFs
├── questions.csv          # MCQ bank
├── README.md
└── .env                   # API keys

```

---

## 🔐 Environment Variables

Create a `.env` file in the `backend/` folder and add:

```

TOGETHER\_API\_KEY=your\_together\_api\_key

```

---

## 📤 API Endpoints

| Method | Endpoint             | Description                      |
|--------|----------------------|----------------------------------|
| POST   | `/upload/`           | Upload PDF and create index      |
| POST   | `/ask/`              | Ask question and get response    |
| POST   | `/generate-test/`    | Generate a test PDF              |
| GET    | `/generated_pdfs/`   | Download test PDFs               |

---

## 🧪 Sample CSV Format for Test Generator

```

subject,difficulty,question,option\_a,option\_b,option\_c,option\_d,answer,explanation
Math,Easy,What is 2+2?,1,2,3,4,D,It’s basic addition.

```

---

## 👨‍💻 Author

**Pranav Satya**  
GitHub: [@PranavSatya](https://github.com/PranavSatya)

---

## 📄 License

This project is licensed under the MIT License.

---

> Built with ❤️ using React, FastAPI & LangChain.
```

