import streamlit as st
from rag_pipeline import answer_query

# Page config
st.set_page_config(
    page_title="Banking Q&A Assistant",
    page_icon="🏦",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 8px;
        padding: 8px 24px;
        font-size: 16px;
    }
    .answer-box {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        margin: 10px 0;
    }
    .idk-box {
        background-color: #fce4ec;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #c62828;
        margin: 10px 0;
    }
    .source-box {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
    }
    .chat-question {
        background-color: #1a73e8;
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .chat-answer {
        background-color: #ffffff;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
        border: 1px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🏦 Banking Q&A Assistant")
# st.markdown("*Powered by RAG + Groq LLM*")
st.divider()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat history
if st.session_state.chat_history:
    st.subheader("💬 Conversation History")
    for item in st.session_state.chat_history:
        st.markdown(f'<div class="chat-question">🧑 {item["question"]}</div>',
                   unsafe_allow_html=True)
        if "I don't know" in item["answer"]:
            st.markdown(f'<div class="idk-box">🤖 {item["answer"]}</div>',
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-answer">🤖 {item["answer"]}</div>',
                       unsafe_allow_html=True)
    st.divider()

# Input section
st.subheader("Ask a Question")
query = st.text_input(
    "Your Question:",
    placeholder="e.g. How do I check my account balance?"
)

col1, col2 = st.columns([1, 5])
with col1:
    ask_btn = st.button("Ask")
with col2:
    if st.button("Clear History"):
        st.session_state.chat_history = []
        st.rerun()

# When Ask is clicked
if ask_btn:
    if query.strip() == "":
        st.warning("⚠️ Please enter a question!")
    else:
        with st.spinner(" Searching knowledge base..."):
            answer, chunks = answer_query(query)

        # Add to history
        st.session_state.chat_history.append({
            "question": query,
            "answer": answer
        })

        # Show answer
        st.divider()
        st.subheader(" Answer")

        if "I don't know" in answer:
            st.markdown(
                f'<div class="idk-box">❌ {answer}</div>',
                unsafe_allow_html=True
            )
            st.info("💡 This question is outside the scope of our banking knowledge base.")
        else:
            st.markdown(
                f'<div class="answer-box">✅ {answer}</div>',
                unsafe_allow_html=True
            )

        # Show sources
        if chunks:
            st.subheader("📚 Sources Used")
            for i, chunk in enumerate(chunks):
                with st.expander(f"📄 Source {i+1}"):
                    st.markdown(
                        f'<div class="source-box">{chunk.page_content}</div>',
                        unsafe_allow_html=True
                    )