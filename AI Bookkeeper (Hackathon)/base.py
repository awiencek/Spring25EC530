import sqlite3
import pandas as pd
import os
import logging
import openai

# Setup logging configuration
def setup_logging():
    """Set up the logging configuration."""
    logging.basicConfig(filename='error_log.txt', level=logging.ERROR, 
                        format='%(asctime)s - %(message)s')

# Function to log errors
def log_error(message):
    """Log errors to a file (error_log.txt)."""
    logging.error(message)

# Function to load CSV into pandas DataFrame
def load_csv(csv_file):
    """Load CSV into pandas DataFrame."""
    try:
        return pd.read_csv(csv_file)
    except Exception as e:
        log_error(f"Error loading CSV file {csv_file}: {str(e)}")
        print(f"Error loading CSV file {csv_file}: {str(e)}")
        return None

# Function to map pandas data types to SQLite data types
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

# Function to create table based on CSV schema
def create_table_from_csv(csv_file, table_name, db_name):
    """Create or handle schema conflict when creating a table."""
    df = load_csv(csv_file)
    if df is None:
        return

    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute(f"PRAGMA table_info({table_name});")
    existing_columns = cursor.fetchall()

    if existing_columns:
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

    try:
        cursor.execute(create_table_query)
        conn.commit()
        print(f"Table '{table_name}' created successfully in '{db_name}'.")
    except Exception as e:
        log_error(f"Error creating table '{table_name}': {str(e)}")
        print(f"Error creating table '{table_name}': {str(e)}")

    # Insert the data into the table
    insert_data_into_table(df, table_name, conn)

    conn.close()

# Function to insert DataFrame data into SQLite table
def insert_data_into_table(df, table_name, conn):
    """Insert DataFrame data into SQLite table."""
    try:
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.commit()
        print(f"Data from CSV inserted into table '{table_name}'.")
    except Exception as e:
        log_error(f"Error inserting data into table '{table_name}': {str(e)}")
        print(f"Error inserting data into table '{table_name}': {str(e)}")

# Function to run an arbitrary SQL query
def run_sql_query(query, db_name):
    """Execute a user-provided SQL query."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        log_error(f"Error executing SQL query: {str(e)}")
        print(f"Error executing SQL query: {str(e)}")
        return None

# Function to list all tables in the database
def list_tables(db_name):
    """List all tables in the database."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        return [table[0] for table in tables]
    except sqlite3.Error as e:
        log_error(f"Error retrieving tables: {str(e)}")
        print(f"Error retrieving tables: {str(e)}")
        return []

# Function to prompt the user for action on schema conflict
def prompt_user_for_conflict_resolution():
    """Prompt the user to resolve schema conflict (overwrite, rename, skip)."""
    while True:
        action = input("Table already exists. Choose an action: 'overwrite', 'rename', or 'skip': ").strip().lower()
        if action in ['overwrite', 'rename', 'skip']:
            return action
        else:
            print("Invalid choice. Please choose 'overwrite', 'rename', or 'skip'.")

# Function to interact with OpenAI's GPT model to generate SQL from plain language
def generate_sql_with_llm(request, table_schema):
    """Generate SQL query using OpenAI's language model."""
    openai.api_key = 'your-openai-api-key-here'  # Replace with your OpenAI API key

    # Prepare the prompt for ChatGPT
    prompt = f"Given the following table schema:\n{table_schema}\n\n" \
             f"Generate an SQL query for the following request:\n{request}\n\n" \
             f"SQL Query:"

    try:
        # Call OpenAI API to get the generated SQL
        response = openai.Completion.create(
            engine="gpt-4",  # Or use any model you prefer, like 'gpt-3.5-turbo'
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5
        )
        generated_sql = response.choices[0].text.strip()
        return generated_sql
    except Exception as e:
        log_error(f"Error with OpenAI API: {str(e)}")
        print(f"Error with OpenAI API: {str(e)}")
        return None

# Function for interactive chat-like assistant
def interactive_assistant():
    """Run the interactive chat-like assistant."""
    db_name = 'example.db'

    while True:
        print("\nWelcome to the SQLite Assistant! What would you like to do?")
        print("1. Load CSV file into SQLite")
        print("2. Run SQL query")
        print("3. List tables in the database")
        print("4. Generate SQL via ChatGPT")
        print("5. Exit")

        choice = input("Enter your choice (1, 2, 3, 4, or 5): ").strip()

        if choice == '1':
            csv_file = input("Enter the CSV file path to load: ").strip()
            table_name = input("Enter the name of the table: ").strip()
            create_table_from_csv(csv_file, table_name, db_name)

        elif choice == '2':
            query = input("Enter the SQL query to run: ").strip()
            result = run_sql_query(query, db_name)
            if result:
                print("Query result:")
                for row in result:
                    print(row)
            else:
                print("No results found or error occurred.")

        elif choice == '3':
            tables = list_tables(db_name)
            if tables:
                print("Tables in the database:")
                for table in tables:
                    print(table)
            else:
                print("No tables found in the database.")

        elif choice == '4':
            request = input("Enter your request in plain language (e.g., 'Show me all records where price > 100'): ").strip()
            tables = list_tables(db_name)
            if tables:
                # Assuming we pick the first table from the list to build the schema
                table_name = tables[0]  # You could prompt the user for the table if necessary
                df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 1", sqlite3.connect(db_name))
                table_schema = df.columns.tolist()
                table_schema_str = ', '.join([f"{col} (type: {map_data_type(df[col].dtype)})" for col in table_schema])

                # Call the LLM to generate SQL based on the plain language request
                generated_sql = generate_sql_with_llm(request, table_schema_str)
                if generated_sql:
                    print(f"Generated SQL Query: {generated_sql}")
                    result = run_sql_query(generated_sql, db_name)
                    if result:
                        print("Query result:")
                        for row in result:
                            print(row)
                    else:
                        print("No results found or error occurred.")
                else:
                    print("Failed to generate SQL query.")

        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

# Run the interactive assistant
if __name__ == '__main__':
    setup_logging()  # Initialize logging setup
    interactive_assistant()

