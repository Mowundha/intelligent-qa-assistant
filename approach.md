# Solution Approach Document

## 1. Problem Interpretation

The task is to build an Intelligent Q&A Assistant 
with two interconnected parts:

- Part 1: Train a traditional ML classifier using 
  CLINC150 dataset to determine if a user query is 
  in-scope or out-of-scope
- Part 2: Build a RAG pipeline that retrieves 
  relevant information from a banking FAQ knowledge 
  base and generates grounded answers using an LLM

My first decisions before writing any code:
- Use CLINC150 dataset as recommended — it has 150 
  real-world intents plus a dedicated out-of-scope 
  class which is perfect for the routing layer
- Use Banking FAQ as knowledge base since CLINC150 
  contains banking intents — this ensures alignment 
  between the classifier domain and RAG domain
- Use Groq API for free LLM inference
- Use FAISS for local vector storage — free and 
  no setup required
- Deploy on Streamlit Cloud for free hosting

---

## 2. Part 1 — Model Selection Rationale

### Models Trained
I trained three models:

1. **Logistic Regression** — chosen because it works 
   well with high dimensional sparse TF-IDF vectors 
   and is fast to train

2. **Support Vector Classifier (SVC)** — chosen 
   because SVM is known to perform well on text 
   classification tasks with many features

3. **Naive Bayes (Multinomial)** — chosen as a 
   strong baseline for text classification, fast 
   and probabilistic

### Preprocessing Pipeline
- Lowercasing
- Punctuation removal
- Tokenization
- Stopword removal
- Stemming using PorterStemmer
- TF-IDF vectorization (max_features=50000, 
  ngram_range=(1,2), sublinear_tf=True)

### Results Before Tuning
| Model | Accuracy |
|-------|----------|
| Logistic Regression | 76.47% |
| SVC | 74.01% |
| Naive Bayes | 68.81% |

### Why Logistic Regression?
The confusion matrices revealed:
- LR had the strongest diagonal across all 151 
  classes — meaning most predictions were correct
- SVC had a slightly weaker diagonal with more 
  off-diagonal errors
- Naive Bayes showed the weakest diagonal with 
  the most misclassifications

Based on both accuracy numbers AND confusion 
matrix analysis, Logistic Regression was selected 
as the best model.

### Hyperparameter Tuning
Used GridSearchCV with:
```python
param_grid = {
    'C': [0.1, 1, 10],
    'solver': ['lbfgs', 'saga'],
    'max_iter': [100, 200]
}
cv=3, n_jobs=-1
```

**Best Parameters:** C=10, solver=lbfgs, max_iter=100

**Best Score after tuning: 83.65%**

---

## 3. Part 2 — Design Decisions

### Knowledge Base
Used Banking FAQ as the domain because:
- CLINC150 contains banking intents — alignment 
  between classifier and RAG domain
- Easy to create structured FAQ documents
- Clear Q&A format works well for RAG retrieval

### Documents Used (5 files)
- account_faq.txt — account management FAQs
- cards_faq.txt — debit/credit card FAQs
- loans_faq.txt — loan related FAQs
- transactions_faq.txt — transfer/payment FAQs
- general_banking_faq.txt — general banking FAQs

### Chunk Size: 500, Overlap: 50
- 500 characters captures 2-3 FAQ pairs per chunk
- Too large would include irrelevant Q&A pairs
- Too small would cut answers mid-sentence
- 50 character overlap prevents meaning loss 
  at chunk boundaries

### Embedding Model: all-MiniLM-L6-v2
- Small (80MB), fast, completely free
- Runs locally — no API key needed
- Good semantic similarity for FAQ-style text
- Industry standard for lightweight RAG systems

### Vector Store: FAISS
- Local and free — no cloud setup required
- Fast similarity search
- Persistent storage with save_local/load_local
- Simple to integrate with LangChain

### LLM: Groq API (llama-3.3-70b-versatile)
- Free tier with generous rate limits
- Current best available free model on Groq
- Fast inference via LPU hardware
- Note: Initially tried llama3-70b-8192 but it 
  was decommissioned — switched to 
  llama-3.3-70b-versatile

