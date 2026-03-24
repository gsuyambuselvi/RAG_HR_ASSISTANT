# HR Policy Assistant — RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers employee questions based on HR policy documents. Built with OpenAI, Pinecone, and Streamlit.

---

## Architecture

```
PDF Documents
     │
     ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  pdfreader  │────▶│   chunker   │────▶│   embedder  │
│  (pypdf)    │     │ (text split)│     │  (OpenAI)   │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  Pinecone   │
                                        │ Vector DB   │
                                        └─────────────┘
                                               │
User Query ──▶ embed_User_query ───────────────┘
                                               │
                                        similarity search
                                               │
                                               ▼
                                        ┌─────────────┐     ┌─────────────┐
                                        │   Top K     │────▶│  OpenAI LLM │
                                        │   Chunks    │     │  GPT-3.5    │
                                        └─────────────┘     └─────────────┘
                                                                   │
                                                                   ▼
                                                            Final Answer
                                                          (Streamlit UI)
```

### How it works

1. **Ingestion** — PDF files are read, split into overlapping chunks, embedded using OpenAI, and stored in Pinecone.
2. **Query** — The user's question is embedded, Pinecone finds the most relevant chunks (top 4), and OpenAI GPT-3.5 generates an answer using those chunks as context.
3. **UI** — Streamlit provides a chat interface that maintains conversation history.

---

## Project Structure

```
RAG_HR_ASSISTANT/
├── resources/          # HR policy PDF documents
│   ├── HRPolicy.pdf
│   └── HRPolicyV1.pdf
├── pdfreader.py        # Reads and extracts text from PDFs
├── chunker.py          # Splits text into overlapping chunks
├── embedder.py         # Embeds chunks and queries using OpenAI
├── vectorstore.py      # Stores and searches vectors in Pinecone
├── dataprocessor.py    # Ingestion pipeline (run once per new PDF)
├── QueryProcessor.py   # Query pipeline (embed → search → LLM)
├── app.py              # Streamlit chatbot UI
├── requirements.txt    # Python dependencies
├── .env.example        # Template for environment variables
└── .gitignore          # Excludes .env and cache files
```

---

## Prerequisites

- Python 3.9+
- [OpenAI API key](https://platform.openai.com/api-keys)
- [Pinecone account](https://www.pinecone.io/) with an index created (dimension: `1536`, metric: `cosine`)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/gsuyambuselvi/RAG_HR_ASSISTANT.git
cd RAG_HR_ASSISTANT
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

```
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=your_pinecone_index_name_here
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Running the Application

### Step 1 — Ingest PDF documents into Pinecone (run once)

Place your HR policy PDFs inside the `resources/` folder, then run:

```bash
python dataprocessor.py
```

This reads all PDFs in `resources/`, chunks them, embeds them, and stores them in Pinecone.

### Step 2 — Launch the chatbot UI

```bash
python -m streamlit run app.py
```

Open your browser at `http://localhost:8501` and start asking questions.

---

## Adding New Policy Documents

1. Add your PDF to the `resources/` folder.
2. Re-run `python dataprocessor.py`.
3. The new document will be added to Pinecone without overwriting existing ones.

---

## Example Questions

- *What is the maternity leave policy?*
- *How many days of sick leave am I entitled to?*
- *What are the contractor work timings?*
- *How do I book a meeting room?*
- *Can I carry over unused annual leave?*
