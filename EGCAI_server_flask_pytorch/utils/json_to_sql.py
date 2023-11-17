import json


def generate_insert_statements(table_name, data_entries):
    if not data_entries:
        return None
    base_statement = f"INSERT INTO {table_name} ({', '.join(data_entries.keys())}) VALUES "
    value_statements = []
    for entry in data_entries:
        values = [str(entry[key]) if isinstance(entry[key], int)
                  else f"'{entry[key]}'" for key in entry.keys()]
        value_statements.append(f"({', '.join(values)})")

    return base_statement + ",\n".join(value_statements) + ";"


def json_path_to_sql(json_path, output_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    sql_file = []
    for table in data.keys():
        sql_file.append(generate_insert_statements(
            str(table), data[str(table)]))
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("\n\n".join(sql_file))


def json_to_sql(data):
    sql_data = []
    for table in data.keys():
        sql_data.append(generate_insert_statements(
            str(table), data[str(table)]))
    return "\n".join(sql_data)
