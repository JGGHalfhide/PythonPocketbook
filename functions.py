import tkinter as tk
import sqlite3
from datetime import datetime
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


def create_database():
    """Create a database"""
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


def handle_view_button(gui):
    """Take user to the view/edit screen to interact with existing budget and create widgets for it"""
    gui.geometry("700x500")

    # Destroy existing widgets in the window
    for widget in gui.winfo_children():
        widget.destroy()

    # Create page description
    edit_page_label = tk.Label(gui, text="Add/view/edit transactions and generate reports.")
    edit_page_label.pack()  # Place the label below the Edit button

    # Create a frame for placing widgets side by side
    top_frame = tk.Frame(gui)
    top_frame.pack(pady=50)  # Add some padding

    # Create a dropdown menu for transaction types and place it in the top frame
    options = ['Entertainment', 'Food & Dining', 'Groceries', 'Health & Fitness', 'Housing', 'Miscellaneous', 'Shopping', 'Transportation',
               'Travel', 'Utilities']
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

    # Create Edit Transactions button and place it in the mid-frame
    edit_transaction_button = tk.Button(mid_frame, text="Edit Transactions", command=lambda: handle_edit_button(gui))
    edit_transaction_button.pack()  # Place the button in the mid-frame

    # Create a frame for placing the 'Visualize Finances' button beneath the mid-frame
    bottom_frame = tk.Frame(gui)
    bottom_frame.pack(pady=20)  # Add some padding

    # Create Visualize Finances button and place it in the bottom frame
    visualize_finances_button = tk.Button(bottom_frame, text="Visualize Finances", command=lambda: visualize_finances(gui))
    visualize_finances_button.pack()  # Place the button in the bottom frame

    # Create a frame for placing the 'Back' button
    back_frame = tk.Frame(gui)
    back_frame.pack(pady=20)  # Add some padding

    # Create 'Back' button and place it in the back frame
    back_button = tk.Button(back_frame, text="Back", command=lambda: back_to_home_screen(gui))
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
    view_trans_button = tk.Button(top_frame, text="View",
                                  command=lambda: select_category(category_var, populate_transactions_listbox))
    view_trans_button.pack(side=tk.LEFT)

    # Listbox for transactions
    transactions_listbox = tk.Listbox(width=50)
    transactions_listbox.pack(pady=20)

    # Frame to hold 'Edit' and 'Remove' buttons
    button_frame = tk.Frame(gui)
    button_frame.pack(pady=20)  # Add padding to position it below the Listbox

    # Create 'Edit' and 'Remove' buttons
    edit_button = tk.Button(button_frame, text="Edit",
                            command=lambda: edit_transaction(transactions_listbox, category_var,
                                                             populate_transactions_listbox))
    edit_button.pack(side=tk.LEFT, padx=10)

    remove_button = tk.Button(button_frame, text="Remove",
                              command=lambda: remove_transaction(transactions_listbox, category_var,
                                                                 populate_transactions_listbox))
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


def edit_transaction(transactions_listbox, category_var, populate_func):
    """Edit transaction in database and display updated results"""

    # Get the selected transaction from the listbox
    selected_index = transactions_listbox.curselection()  # Get the index of the selected item
    if not selected_index:  # If no item is selected
        tk.messagebox.showerror("Error", "Please select a transaction to edit.")
        return

    # Extract amount and date details from the selected item
    selected_transaction = transactions_listbox.get(selected_index)
    amount = selected_transaction.split(",")[0].split(":")[1].strip()[1:]  # Extracting amount value
    date = selected_transaction.split(",")[1].split(":")[1].strip()  # Extracting date value

    # Create a simple dialog to get the new amount from the user
    new_amount = tk.simpledialog.askfloat("Edit Transaction", "Enter the new amount:", initialvalue=float(amount))
    if new_amount is None:  # If the user cancels the dialog
        return

    # Connect to the SQLite database
    conn = sqlite3.connect('transactions.db')
    with conn:
        cursor = conn.cursor()

        # Update the amount in the database for the selected transaction
        cursor.execute("UPDATE transactions SET amount=? WHERE amount=? AND date=?", (new_amount, amount, date))

        # Commit the changes
        conn.commit()

    # Show a message to inform the user
    tk.messagebox.showinfo("Success", "Transaction updated successfully.")

    # Refresh the transactions listbox
    populate_func(category_var.get())


def remove_transaction(transactions_listbox, category_var, populate_func):
    """Remove transaction from database and display updated results"""
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
    # Configure window size and title
    gui.geometry("700x500")
    gui.title("Python Pocketbook")

    # Destroy existing widgets
    for widget in gui.winfo_children():
        widget.destroy()

    # Create a label with app description
    new_label = tk.Label(
        gui,
        text="Welcome to Python Pocketbook! Manage your finances effortlessly by entering, editing, and visualizing "
             "your transactions. Your financial journey starts here.",
        wraplength=600
    )
    new_label.pack(pady=20)  # Add vertical padding at the top

    # Load and resize the image using Pillow
    image_path = "/Users/jonathan/PycharmProjects/PythonPocketbook/venv/images/wallet-svgrepo-com.png"
    image = Image.open(image_path)
    image = image.resize((200, 200), Image.ANTIALIAS if hasattr(Image, "ANTIALIAS") else Image.BILINEAR)
    logo_image = ImageTk.PhotoImage(image)

    # Create a label to display the image
    logo_label = tk.Label(gui, image=logo_image)
    logo_label.image = logo_image  # Retain a reference to the image
    logo_label.pack(pady=10)  # Add vertical padding below the description label

    # Create the 'Go!' button
    go_button = tk.Button(gui, text="Go!", command=lambda: handle_view_button(gui))
    go_button.pack(pady=10)  # Add vertical padding below the image label



