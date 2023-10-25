import streamlit as st
import boto3
import time
import pandas as pd
import re

athena_client = boto3.client('athena')

def get_athena_result(sql_query):
    # Use regular expressions to extract the database name
    match = re.search(r'FROM\s+([\w_]+)\.\w+', sql_query)

    database_name=""
    if match:
        database_name = match.group(1)
        print(database_name)

        queryStart = athena_client.start_query_execution(
            QueryString = sql_query,
            QueryExecutionContext = {
                'Database': database_name
            }, 
            ResultConfiguration = { 'OutputLocation': 's3://layer-bucket-test-anish/'}
        )

        query_execution_id = queryStart['QueryExecutionId']

        time.sleep(7)

        # Streamlit app
        st.title("Athena Query Results")

        # Display a loading spinner
        with st.spinner("Running Athena Query..."):

            result = athena_client.get_query_results(QueryExecutionId=query_execution_id)
            
            column_names = [col['Label'] for col in result['ResultSet']['ResultSetMetadata']['ColumnInfo']]
            data_rows = [list(row['VarCharValue'] for row in row['Data']) for row in result['ResultSet']['Rows'][1:]]

            # Create a Pandas DataFrame for better formatting
            data = pd.DataFrame(data_rows, columns=column_names)

            # Display the table
            st.table(data)