# # from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# import os

# os.environ["TOKENIZERS_PARALLELISM"] = "false"

# # 2. Load embeddings (same model as ingest.py!)
# # embeddings= HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# embeddings = HuggingFaceEmbeddings(
#     model_name="all-MiniLM-L6-v2",
#     model_kwargs={"device": "cpu"},
#     encode_kwargs={"normalize_embeddings": False}
# )

# # 3. Load vectorstore from disk
# # vectorstore=  FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# vectorstore = FAISS.load_local(
#     os.path.join(BASE_DIR, "vectorstore"),
#     embeddings,
#     allow_dangerous_deserialization=True
# )


# # 4. Create retriever with K=3
# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

os.environ["TOKENIZERS_PARALLELISM"] = "false"

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False}
)

# Fix: use absolute path so it works on both local and Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTORSTORE_PATH = os.path.join(BASE_DIR, "vectorstore")

vectorstore = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})