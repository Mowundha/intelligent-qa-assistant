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
        {"role": "system", "content": "You are a helpful banking assistant. Answer only from the given context. If answer not in context say I don't know."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]
    )

    answer = response.choices[0].message.content
    return answer, retriever_result
    

    
if __name__ == "__main__":
    answer, chunks = answer_query("how to check my account balance")
    print("Answer:", answer)
    print("Sources:", len(chunks), "chunks used")