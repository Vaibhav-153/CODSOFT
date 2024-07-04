import tkinter as tk
from tkinter import messagebox
import random
import string

# Function to generate password
def generate_password():
    try:
        length = int(entry_length.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for the length.")
        return

    if length <= 0:
        messagebox.showerror("Input Error", "Please enter a positive number for the length.")
        return

    complexity = complexity_var.get()
    characters = ""

    if complexity == "Low":
        characters = string.ascii_lowercase + string.digits
    elif complexity == "Medium":
        characters = string.ascii_letters + string.digits + string.punctuation
    elif complexity == "High":
        characters = string.ascii_letters + string.digits + string.punctuation + string.ascii_uppercase
    elif complexity == "Very High":
        characters = string.ascii_letters + string.digits + string.punctuation + string.ascii_uppercase + string.punctuation

    if not characters:
        messagebox.showerror("Input Error", "Please select a complexity level.")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    result_var.set(password)

# Create the main window
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x250")  # Set the window size

# Variables to store user input and result
entry_length = tk.Entry(root, width=20)
result_var = tk.StringVar()

# Complexity levels
complexity_var = tk.StringVar()
complexity_var.set("Low")  # Default complexity level

# Layout of the GUI
tk.Label(root, text="Password Length:").grid(row=0, column=0, padx=20, pady=10, sticky="e")
entry_length.grid(row=0, column=1, padx=20, pady=10)

tk.Label(root, text="Complexity Level:").grid(row=1, column=0, padx=20, pady=10, sticky="e")
tk.OptionMenu(root, complexity_var, "Low", "Medium", "High", "Very High").grid(row=1, column=1, padx=20, pady=10)

tk.Button(root, text="Generate Password", command=generate_password).grid(row=2, column=0, columnspan=2, pady=20)

tk.Label(root, text="Generated Password:").grid(row=3, column=0, padx=20, pady=10, sticky="e")
tk.Entry(root, textvariable=result_var, state="readonly", width=30).grid(row=3, column=1, padx=20, pady=10)

# Run the main event loop
root.mainloop()
