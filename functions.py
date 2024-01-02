import tkinter as tk


def handle_new_button():
    # Define the functionality for the New button (to be implemented later)
    print("New button clicked")


def handle_view_button(gui):
    """Take user to the view/edit screen to interact with existing budget"""
    print("Edit button clicked")  # here for testing
    gui.geometry("700x500")

    # Destroy existing widgets in the window
    for widget in gui.winfo_children():
        widget.destroy()

    # Create page description
    edit_page_label = tk.Label(gui, text="Add/Edit transactions and generate reports.")
    edit_page_label.pack()  # Place the label below the Edit button

    # Create a frame for placing widgets side by side
    top_frame = tk.Frame(gui)
    top_frame.pack(pady=50)  # Add some padding

    # Create Add Transaction button and place it in the top frame
    add_transaction_button = tk.Button(top_frame, text="Add Transaction")
    add_transaction_button.pack(side=tk.LEFT, padx=10)  # Add padding

    # Create a dropdown menu for transaction types and place it in the top frame
    options = ['gas', 'groceries', 'discretionary']
    variable = tk.StringVar(gui)
    variable.set(options[0])  # Set the default option

    dropdown_menu = tk.OptionMenu(top_frame, variable, *options)
    dropdown_menu.pack(side=tk.LEFT, padx=10)  # Add padding

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

