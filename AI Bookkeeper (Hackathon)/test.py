import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import pandas as pd
import openai
import os
import logging

# Assuming the above code is in a module named 'sqlite_assistant'
import sqlite_assistant

class TestSQLiteAssistant(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_create_table_from_csv(self, mock_connect):
        """Test the creation of a table from CSV data."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        table_name = 'test_table'
        db_name = 'test.db'
        
        # Mocking the CSV data
        csv_data = pd.DataFrame({
            'id': [1, 2],
            'name': ['Alice', 'Bob']
        })
        
        # Mock load_csv to return our mock DataFrame
        with patch.object(sqlite_assistant, 'load_csv', return_value=csv_data):
            sqlite_assistant.create_table_from_csv('test.csv', table_name, db_name)
        
        # Check that the correct SQL statement is called to create the table
        mock_conn.cursor().execute.assert_called_with(
            f"CREATE TABLE IF NOT EXISTS {table_name} (\n" +
            "id INTEGER,\n" +
            "name TEXT\n);"
        )
        
        # Verify that the insert data method is called
        sqlite_assistant.insert_data_into_table.assert_called_with(csv_data, table_name, mock_conn)

    @patch('sqlite3.connect')
    def test_run_sql_query(self, mock_connect):
        """Test the execution of an arbitrary SQL query."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        query = 'SELECT * FROM test_table'
        db_name = 'test.db'

        # Mock the return value for the query
        mock_conn.cursor().fetchall.return_value = [(1, 'Alice'), (2, 'Bob')]
        
        result = sqlite_assistant.run_sql_query(query, db_name)
        
        # Ensure the SQL query was executed
        mock_conn.cursor().execute.assert_called_with(query)
        
        # Verify the result
        self.assertEqual(result, [(1, 'Alice'), (2, 'Bob')])

    @patch('openai.Completion.create')
    def test_generate_sql_with_llm(self, mock_openai):
        """Test generating SQL with the OpenAI API."""
        request = "Show all records where name is 'Alice'"
        table_schema = "id (type: INTEGER), name (type: TEXT)"
        
        # Mock OpenAI's response
        mock_openai.return_value = MagicMock(choices=[MagicMock(text="SELECT * FROM test_table WHERE name = 'Alice'")])
        
        generated_sql = sqlite_assistant.generate_sql_with_llm(request, table_schema)
        
        # Check that OpenAI's API was called with the correct prompt
        mock_openai.assert_called_with(
            engine="gpt-4",
            prompt=f"Given the following table schema:\n{table_schema}\n\n" +
                   f"Generate an SQL query for the following request:\n{request}\n\nSQL Query:",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5
        )
        
        # Check that the correct SQL query was generated
        self.assertEqual(generated_sql, "SELECT * FROM test_table WHERE name = 'Alice'")

    @patch('sqlite3.connect')
    def test_list_tables(self, mock_connect):
        """Test listing tables from a database."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        db_name = 'test.db'
        
        # Mock the result of the SQL query to list tables
        mock_conn.cursor().fetchall.return_value = [('table1',), ('table2',)]
        
        result = sqlite_assistant.list_tables(db_name)
        
        # Ensure that the SQL query was executed to list tables
        mock_conn.cursor().execute.assert_called_with("SELECT name FROM sqlite_master WHERE type='table';")
        
        # Verify the list of tables returned
        self.assertEqual(result, ['table1', 'table2'])

    @patch('sqlite3.connect')
    def test_insert_data_into_table(self, mock_connect):
        """Test inserting data into the SQLite table."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        df = pd.DataFrame({
            'id': [1, 2],
            'name': ['Alice', 'Bob']
        })
        table_name = 'test_table'

        # Call insert_data_into_table to test
        sqlite_assistant.insert_data_into_table(df, table_name, mock_conn)
        
        # Check that to_sql was called to insert the data
        mock_conn.cursor().execute.assert_called_with('BEGIN')
        mock_conn.commit.assert_called_once()
        self.assertTrue(mock_conn.cursor().call_count > 0)

if __name__ == '__main__':
    unittest.main()
