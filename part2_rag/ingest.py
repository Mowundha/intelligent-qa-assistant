from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

docs = []
for file in os.listdir("../data/sample_docs"):
    full_path = os.path.join("../data/sample_docs", file)
    text_loader = TextLoader(full_path)
    docs.extend(text_loader.load())

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, 
    chunk_overlap=50
)
chunks = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("vectorstore")