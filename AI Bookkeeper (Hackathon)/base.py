import pandas as pd
import sqlite3
import os
import logging

# Step 1: Load CSV and inspect data
def load_csv(csv_file):
    """Load CSV into pandas DataFrame."""
    try:
        return pd.read_csv(csv_file)
    except Exception as e:
        log_error(f"Error loading CSV file {csv_file}: {str(e)}")
        raise

# Step 2: Map pandas data types to SQLite data types
def map_data_type(pandas_dtype):
    """Map pandas data type to SQLite data type."""
    if pandas_dtype == 'object':
        return 'TEXT'
    elif pandas_dtype == 'int64':
        return 'INTEGER'
    elif pandas_dtype == 'float64':
        return 'REAL'
    else:
        return 'TEXT'  # Default to TEXT for any other types

# Step 3: Create table if it doesn't exist, otherwise handle schema conflict
def create_table_from_csv(csv_file, table_name, db_name):
    """Create or handle schema conflict when creating a table."""
    # Load CSV into DataFrame
    df = load_csv(csv_file)

    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute(f"PRAGMA table_info({table_name});")
    existing_columns = cursor.fetchall()

    if existing_columns:
        # Table exists, handle conflict
        print(f"Table '{table_name}' already exists.")
        action = prompt_user_for_conflict_resolution()

        if action == 'overwrite':
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            conn.commit()
            print(f"Table '{table_name}' has been dropped and will be recreated.")
        elif action == 'rename':
            new_table_name = f"{table_name}_1"  # You can add a more complex renaming logic
            print(f"Renaming table to '{new_table_name}'.")
            table_name = new_table_name
        elif action == 'skip':
            print(f"Skipping table creation for '{table_name}'.")
            conn.close()
            return
        else:
            print("Invalid action. Skipping operation.")
            conn.close()
            return

    # Build CREATE TABLE SQL statement
    columns = df.columns
    column_definitions = []
    
    for column in columns:
        column_type = map_data_type(df[column].dtype)
        column_definition = f"{column} {column_type}"
        column_definitions.append(column_definition)
    
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (\n" + \
                         ",\n".join(column_definitions) + "\n);"
    
    # Execute the CREATE TABLE query
    try:
        cursor.execute(create_table_query)
        conn.commit()
        print(f"Table '{table_name}' created successfully in '{db_name}'.")
    except Exception as e:
        log_error(f"Error creating table '{table_name}': {str(e)}")
        print(f"Error occurred while creating table '{table_name}'. Check error_log.txt.")
    
    conn.close()

# Step 4: Insert Data into SQLite Table
def insert_data_into_table(csv_file, table_name, db_name):
    """Insert CSV data into the specified SQLite table."""
    df = load_csv(csv_file)

    # Connect to SQLite database
    conn = sqlite3.connect(db_name)

    try:
        # Insert the data from DataFrame to SQL table
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.commit()
        print(f"Data from '{csv_file}' inserted into '{table_name}'.")
    except Exception as e:
        log_error(f"Error inserting data into table '{table_name}': {str(e)}")
        print(f"Error occurred while inserting data. Check error_log.txt.")
    finally:
        conn.close()

# Prompt the user for action on schema conflict
def prompt_user_for_conflict_resolution():
    """Prompt the user to resolve schema conflict (overwrite, rename, skip)."""
    while True:
        action = input("Table already exists. Choose an action: 'overwrite', 'rename', or 'skip': ").strip().lower()
        if action in ['overwrite', 'rename', 'skip']:
            return action
        else:
            print("Invalid choice. Please choose 'overwrite', 'rename', or 'skip'.")

# Error logging function
def log_error(message):
    """Log errors to a file (error_log.txt)."""
    logging.basicConfig(filename='error_log.txt', level=logging.ERROR, 
                        format='%(asctime)s - %(message)s')
    logging.error(message)

# Example Usage: Combine both steps
def main():
    csv_file = 'users.csv'
    table_name = 'users'
    db_name = 'example.db'

    # Step 1 & Step 2: Create or handle table creation based on CSV schema
    create_table_from_csv(csv_file, table_name, db_name)

    # Step 3: Insert the data into the table
    insert_data_into_table(csv_file, table_name, db_name)

# Run the combined process
if __name__ == '__main__':
    main()
