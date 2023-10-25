from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock

import streamlit as st
import time

# Function to generate LLM response (SQL + Explanation)

bedrock_llm = Bedrock(
    model_id="anthropic.claude-v2",
    model_kwargs={
        'max_tokens_to_sample': 3000})
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1")

def generate_sql(vectorstore, k, query, region):
    prompt_template = """
        \n\nHuman: Between <context></context> tags, you have a description of tables with their associated columns. Create a SQL query to answer the question between <question></question> tags only using the tables described between the <context></context> tags. If you cannot find the solution with the provided tables, say that you are unable to generate the SQL query.

    <context>
    {context}
    </context>

    Question: <question>{question}</question>

    # Rules
    1. Provide your answer using the following xml format: <result><sql>SQL query</sql><explanation>Explain clearly your approach, what the query does, and its syntax</explanation></result>
    Assistant:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa = RetrievalQA.from_chain_type(
        llm=bedrock_llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
        verbose=True
    )
    with st.status("Generating response :thinking_face:"):
        answer = qa({"query": query})

    # st.write(answer)

    with st.status("Searching tables :books:"):
        time.sleep(1)

    for i, rel_doc in enumerate(answer["source_documents"]):
        st.write(rel_doc.page_content.split(" ")[0])

    with st.status("Rendering response :fire:"):
        sql_query = answer["result"].split("<sql>")[1].split("</sql>")[0]
        explanation = answer["result"].split("<explanation>")[1].split("</explanation>")[0]

    st.code(sql_query, language='sql')
    st.link_button(
        "Athena console :sun_with_face:",
        "https://{0}.console.aws.amazon.com/athena/home?region={0}".format(region))

    st.write(explanation)

    return sql_query