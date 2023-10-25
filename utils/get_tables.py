# Function to get all tables from Glue Data Catalog
def get_tables(glue_client):
    # get all AWS Glue databases
    databases = glue_client.get_databases()

    tables = []

    num_db = len(databases['DatabaseList'])

    for db in databases['DatabaseList']:
        tables = tables + \
            glue_client.get_tables(DatabaseName=db['Name'])["TableList"]

    num_tables = len(tables)

    return tables, num_db, num_tables