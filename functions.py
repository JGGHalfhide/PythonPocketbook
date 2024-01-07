import tkinter as tk
import sqlite3
from datetime import datetime
import tkinter.messagebox as messagebox


def create_database():
    """Create a database when the 'new' button is clicked"""
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
    """Take user to the view/edit screen to interact with existing budget and create widgets for it"""
    gui.geometry("700x500")

    # Destroy existing widgets in the window
    for widget in gui.winfo_children():
        widget.destroy()

    # Create page description
    edit_page_label = tk.Label(gui, text="Add, view, and edit transactions and generate reports.")
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

    # Attach the 'Add Transaction' function to the button click event
    add_transaction_button = tk.Button(top_frame, text="Add Transaction",
                                       command=lambda: add_transaction_click(variable, amount_entry))
    add_transaction_button.pack(side=tk.LEFT, padx=2)  # Add padding

    # Create a frame for placing the 'Edit Transactions' button beneath the top frame
    mid_frame = tk.Frame(gui)
    mid_frame.pack(pady=20)  # Add some padding

    # Create Edit Transactions button and place it in the bottom frame
    edit_transaction_button = tk.Button(mid_frame, text="Edit Transactions", command=lambda: handle_edit_button(gui))
    edit_transaction_button.pack()  # Place the button in the mid-frame

    # Create a frame for placing the 'Visualize Finances' button beneath the mid-frame
    bottom_frame = tk.Frame(gui)
    bottom_frame.pack(pady=20)  # Add some padding

    # Create Visualize Finances button and place it in the bottom frame
    visualize_finances_button = tk.Button(bottom_frame, text="Visualize Finances")
    visualize_finances_button.pack()  # Place the button in the bottom frame

    # Create a frame for placing the 'Back' button
    back_frame = tk.Frame(gui)
    back_frame.pack(pady=20)  # Add some padding

    # Create 'Back' button and place it in the back frame
    back_button = tk.Button(back_frame, text="Back", command=lambda: back_to_home(gui))
    back_button.pack()  # Place the button in the bottom frame


def add_transaction_click(variable, amount_entry):
    """Listener for add transaction button to capture values"""
    selected_category = variable.get()  # Get selected category from dropdown menu
    transaction_amount = float(amount_entry.get())  # Get transaction amount from entry box
    add_transaction_to_database(selected_category, transaction_amount)  # Add transaction to database

    # Clear the entry box after adding the transaction (optional)
    amount_entry.delete(0, tk.END)


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

        # Show a message to inform the user
        tk.messagebox.showinfo("Success", "Transaction added successfully.")


