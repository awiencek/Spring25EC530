import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import pandas as pd
import os
import sqlite_assistant  # Assuming your code is in the sqlite_assistant.py module


class SQLiteAssistantUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite Assistant")

        # Database name
        self.db_name = 'example.db'

        # Default colors (if no user input)
        self.default_bg_color = '#f0f0f0'
        self.default_button_color = '#4CAF50'
        self.default_text_color = '#000000'

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Label for instructions
        self.instructions_label = tk.Label(self.root, text="Select an action:")
        self.instructions_label.grid(row=0, column=0, padx=10, pady=10)

        # Buttons for various actions
        self.load_csv_button = tk.Button(self.root, text="Load CSV", command=self.load_csv)
        self.load_csv_button.grid(row=1, column=0, padx=10, pady=10)

        self.run_query_button = tk.Button(self.root, text="Run SQL Query", command=self.run_sql_query)
        self.run_query_button.grid(row=2, column=0, padx=10, pady=10)

        self.list_tables_button = tk.Button(self.root, text="List Tables", command=self.list_tables)
        self.list_tables_button.grid(row=3, column=0, padx=10, pady=10)

        self.generate_sql_button = tk.Button(self.root, text="Generate SQL via ChatGPT", command=self.generate_sql)
        self.generate_sql_button.grid(row=4, column=0, padx=10, pady=10)

        # Add "Set Color Theme" button
        self.set_theme_button = tk.Button(self.root, text="Set Color Theme", command=self.set_color_theme)
        self.set_theme_button.grid(row=5, column=0, padx=10, pady=10)

        # Textbox for SQL Query input and results
        self.query_input_label = tk.Label(self.root, text="Enter SQL query:")
        self.query_input_label.grid(row=6, column=0, padx=10, pady=5)

        self.query_input_text = tk.Text(self.root, height=4, width=50)
        self.query_input_text.grid(row=7, column=0, padx=10, pady=5)

        self.result_label = tk.Label(self.root, text="Query Result:")
        self.result_label.grid(row=8, column=0, padx=10, pady=5)

        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.grid(row=9, column=0, padx=10, pady=10)

    def set_color_theme(self):
        """Allow the user to set a custom color theme using up to 3 hex codes."""
        # Get user input for color codes (1 to 3)
        color_input = simpledialog.askstring(
            "Input", "Enter up to 3 hex color codes (e.g., #RRGGBB, #RRGGBB, #RRGGBB):"
        )
        if not color_input:
            return

        # Split the input and clean up the list
        color_codes = [color.strip() for color in color_input.split(',') if color.strip()]
        
        # Validate that the user provided between 1 and 3 valid hex color codes
        if len(color_codes) < 1 or len(color_codes) > 3:
            messagebox.showerror("Invalid Input", "Please enter between 1 and 3 hex color codes.")
            return
        
        # Check if each color code is valid
        for color in color_codes:
            if not color.startswith('#') or len(color) != 7 or not all(c in '0123456789ABCDEFabcdef' for c in color[1:]):
                messagebox.showerror("Invalid Input", f"Invalid color code: {color}")
                return

        # Apply the colors to the UI
        if len(color_codes) >= 1:
            self.default_bg_color = color_codes[0]
        if len(color_codes) >= 2:
            self.default_button_color = color_codes[1]
        if len(color_codes) >= 3:
            self.default_text_color = color_codes[2]

        # Update UI components with the new colors
        self.apply_color_theme()

        messagebox.showinfo("Success", "Color theme applied successfully!")

    def apply_color_theme(self):
        """Apply the current color theme to the UI."""
        # Update the background color of the window
        self.root.configure(bg=self.default_bg_color)

        # Apply color changes to widgets
        self.instructions_label.configure(bg=self.default_bg_color, fg=self.default_text_color)
        self.query_input_label.configure(bg=self.default_bg_color, fg=self.default_text_color)
        self.result_label.configure(bg=self.default_bg_color, fg=self.default_text_color)

        # Buttons
        self.load_csv_button.configure(bg=self.default_button_color, fg=self.default_text_color)
        self.run_query_button.configure(bg=self.default_button_color, fg=self.default_text_color)
        self.list_tables_button.configure(bg=self.default_button_color, fg=self.default_text_color)
        self.generate_sql_button.configure(bg=self.default_button_color, fg=self.default_text_color)
        self.set_theme_button.configure(bg=self.default_button_color, fg=self.default_text_color)

        # Textboxes (input and result)
        self.query_input_text.configure(bg=self.default_bg_color, fg=self.default_text_color)
        self.result_text.configure(bg=self.default_bg_color, fg=self.default_text_color)

    def load_csv(self):
        """Load CSV file into SQLite database."""
        csv_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not csv_file:
            return

        table_name = simpledialog.askstring("Input", "Enter table name:")
        if not table_name:
            return

        try:
            sqlite_assistant.create_table_from_csv(csv_file, table_name, self.db_name)
            messagebox.showinfo("Success", f"CSV file {csv_file} loaded into table '{table_name}'")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading CSV: {str(e)}")

    def run_sql_query(self):
        """Run SQL query and show result in the UI."""
        query = self.query_input_text.get("1.0", tk.END).strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a SQL query.")
            return

        try:
            result = sqlite_assistant.run_sql_query(query, self.db_name)
            self.display_result(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error running query: {str(e)}")

    def list_tables(self):
        """List all tables in the database."""
        try:
            tables = sqlite_assistant.list_tables(self.db_name)
            self.display_result(tables)
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving tables: {str(e)}")

    def generate_sql(self):
        """Generate SQL query using ChatGPT."""
        request = simpledialog.askstring("Input", "Enter your request (e.g., 'Show me all records where price > 100'):")
        if not request:
            return

        tables = sqlite_assistant.list_tables(self.db_name)
        if not tables:
            messagebox.showwarning("Error", "No tables found in the database.")
            return

        table_name = tables[0]  # You can expand this to allow user to choose a table
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 1", sqlite3.connect(self.db_name))
        table_schema = df.columns.tolist()
        table_schema_str = ', '.join([f"{col} (type: {sqlite_assistant.map_data_type(df[col].dtype)})" for col in table_schema])

        generated_sql = sqlite_assistant.generate_sql_with_llm(request, table_schema_str)
        if generated_sql:
            self.query_input_text.delete("1.0", tk.END)
            self.query_input_text.insert(tk.END, generated_sql)
            self.run_sql_query()  # Automatically run the generated query
        else:
            messagebox.showerror("Error", "Failed to generate SQL query.")

    def display_result(self, result):
        """Display query result in the result textbox."""
        self.result_text.delete("1.0", tk.END)
        if isinstance(result, list):
            for row in result:
                self.result_text.insert(tk.END, str(row) + "\n")
        else:
            self.result_text.insert(tk.END, "No result or query failed.")

# Run the Tkinter UI
if __name__ == "__main__":
    import tkinter.simpledialog as simpledialog

    root = tk.Tk()
    ui = SQLiteAssistantUI(root)
    root.mainloop()
