# SQLite Assistant with Chat Interaction
This project provides a chat-based interface for interacting with SQLite databases, using AI to assist with SQL query generation and interaction. It leverages SQLite for database management, OpenAI for natural language processing, and Pandas for handling data manipulation and loading CSV files.

## Key Features:
- Load CSV files into SQLite databases.
- Dynamically create tables from CSV data.
- Handle schema conflicts (overwrite, rename, or skip).
- Use OpenAI to generate SQL queries from natural language input.
- Run and display SQL query results in a simple UI.

## Prerequisites
Make sure you have the following installed:

Python 3.x

SQLite (SQLite is embedded in Python, so it's already included with Python installations)

OpenAI API Key (Required to use OpenAI's language models)

#### To install the required Python libraries, run the following:
pip install sqlite3 pandas openai tk

## Overview of Components
1. SQLite Assistant
- The core of the application interacts with SQLite databases.

- It supports loading CSV files, creating tables, inserting data, and running SQL queries.

- It also supports generating SQL queries based on plain language input using OpenAI's language models.

2. AI-Powered SQL Generation
- OpenAI powers the ability to generate SQL queries using plain language.

- The user can input natural language requests, such as "Show all records where price > 100," and the AI will generate the corresponding SQL query.

3. Graphical User Interface (GUI)
- Built with Tkinter, the UI offers buttons for various actions like loading CSV files, running SQL queries, and generating SQL via ChatGPT.

- The UI also allows users to customize the color theme for a personalized experience.

4. Unit Testing
- Unit tests have been written to ensure the core functionality of the SQLite Assistant (e.g., creating tables from CSV, running SQL queries, generating SQL with AI).

## Getting Started
Step 1: Load CSV Files into SQLite
The user can select a CSV file, which is then loaded into SQLite. The application automatically creates a table based on the CSV schema.

Step 2: Create Tables Dynamically from CSV
When a CSV is loaded, a table is created dynamically in the SQLite database using the column names and data types from the CSV.

Step 3: Handle Schema Conflicts
If a table already exists with the same name, the user is prompted to either overwrite, rename, or skip creating the new table.

Step 4: Simulate AI using Input
The application simulates AI using the schema of a selected table. This schema is provided as input to OpenAI's API to generate SQL queries.

Step 5: Generate SQL via ChatGPT
The AI listens to natural language queries, converts them into SQL statements, and automatically executes them to retrieve results.

## Project Structure
The project consists of the following files:

sqlite_assistant.py
Contains the core functionality for interacting with SQLite databases (e.g., creating tables, inserting data, running queries, etc.).

sqlite_assistant_test.py
Contains unit tests for the core functions of the SQLite Assistant, ensuring the system works correctly.

sqlite_assistant_ui.py
Contains the Tkinter-based UI for interacting with the SQLite database, running SQL queries, and generating SQL with ChatGPT.

readme.md
This file! It contains the project overview and instructions.

## Usage
Running the Application
Clone the repository or download the files.

Ensure you have all the required dependencies installed.

Run the sqlite_assistant_ui.py file to launch the application.

bash
Copy
python sqlite_assistant_ui.py
Key Features in the UI:
Load CSV: Allows you to load a CSV file into the SQLite database.

Run SQL Query: Input a SQL query to execute on the SQLite database.

List Tables: Lists all tables in the database.

Generate SQL via ChatGPT: Use natural language to generate SQL queries using OpenAI's API.

Set Color Theme: Personalize the UI by setting your own color theme with up to three hex color codes.

Unit Tests
Unit tests are written using the unittest framework. To run the tests:

Ensure that the necessary libraries (unittest, sqlite3, pandas, openai) are installed.

Run the test suite with the following command:
python -m unittest sqlite_assistant_test.py

This will verify the core functionality, including:

Loading CSV files and creating tables.

Running SQL queries.

Generating SQL queries using OpenAI.

#### Enhancements and Future Improvements
AI-Based Query Optimization: In addition to generating queries, AI can be used to suggest query optimizations or recommend indexes based on the data.

Improved UI Features: Add more customization options for the UI, such as font sizes and layouts.

Support for More Database Types: Expand the assistant to support databases other than SQLite, such as MySQL or PostgreSQL.

Better Error Handling: Enhance error handling to display more user-friendly messages and provide debugging information.

## Conclusion
This project provides a powerful and interactive assistant for working with SQLite databases, enhanced by the power of OpenAI for natural language query generation. It combines database management, data analysis, and AI to create a seamless user experience.

Feel free to contribute to the project or suggest improvements!

## License
This project is licensed under the MIT License - see the LICENSE file for details.
