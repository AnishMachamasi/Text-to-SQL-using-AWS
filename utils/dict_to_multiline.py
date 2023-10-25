# Function to flatten JSON representations of Glue tables
def dict_to_multiline_string(d):

    lines = []
    db_name = d['DatabaseName']
    table_name = d['Name']
    columns = [c['Name'] for c in d['StorageDescriptor']['Columns']]

    line = f"{db_name}.{table_name} ({', '.join(columns)})"
    lines.append(line)

    return "\n".join(lines)