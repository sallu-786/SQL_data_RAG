import sqlite3
import pandas as pd

def xlsx_to_sqlite(xlsx_file_path, sqlite_db_path, table_name):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(xlsx_file_path)

    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    # Create a table with the same columns as in the Excel file
    columns = df.columns
    columns_with_types = ", ".join([f"{col} TEXT" for col in columns])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types});"
    cursor.execute(create_table_query)

    # Insert DataFrame rows into the SQLite table
    for row in df.itertuples(index=False, name=None):
        placeholders = ", ".join(["?"] * len(row))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.execute(insert_query, row)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(f"Data from {xlsx_file_path} has been inserted into {table_name} table in {sqlite_db_path} database.")

# Example usage
csv_file_path = 'input_data/miibo_data.xlsx'
sqlite_db_path = 'input_data/database.db'
table_name = 'miibo_data'

xlsx_to_sqlite(csv_file_path, sqlite_db_path, table_name)
