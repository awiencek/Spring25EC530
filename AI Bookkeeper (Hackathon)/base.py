import pandas as pd
import sqlite3

# Step 1: Load CSV and inspect data
def load_csv(csv_file):
    """Load CSV into pandas DataFrame."""
    return pd.read_csv(csv_file)

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

# Step 3: Create a table dynamically in SQLite
def create_table_from_csv(csv_file, table_name, db_name):
    """Create a table in SQLite based on CSV schema."""
    # Load CSV into DataFrame
    df = load_csv(csv_file)
    
    # Build CREATE TABLE SQL statement
    columns = df.columns
    column_definitions = []
    
    for column in columns:
        # Get the pandas dtype and map it to SQLite type
        column_type = map_data_type(df[column].dtype)
        column_definition = f"{column} {column_type}"
        column_definitions.append(column_definition)
    
    # Create the SQL query for table creation
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (\n" + \
                         ",\n".join(column_definitions) + "\n);"
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Execute the CREATE TABLE query
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()
    print(f"Table '{table_name}' created successfully in '{db_name}'.")

# Step 4: Insert Data into SQLite Table
def insert_data_into_table(csv_file, table_name, db_name):
    """Insert CSV data into the specified SQLite table."""
    df = load_csv(csv_file)
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    
    # Insert the data from DataFrame to SQL table
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    print(f"Data from '{csv_file}' inserted into '{table_name}'.")

# Example Usage: Combine both steps
def main():
    csv_file = 'users.csv'
    table_name = 'users'
    db_name = 'example.db'
    
    # Step 1 & Step 2: Create the table based on CSV schema
    create_table_from_csv(csv_file, table_name, db_name)
    
    # Step 3: Insert the data into the table
    insert_data_into_table(csv_file, table_name, db_name)

# Run the combined process
if __name__ == '__main__':
    main()
