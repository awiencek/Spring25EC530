import sqlite3
import pandas as pd

# Step 1: Load CSV into pandas DataFrame
df = pd.read_csv('users.csv')

# Step 2: Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect('example.db')

# Step 3: Insert data from DataFrame to SQLite table
df.to_sql('users', conn, if_exists='replace', index=False)

# Step 4: Query the database
cursor = conn.cursor()

# Run a SELECT query
cursor.execute("SELECT * FROM users")
print("All Users:")
print(cursor.fetchall())

# Run a WHERE query
cursor.execute("SELECT * FROM users WHERE age > 30")
print("\nUsers older than 30:")
print(cursor.fetchall())

# Run a LIMIT query
cursor.execute("SELECT * FROM users LIMIT 2")
print("\nFirst 2 users:")
print(cursor.fetchall())

# Close the connection
conn.close()
