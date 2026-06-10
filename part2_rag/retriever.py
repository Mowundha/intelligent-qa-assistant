# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 2. Load embeddings (same model as ingest.py!)
# embeddings= HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False}
)

# 3. Load vectorstore from disk
vectorstore=  FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)


# 4. Create retriever with K=3
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
