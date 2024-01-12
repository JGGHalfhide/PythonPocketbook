import tkinter as tk
from functions import create_database, handle_view_button
from PIL import Image, ImageTk

# Create database if it does not exist
create_database()

# Create the main application window
gui = tk.Tk()
gui.geometry("700x500")
gui.title("Python Pocketbook")

# Create a label with app description and pack it at the top
new_label = tk.Label(
    gui,
    text="Welcome to Python Pocketbook! Manage your finances effortlessly by entering, editing, and visualizing your transactions. Your financial journey starts here.",
    wraplength=600
)
new_label.pack(pady=20)

# Load and resize the image using Pillow
image_path = "/Users/jonathan/PycharmProjects/PythonPocketbook/venv/images/wallet-svgrepo-com.png"
image = Image.open(image_path)
image = image.resize((200, 200), Image.ANTIALIAS if hasattr(Image, "ANTIALIAS") else Image.BILINEAR)
logo_image = ImageTk.PhotoImage(image)

# Create a label to display the image
logo_label = tk.Label(gui, image=logo_image)
logo_label.image = logo_image  # Retain a reference to the image
logo_label.pack(pady=10)

# Create the 'Go!' button and pack it below the image label
go_button = tk.Button(gui, text="Go!", command=lambda: handle_view_button(gui))
go_button.pack(pady=10)

# Run the main event loop
gui.mainloop()
