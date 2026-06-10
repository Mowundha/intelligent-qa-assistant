# Intelligent Q&A Assistant

A Banking FAQ chatbot built with RAG (Retrieval-Augmented Generation) pipeline.

## Project Structure

aiml-assignment/
├── data/sample_docs/     ← Knowledge base documents
├── part1_nlp/
│   └── classification.py ← Intent classifier
├── part2_rag/
│   ├── ingest.py         ← Document ingestion
│   ├── retriever.py      ← Vector search
│   ├── rag_pipeline.py   ← Main pipeline
│   └── app.py            ← Streamlit UI
├── approach.md
├── test_cases.md
└── requirements.txt

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Mowundha/intelligent-qa-assistant.git
cd intelligent-qa-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Add your GROQ_API_KEY in .env file
```

### 4. Run document ingestion
```bash
cd part2_rag
python ingest.py
```

### 5. Run the classifier
```bash
cd part1_nlp
python classification.py
```

### 6. Run the full pipeline
```bash
cd part2_rag
streamlit run app.py
```

## Public URL
[Banking Q&A Assistant](https://intelligent-app-assistant-xwjdtexcunh62ci76adxlw.streamlit.app)