### Framework: LangChain
- Provides ready-made components for RAG pipeline
- TextLoader, RecursiveCharacterTextSplitter, 
  HuggingFaceEmbeddings, FAISS all integrated
- Reduces boilerplate code significantly

### Deployment: Streamlit Cloud
- Free hosting
- Easy GitHub integration
- Simple to build chat interface

---

## 4. Pipeline Integration

### How Part 1 Connects to Part 2

User Query (string)
↓
[TF-IDF Vectorizer]
transforms query to sparse vector
↓
[Logistic Regression Classifier]
predicts label (integer)
↓
label == 42 (out_of_scope)?
↓              ↓
YES             NO
↓              ↓
"I don't know"   [FAISS Retriever]
return []        finds top 3 similar chunks
↓
chunks empty?
↓
YES → "I don't know"
↓
NO
↓
context = join chunk texts
↓
[Groq LLM]
receives context + question
↓
generates answer from context
↓
return answer + source chunks

### Component Descriptions

**ingest.py**
- Input: 5 txt files from data/sample_docs/
- Process: loads files → splits into 500 char 
  chunks → creates embeddings → stores in FAISS
- Output: vectorstore/ folder saved to disk

**retriever.py**
- Input: user query string
- Process: loads vectorstore → searches for 
  similar chunks using cosine similarity
- Output: top 3 most relevant document chunks

**rag_pipeline.py**
- Input: user query string
- Process: classify → retrieve → build context 
  → call LLM → return answer
- Output: answer string + source chunks list

**app.py**
- Input: user query via Streamlit text input
- Process: calls answer_query() → formats result
- Output: answer displayed with expandable 
  source chunks in browser

---

## 5. Challenges

### Challenge 1 — Sklearn Version Mismatch
Model saved in Colab with sklearn 1.6.1 but 
local machine had 1.5.2, causing 
InconsistentVersionWarning when loading pkl files.
Fixed by pinning scikit-learn==1.6.1 in 
requirements.txt.

### Challenge 2 — CLINC150 Label Format
CLINC150 returns labels as numpy integers, not 
plain Python ints. GridSearchCV cross-validation 
failed with TypeError when using the dataset 
labels directly.
Fixed by converting labels to numpy array:
numpy.array(train_labels)

### Challenge 3 — Windows Path Issues
Windows backslash in file paths caused 
SyntaxWarning when using "data\sample_docs".
Fixed by using forward slashes and os.path.join().

### Challenge 4 — Groq Model Decommissioned
llama3-70b-8192 was decommissioned during 
development, causing BadRequestError.
Fixed by switching to llama-3.3-70b-versatile.

### Challenge 5 — LangChain Deprecations
langchain.text_splitter module moved to 
langchain_text_splitters package.
langchain_community.embeddings moved to 
langchain_huggingface package.
Fixed by updating imports accordingly.

### Challenge 6 — Streamlit Cloud Deployment
sentence-transformers tried to import torchvision 
which is not available on Streamlit Cloud, causing 
ModuleNotFoundError.
Fixed by switching to langchain-huggingface 
package and setting 
TOKENIZERS_PARALLELISM=false to prevent 
process hanging.

---

## 6. Limitations & What I Would Improve

### Current Limitations
- Classifier trained on CLINC150 general intents — 
  may occasionally misclassify banking queries as 
  out-of-scope since healthcare/specialized banking 
  terms aren't in CLINC150
- Knowledge base has only 5 documents — limited 
  coverage of banking topics
- No conversation memory — each question is 
  independent, no follow-up questions supported
- Embedding model all-MiniLM-L6-v2 is small — 
  larger model would improve retrieval quality

### What I Would Improve With More Time
- Retrain classifier specifically on banking domain 
  queries for better in-scope detection
- Add more documents to knowledge base (50+ FAQs)
- Use larger embedding model (all-mpnet-base-v2) 
  for better semantic search
- Add conversation history to support follow-up 
  questions
- Implement confidence scoring for hallucination 
  guard instead of simple empty-chunk check
- Add PDF support to knowledge base loader