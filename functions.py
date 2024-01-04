import tkinter as tk
import sqlite3
from datetime import datetime


def create_database():
    print("New SQLite database created with transactions table.")  # Testing

    # Connect to SQLite database (it will create the database file if it doesn't exist)
    conn = sqlite3.connect('transactions.db')

    # Create a table to store categorized transactions
    with conn:
        cursor = conn.cursor()

        # Create transactions table with columns for transaction details
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL
            )
            """)

    # Commit the changes and close the connection
    conn.commit()
    # conn.close()


def handle_view_button(gui):
    """Take user to the view/edit screen to interact with existing budget"""
    print("Edit button clicked")  # here for testing
    gui.geometry("700x500")

    # Destroy existing widgets in the window
    for widget in gui.winfo_children():
        widget.destroy()

    # Create page description
    edit_page_label = tk.Label(gui, text="Add/edit transactions and generate reports.")
    edit_page_label.pack()  # Place the label below the Edit button

    # Create a frame for placing widgets side by side
    top_frame = tk.Frame(gui)
    top_frame.pack(pady=50)  # Add some padding

    # Create a dropdown menu for transaction types and place it in the top frame
    options = ['Car Repair/Maintenance', 'Discretionary', 'Gas', 'Groceries', 'Healthcare', 'Home Repair/Maintenance',
               'Restaurants']
    variable = tk.StringVar(gui)
    variable.set(options[0])  # Set the default option

    dropdown_menu = tk.OptionMenu(top_frame, variable, *options)
    dropdown_menu.pack(side=tk.LEFT, padx=10)  # Add padding

    # Create an Entry widget for entering the transaction amount
    amount_entry_label = tk.Label(top_frame, text="Amount:  $")
    amount_entry_label.pack(side=tk.LEFT)  # Add padding

    amount_entry = tk.Entry(top_frame)
    amount_entry.pack(side=tk.LEFT)  # Add padding

    # Create a frame for placing the 'Edit Transactions' button beneath the top frame
    mid_frame = tk.Frame(gui)
    mid_frame.pack(pady=20)  # Add some padding

    # Create Edit Transactions button and place it in the bottom frame
    edit_transaction_button = tk.Button(mid_frame, text="Edit Transactions")
    edit_transaction_button.pack()  # Place the button in the mid frame

    # Create a frame for placing the 'Visualize Finances' button beneath the mid frame
    bottom_frame = tk.Frame(gui)
    bottom_frame.pack(pady=20)  # Add some padding

    # Create Visualize Finances button and place it in the bottom frame
    visualize_finances_button = tk.Button(bottom_frame, text="Visualize Finances")
    visualize_finances_button.pack()  # Place the button in the bottom frame

    def add_transaction_click():
        selected_category = variable.get()  # Get selected category from dropdown menu
        transaction_amount = float(amount_entry.get())  # Get transaction amount from entry box
        add_transaction_to_database(selected_category, transaction_amount)  # Add transaction to database

        # Clear the entry box after adding the transaction (optional)
        amount_entry.delete(0, tk.END)

    # Attach the 'Add Transaction' function to the button click event
    add_transaction_button = tk.Button(top_frame, text="Add Transaction", command=add_transaction_click)
    add_transaction_button.pack(side=tk.LEFT, padx=2)  # Add padding

    # Create 'View Transactions' button
    view_transactions_button = tk.Button(gui, text="View Transactions", command=view_transactions_from_database)
    view_transactions_button.pack(pady=20)  # Place the button beneath the top frame


def add_transaction_to_database(category, amount):
    """Add transaction to SQLite database with current date"""
    # Connect to SQLite database
    conn = sqlite3.connect('transactions.db')

    with conn:
        cursor = conn.cursor()

        # Get the current date in YYYY-MM-DD format
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Insert the transaction into the database
        cursor.execute("""
        INSERT INTO transactions (category, amount, date)
        VALUES (?, ?, ?)
        """, (category, amount, current_date))

        # Commit the changes
        conn.commit()

# For testing (remove when done)
def view_transactions_from_database():
    """Fetch and display transactions from SQLite database"""
    # Connect to SQLite database
    conn = sqlite3.connect('transactions.db')

    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        rows = cursor.fetchall()

        print("\nTransactions:")
        for row in rows:
            print(row)
