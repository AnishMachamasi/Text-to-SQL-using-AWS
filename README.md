# Search Your AWS Glue Data Catalog Tables with Text


**AWS Glue Data Catalog** is a central metadata repository that provides a unified view of data across diverse data stores. It makes it easy to discover, understand, and manage data.

One of the challenges of working with large datasets is finding the right tables to query. With traditional methods, you need to have a good understanding of the data schema and table names. This can be time-consuming and error-prone, especially if you are working with a new dataset.

A text-based search capability for Glue Data Catalog tables can make it much easier to find the right tables to query. You can simply enter a keyword or phrase related to the data you are looking for, and the search engine will return a list of relevant tables.

![Untitled Diagram drawio (5)](https://github.com/AnishMachamasi/Text-to-SQL-using-AWS/assets/98002255/2f41bebe-3ab6-4eee-9391-69d3a6c20488)


## Architecture

The architecture works as follows:

1. The user initiates the application, triggering the indexing of crucial information such as database name, table name, and column name into the FAISS vector database.

2. Subsequently, the user inputs a textual query within a Streamlit app.

3. The query and the vector database are then dispatched to **Bedrock LLM (Language Model)**.

4. Bedrock LLM processes the input and generates an SQL query as a response.

5. The SQL query is forwarded to **Athena**, which commences the execution of the query and subsequently transmits the necessary query results back to the user.

6. Finally, the query results are presented within the Streamlit app interface.

**Note:** In this project, we utilize a local vector database, FAISS. However, it's worth mentioning that **AWS OpenSearch Service** can also be employed to store this information.

## Prerequisites

### AWS Account

You need to have an AWS Account to run this code. If you have an AWS account, you should have AWS CLI configured in your system. In case you do not configure the CLI, you can manually set your Access Key and Secret Access Key in the code.

### Region

This code should run in the region where:

- Your Glue Data Catalog is hosted.
- **Amazon Bedrock** service is available.

### Python Version

This code is tested on Anaconda Environment with **Python 3.11.5**.

## Installation

Install required dependencies by following the command:

```bash
pip install -r requirements.txt
```
## Usage

Run the Streamlit app using the following command:

```bash
pip install -r requirements.txt
```

## Demo
https://github.com/AnishMachamasi/Text-to-SQL-using-AWS/assets/98002255/dd8b021a-e40d-4beb-a42e-c573eac162b5

## Workflow
You can see entire architecture workflow at [blog](https://macha7.hashnode.dev/search-your-aws-glue-data-catalog-tables-with-text).



