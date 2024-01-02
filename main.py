import tkinter as tk  # Import the Tkinter module
from functions import handle_new_button, handle_view_button


# Create the main application window
gui = tk.Tk()
# Set the GUI size
gui.geometry("300x200")

# Set the title of the window
gui.title("Python Pocketbook")

# Create the New button and pack it into the main window
new_button = tk.Button(gui, text="New", command=handle_new_button)
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

# Run the main event loop
gui.mainloop()
