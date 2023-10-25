import streamlit as st
import boto3
import time
import config
import langchain
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
from langchain.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
from langchain.vectorstores import FAISS
from langchain.vectorstores import OpenSearchVectorSearch
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from utils.get_tables import get_tables
from utils.dict_to_multiline import dict_to_multiline_string
from utils.render_form import render_form
from utils.search_table import search_tables
from utils.generate_sql import generate_sql
from utils.get_athena_result import get_athena_result

import pandas as pd
    
if __name__ == "__main__":
    
    # Page configuration
    
    st.set_page_config(
        page_title='Text-to-SQL using AWS',
        page_icon=':space_invader:',
        initial_sidebar_state='collapsed')
    st.title(':violet[Text-to-SQL] using AWS :space_invader:')
    
    # Variables
    
    langchain.verbose = True
    session = boto3.session.Session()
    region = config._global['region']
    credentials = session.get_credentials()
    service = 'es'
    http_auth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        service,
        session_token=credentials.token)
    opensearch_cluster_domain_endpoint = config.opensearch['domain_endpoint']
    domain_name = config.opensearch['domain_name']
    index_name = "index-superglue"
    
    # Create AWS Glue client
    glue_client = boto3.client('glue', region_name=region)
    
    # Amazon Bedrock LangChain clients
    bedrock_llm = Bedrock(
        model_id="anthropic.claude-v2",
        model_kwargs={
            'max_tokens_to_sample': 3000})
    bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1")
    
    # VectorDB type
    
    vectorDB = st.selectbox(
        "VectorDB",
        ("FAISS (local)", "OpenSearch (Persistent)"),
        index=0
    )
    
    if vectorDB == "FAISS (local)":
        st.markdown("<br>", unsafe_allow_html=True)
        with st.status("Connecting to Glue Data Catalog :man_dancing:"):
    
            catalog, num_db, num_tables = get_tables(glue_client)
    
            # Check if an index copy of FAISS is stored locally
    
            try:
                vectorstore_faiss = FAISS.load_local(
                    "faiss_index", bedrock_embeddings)
            except BaseException:
                docs = [
                    Document(
                        page_content=dict_to_multiline_string(x),
                        metadata={
                            "source": "local"}) for x in catalog]
    
                vectorstore_faiss = FAISS.from_documents(
                    docs,
                    bedrock_embeddings,
                )
    
                vectorstore_faiss.save_local("faiss_index")
    
        k, query = render_form(catalog, num_db, num_tables)
    
        if st.button('Search relevant tables :dart:'):
    
            search_tables(vectorstore=vectorstore_faiss, k=k, query=query)

        sql_query = ""
        if st.button('Generate SQL :crystal_ball:'):
            sql_query = generate_sql(vectorstore=vectorstore_faiss, k=k, query=query, region=region)
            
        if sql_query:
            print("Calling get_athena_result")
            print(sql_query)
            get_athena_result(sql_query)
    
    elif vectorDB == "OpenSearch (Persistent)":
    
        with st.status("Connecting to Glue Data Catalog :man_dancing:"):
    
            catalog, num_db, num_tables = get_tables(glue_client)
    
            # Initialize Opensearch Vector Search clients
    
            vectorstore_opensearch = OpenSearchVectorSearch(
                index_name=index_name,
                embedding_function=bedrock_embeddings,
                opensearch_url=opensearch_cluster_domain_endpoint,
                engine="faiss",
                timeout=300,
                use_ssl=True,
                verify_certs=True,
                http_auth=http_auth,
                connection_class=RequestsHttpConnection
            )
    
        k, query = render_form(catalog)
    
        if st.button('Search relevant tables :dart:'):
            search_tables(vectorstore=vectorstore_opensearch, k=k, query=query)
    
        if st.button('Generate SQL :crystal_ball:'):
    
            generate_sql(vectorstore=vectorstore_opensearch, k=k, query=query)
