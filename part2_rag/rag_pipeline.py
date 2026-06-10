# 1. Imports
import os, joblib
from groq import Groq
from dotenv import load_dotenv
from retriever import retriever

# 2. Load env + Groq client
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 3. Load classifier + vectorizer
classifier = joblib.load("../part1_nlp/best_model.pkl")
vectorizer = joblib.load("../part1_nlp/vectorizer.pkl")

# 4. Main function
def answer_query(query):
    # classify → retrieve → LLM → return answer
    # vectorize= vectorizer.transform([query])
    # prediction= classifier.predict(vectorize)

    # if prediction[0] == 42:
    #     return "I don't know" , []
    
    retriever_result= retriever.invoke(query)

    if not retriever_result:
        return "I don't know" , []
    
    context = "\n".join([chunk.page_content for chunk in retriever_result])

    response = client.chat.completions.create(
    # model="llama3-8b-8192",
    # model="llama3-70b-8192",
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a helpful banking assistant. Use the provided context to answer the question. Give a clear and complete answer based on the context. Only say 'I don't know' if the context has absolutely no relevant information."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]
    )

    answer = response.choices[0].message.content
    return answer, retriever_result
    

    
