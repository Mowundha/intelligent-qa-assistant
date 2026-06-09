import streamlit as st
from rag_pipeline import answer_query

st.title("Intelligent Q&A Assistant")

query = st.text_input("Ask a question:")

if st.button("Ask"):
    if query:
        answer, sources = answer_query(query)

        st.write("### Answer")
        st.write(answer)

        st.write("### Sources")
        for i, chunk in enumerate(sources):
            st.expander(f"Chunk {i+1}").write(chunk.page_content)
    else:
        st.warning("Please enter a question!")





# import streamlit as st
# from rag_pipeline import answer_query

# # Page config
# st.set_page_config(
#     page_title="Intelligent Q&A Assistant",
#     page_icon="🤖",
#     layout="centered"
# )

# # Header
# st.title("🤖 Intelligent Q&A Assistant")
# st.markdown("Ask questions about **banking, loans, cards & transactions**")
# st.divider()

# # Input
# query = st.text_input("💬 Your Question:", placeholder="e.g. How do I check my account balance?")

# if st.button("Ask", type="primary", use_container_width=True):
#     if query:
#         with st.spinner("Thinking..."):
#             answer, sources = answer_query(query)

#         # Answer box
#         if answer == "I don't know":
#             st.error("❌ I don't know — question is out of scope.")
#         else:
#             st.success("✅ Answer")
#             st.write(answer)

#             # Sources
#             st.divider()
#             st.markdown(f"📚 **{len(sources)} source chunks used:**")
#             for i, chunk in enumerate(sources):
#                 with st.expander(f"📄 Chunk {i+1}"):
#                     st.write(chunk.page_content)
#     else:
#         st.warning("⚠️ Please enter a question first!")