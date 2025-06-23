# 🧠 RAG Q\&A System for Documentation Search

This is a Retrieval-Augmented Generation (RAG) application built using [LangChain](https://www.langchain.com/), [Ollama](https://ollama.com), and [ChromaDB](https://www.trychroma.com/). It helps users search and query internal documentation (PDFs) using local LLMs and embeddings.

---

## 📁 Project Structure

```
rag-app/
├── main.py                     # RAG Q&A interface using LangChain + Ollama LLM
├── vector.py                   # Vector store setup using Chroma + Ollama embeddings
├── requirements.txt            # Python dependencies
├── .gitignore                  # Ignore venv, Chroma DB, etc.
├── pdfs/                       # Place your PDF documents here
└── chroma_langchain_db_pdf/    # Auto-generated vector store (ignored in Git)
```

---

## ✅ Prerequisites

1. Python 3.8+
2. Git
3. [Ollama installed](https://ollama.com/download)

---

## 🚀 Setup Instructions

Follow these steps to set up and run the application:

### 1. Clone the Repository


### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
# Activate:
source venv/bin/activate      # On Linux/Mac
.\venv\Scripts\activate       # On Windows
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🧠 Ollama Model Setup

This app uses **local Ollama models**. You need to install and pull the required models:

### Step 1: Install Ollama

* Download and install from: [https://ollama.com/download](https://ollama.com/download)

### Step 2: Pull the required models

```bash
ollama pull gemma3
ollama pull mxbai-embed-large
```

---

## 📄 Add Your PDF Files

Place all your documentation PDFs inside the `pdfs/` folder.


## ▶️ Run the Application

Once setup is complete, you can run the app:

```bash
python main.py
```

You will see a prompt:

```
RAG Q&A System - Internship Documentation
Type 'q' to quit
==================================================
```

Ask your question related to the documentation, and the assistant will provide an answer based on retrieved content.

---

## 🧹 Notes

* The `chroma_langchain_db_pdf/` folder is auto-generated for vector storage. It’s already `.gitignored`.
* To rebuild the vector DB from scratch, delete the folder and set `force_rebuild=True` in `vector.py`:

  ```python
  vector_store = setup_vector_store(force_rebuild=True)
  ```

---

## 🛠️ Tech Stack

* [LangChain](https://www.langchain.com/)
* [Ollama](https://ollama.com/)
* [ChromaDB](https://www.trychroma.com/)
* [PyMuPDF](https://github.com/pymupdf/PyMuPDF)

---