def handle_edit_button(gui):
    """Take user to edit screen where they can view and edit transactions"""
    gui.geometry("700x500")

    # Destroy existing widgets
    for widget in gui.winfo_children():
        widget.destroy()

    # Create page description
    edit_page_label = tk.Label(gui, text="View/Edit transactions.")
    edit_page_label.pack()

    # Create frame for widgets
    top_frame = tk.Frame(gui)
    top_frame.pack(pady=20)

    # Function to fetch categories from SQLite database
    def fetch_categories_from_database():
        conn = sqlite3.connect('transactions.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM transactions")
            category = [row[0] for row in cursor.fetchall()]
        return category

    # Fetch categories from database
    categories = fetch_categories_from_database()

    # Dropdown for categories
    category_var = tk.StringVar(top_frame)
    category_var.set(categories[0])
    category_dropdown = tk.OptionMenu(top_frame, category_var, *categories)
    category_dropdown.pack(side=tk.LEFT, padx=10)

    # Select button
    select_button = tk.Button(top_frame, text="Select",
                              command=lambda: select_category(category_var, populate_transactions_listbox))
    select_button.pack(side=tk.LEFT)

    # Listbox for transactions
    transactions_listbox = tk.Listbox(width=50)
    transactions_listbox.pack(pady=20)

    # Frame to hold 'Edit' and 'Remove' buttons
    button_frame = tk.Frame(gui)
    button_frame.pack(pady=20)  # Add padding to position it below the Listbox

    # Dummy 'Edit' and 'Remove' buttons
    edit_button = tk.Button(button_frame, text="Edit", command=edit_transaction)
    edit_button.pack(side=tk.LEFT, padx=10)

    remove_button = tk.Button(button_frame, text="Remove", command=lambda: remove_transaction(transactions_listbox, category_var, populate_transactions_listbox))
    remove_button.pack(side=tk.LEFT, padx=10)

    # Hide the button frame initially
    button_frame.pack_forget()

    # Create a frame for placing the 'Back' button
    back_frame = tk.Frame(gui)
    back_frame.pack(pady=20)  # Add some padding

    # Create 'Back' button and place it in the back frame
    back_button = tk.Button(back_frame, text="Back", command=lambda: handle_view_button(gui))
    back_button.pack()  # Place the button in the bottom frame

    # Function to populate transactions based on category
    def populate_transactions_listbox(category):
        transactions_listbox.delete(0, tk.END)  # Clear previous items
        conn = sqlite3.connect('transactions.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT amount, date FROM transactions WHERE category=?", (category,))
            transactions = ["Amount: ${}, Date: {}".format(row[0], row[1]) for row in cursor.fetchall()]

        for transaction in transactions:
            transactions_listbox.insert(tk.END, transaction)

            # Bind function to handle selection in the Listbox
            transactions_listbox.bind('<<ListboxSelect>>', on_select)

    # Function to handle Listbox item selection
    def on_select(event):
        # Unhide the 'Edit' and 'Remove' buttons when an item is selected
        button_frame.pack(side=tk.TOP, pady=20)


# Function to handle user highlighted categories
def select_category(category_var, populate_transactions_listbox):
    selected_category = category_var.get()
    populate_transactions_listbox(selected_category)


# Dummy edit and remove functions (you can replace these with actual functionality)
def edit_transaction():
    print("Edit button clicked")


def remove_transaction(transactions_listbox, category_var, populate_func):
    # Get the selected transaction from the listbox
    selected_index = transactions_listbox.curselection()  # Get the index of the selected item
    if not selected_index:  # If no item is selected
        tk.messagebox.showerror("Error", "Please select a transaction to remove.")
        return

    # Extract amount and date details from the selected item
    selected_transaction = transactions_listbox.get(selected_index)
    amount = selected_transaction.split(",")[0].split(":")[1].strip()[1:]  # Extracting amount value
    date = selected_transaction.split(",")[1].split(":")[1].strip()  # Extracting date value

    # Connect to the SQLite database
    conn = sqlite3.connect('transactions.db')
    with conn:
        cursor = conn.cursor()

        # Execute SQL command to delete the transaction with the extracted amount and date
        cursor.execute("DELETE FROM transactions WHERE amount=? AND date=?", (amount, date))

        # Commit the changes
        conn.commit()

    # Show a message to inform the user
    tk.messagebox.showinfo("Success", "Transaction removed successfully.")

    # Refresh the transactions listbox
    populate_func(category_var.get())



def back_to_home_screen(gui):
    """Take user back to home screen"""
    # Destroy the current instance of the GUI
    gui.destroy()

    # Create the main application window
    gui = tk.Tk()
    # Set the GUI size
    gui.geometry("300x200")

    # Set the title of the window
    gui.title("Python Pocketbook")

    # Create the New button and pack it into the main window
    new_button = tk.Button(gui, text="New", command=create_database)
    new_button.pack(pady=20)  # Add some vertical padding

    # Create a label with descriptive text for the New button
    new_label = tk.Label(gui, text="Create new personal finance plan.")
    new_label.pack()  # Place the label below the New button

    # Create the Edit button and pack it into the main window
    edit_button = tk.Button(gui, text="View", command=lambda: handle_view_button(gui))
    edit_button.pack(pady=20)  # Add some vertical padding

    # Create a label with descriptive text for the Edit button
    edit_label = tk.Label(gui, text="View/Edit an existing plan.")
    edit_label.pack()  # Place the label below the Edit button

