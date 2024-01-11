import tkinter as tk
from functions import create_database, handle_view_button
from PIL import Image, ImageTk


# Create the main application window
gui = tk.Tk()
# Set the GUI size
gui.geometry("700x500")

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

# Load the image using Pillow
image = Image.open("/Users/jonathan/PycharmProjects/PythonPocketbook/venv/images/wallet-svgrepo-com.png")

# Resize the image with antialiasing
image = image.resize((200, 200), Image.ANTIALIAS if hasattr(Image, "ANTIALIAS") else Image.BILINEAR)

# Convert the Image object into a PhotoImage object
logo_image = ImageTk.PhotoImage(image)

# Create a label to display the image
logo_label = tk.Label(gui, image=logo_image)
logo_label.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)  # Position at the bottom and fill the space

# Keep a reference to the image to prevent it from being garbage collected
logo_label.image = logo_image

# Run the main event loop
gui.mainloop()
