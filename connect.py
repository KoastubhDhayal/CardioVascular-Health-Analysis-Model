import pandas as pd
import mysql.connector
from mysql.connector import Error

config = {
    'user': 'root',
    'password': 'vaish',
    'host': '127.0.0.1',
    'database': 'sleepData',
}

csv_file_path = r'C:\Users\Vaishnavi\OneDrive\Desktop\sem 5\de\DE_MiniProject\data_updated.csv'

database_name = 'sleepData'
table_name = 'Cardio'

def create_database_if_not_exists(cursor, database_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    cursor.execute(f"USE {database_name}")

def create_table_if_not_exists(cursor, table_name, df):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    column_definitions = ', '.join([
        f"`{col.replace(' ', '_')}` VARCHAR(255)" for col in df.columns
    ])
    
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        User_Id INT AUTO_INCREMENT PRIMARY KEY,
        {column_definitions}
    )
    """
    print("Create table query:", create_table_query)
    cursor.execute(create_table_query)

def import_csv_to_mysql(csv_file_path, table_name, db_config):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Successfully connected to MySQL server")

            cursor = connection.cursor()

            create_database_if_not_exists(cursor, database_name)

            df = pd.read_csv(csv_file_path)

            create_table_if_not_exists(cursor, table_name, df)

            placeholders = ', '.join(['%s'] * len(df.columns))
            insert_query = f"""
            INSERT INTO {table_name} ({', '.join([f'`{col.replace(" ", "_")}`' for col in df.columns])})
            VALUES ({placeholders})
            """
            print("Insert query:", insert_query)

            data_tuples = [tuple(row) for row in df.to_numpy()]

            cursor.executemany(insert_query, data_tuples)

            connection.commit()
            print("Data imported successfully")

    except Error as e:
        print(f"Error: {e}")


import_csv_to_mysql(csv_file_path, table_name, config)

