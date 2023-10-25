import streamlit as st

# Function to perform a similarity search
def search_tables(vectorstore, k, query):
    relevant_documents = vectorstore.similarity_search_with_score(query, k=k)
    for rel_doc in relevant_documents:
        st.write(rel_doc[0].page_content.split(" ")[0])
        st.write("Score: ", rel_doc[1])
        st.divider()