def visualize_finances(gui):
    """Take user to the visualize screen to generate charts for transactions"""
    gui.geometry("700x500")

    # Destroy existing widgets
    for widget in gui.winfo_children():
        widget.destroy()

    # Create page description
    visualize_page_label = tk.Label(gui,
                                    text="Generate graphs and charts for transactions. Specify dates (YYYY-MM-DD) to visualize below.")
    visualize_page_label.pack()

    # Create a frame for date range selection
    date_frame = tk.Frame(gui)
    date_frame.pack(pady=20)

    # Date Range Label and Entry Widgets
    start_date_label = tk.Label(date_frame, text="Start Date:")
    start_date_label.grid(row=0, column=0, padx=10)
    start_date_entry = tk.Entry(date_frame)
    start_date_entry.grid(row=0, column=1, padx=10)

    end_date_label = tk.Label(date_frame, text="End Date:")
    end_date_label.grid(row=0, column=2, padx=10)
    end_date_entry = tk.Entry(date_frame)
    end_date_entry.grid(row=0, column=3, padx=10)

    # Function to fetch transaction totals based on date range
    def fetch_transaction_totals(start_date, end_date):
        """Fetch transaction totals by category from SQLite database within the specified date range."""
        conn = sqlite3.connect('transactions.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT category, SUM(amount) FROM transactions WHERE date BETWEEN ? AND ? GROUP BY category",
                (start_date, end_date))
            rows = cursor.fetchall()
        return rows

    # Function to generate pie chart based on selected date range
    def generate_pie_chart():
        """Generate pie chart based on transaction totals."""
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        # Check if start_date or end_date is not specified
        if not start_date or not end_date:
            tk.messagebox.showerror("Error", "Please specify both start and end dates.")
            return

        data = fetch_transaction_totals(start_date, end_date)
        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        # Plotting
        plt.figure(figsize=(8, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')

        plt.title(f'Transaction Distribution by Category ({start_date} to {end_date})')
        plt.show()

    # Create a frame for the 'Transactions Pie Chart'
    pie_frame = tk.Frame(gui)
    pie_frame.pack(pady=20)

    # Label for pie chart button
    pie_label = tk.Label(pie_frame, text="View pie chart of transactions for given date range")
    pie_label.pack(pady=10)

    # Create Pie Chart button and place it in the pie frame
    pie_transactions_button = tk.Button(pie_frame, text="Transactions Pie Chart", command=generate_pie_chart)
    pie_transactions_button.pack()

    # Function to fetch unique categories from the database
    def fetch_unique_categories():
        """Fetch unique categories from SQLite database."""
        conn = sqlite3.connect('transactions.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM transactions")
            rows = cursor.fetchall()
        return [row[0] for row in rows]  # Extract categories from fetched rows

    # Create a frame for the 'Trends Graph'
    trends_frame = tk.Frame(gui)
    trends_frame.pack(pady=20)

    # Label for trends button
    trends_label = tk.Label(trends_frame, text="View spending trends for specified category and date range")
    trends_label.pack(pady=10)

    # Function to generate line graph based on selected category and date range
    def generate_trends_graph():
        """Generate line graph to visualize transaction trends for the selected category."""
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        selected_category = category_var.get()

        # Ensure that a category is selected
        if not selected_category:
            tk.messagebox.showerror("Error", "Please select a category.")
            return

        # Fetch individual transactions for the selected category and date range
        conn = sqlite3.connect('transactions.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT date, amount FROM transactions WHERE category = ? AND date BETWEEN ? AND ?",
                           (selected_category, start_date, end_date))
            rows = cursor.fetchall()

        if not rows:
            tk.messagebox.showerror("Error",
                                    f"No transactions found for {selected_category} in the specified date range.")
            return

        dates = [row[0] for row in rows]  # Extract dates
        amounts = [row[1] for row in rows]  # Extract amounts

        # Convert dates to a format suitable for plotting, if necessary
        # (This assumes that the dates are already in a format that matplotlib can interpret)
        # If the dates are strings, you may need to convert them to a datetime object and then format them as needed.

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(dates, amounts, marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title(f'Transaction Trend for {selected_category} ({start_date} to {end_date})')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Fetch unique categories and update the dropdown widget
    categories = fetch_unique_categories()

    # If there are no categories, show an error message
    if not categories:
        tk.messagebox.showerror("Error", "No categories found in the database.")
    else:
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(trends_frame, textvariable=category_var, values=categories)
        category_dropdown.set("Select Category")
        category_dropdown.pack(pady=10)

        # Create trends button and place it in the trend frame
        trends_button = tk.Button(trends_frame, text="View Trends", command=generate_trends_graph)
        trends_button.pack(pady=10)

    # Create a frame for placing the 'Back' button
    back_frame = tk.Frame(gui)
    back_frame.pack(pady=20)  # Add some padding

    # Create 'Back' button and place it in the back frame
    back_button = tk.Button(back_frame, text="Back", command=lambda: handle_view_button(gui))
    back_button.pack()  # Place the button in the bottom frame

