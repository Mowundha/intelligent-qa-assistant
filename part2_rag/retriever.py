from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 2. Load embeddings (same model as ingest.py!)
embeddings= HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 3. Load vectorstore from disk
vectorstore=  FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)


# 4. Create retriever with K=3
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
