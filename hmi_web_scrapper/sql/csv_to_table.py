import csv
import json
import pyodbc
import configparser

# Read database configuration
config = configparser.ConfigParser()
config.read('config.ini')

host = config['sql']['host']
database = config['sql']['database']
user = config['sql']['user']
password = config['sql']['password']

# Construct the connection string
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={host};DATABASE={database};UID={user};PWD={password}'

# The column to be set as the primary key
primary_key = 'E28.SerialNumber'

def main():
    data = csv_to_json_dict(r'data\05231527.CSV')
    json_to_sql(data)


def create_column_dict(name, primary):
    column = {
        "name": name,
        "type": "bit",
        "length": 1,
        "nullable": False,
        "default": 1,
        "unique": False,
        "primary_key": False,
        "auto_increment": False,
        "foreign_key": None
    }

    # Dynamically determine the column info
    if 'MeasuredVoltage' in name or 'MinimumValue' in name or 'MaximumValue' in name:
        column.update({
            "type": "float",
            "length": None,
            "nullable": False,
            "default": None
        })
    elif 'Date' in name:
        column.update({
            "type": "datetime",
            "length": None,
            "nullable": False,
            "default": None
        })
    elif 'MeasurementUnit' in name or 'E28.EmployeeNumber' in name or 'E28.SerialNumber' in name or 'E28.YorkPN' in name:
        column.update({
            "type": "string",
            "length": 50,
            "nullable": False,
            "default": None
        })
    
    if primary:
        column['primary_key'] = True

    return column

def csv_to_json_dict(csv_filepath):
    with open(csv_filepath, 'r') as csv_file:
        reader = csv.reader(csv_file)
        columns = next(reader)

        data = {
            "table_name": "E28",
            "columns": [create_column_dict(name, name==primary_key) for name in columns]
        }

        # with open(r'data\output.json', 'w') as json_file:
        #     json.dump(data, json_file, indent=2)

        return data


def json_to_sql(json_data):

        table_name = json_data['table_name']
        columns = json_data['columns']

        # Generate SQL
        column_defs = []
        for column in columns:

            if column['name'] == "Time":
                continue

            if column['name'] == "Date":
                column_def = "Timestamp "
            else:
                column_def = f"[{column['name']}] "
            if column['type'] == 'string':
                column_def += f"VARCHAR({column['length']})"
            elif column['type'] == 'integer':
                column_def += 'INTEGER'
            elif column['type'] == 'datetime':
                column_def += 'DATETIME'
            elif column['type'] == 'float':
                column_def += 'FLOAT'
            elif column['type'] == 'bit':
                column_def += 'BIT'
            if column['primary_key']:
                column_def += ' PRIMARY KEY'
            elif column['unique']:
                column_def += ' UNIQUE'
            if not column['nullable']:
                column_def += ' NOT NULL'
            if column['auto_increment']:
                column_def += ' AUTO_INCREMENT'
            if column['default'] is not None:
                column_def += f" DEFAULT {column['default']}"
            column_defs.append(column_def)

        sql = "CREATE TABLE " + table_name + " (\n" + ',\n'.join(column_defs) + "\n);"

        print(f"Executing SQL:\n{sql}")

        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Execute SQL
        cursor.execute(sql)

        # Commit changes and close connection
        conn.commit()
        conn.close()


if __name__ == "__main__":
    main()