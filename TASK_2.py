import tkinter as tk
from tkinter import messagebox

# Functions for arithmetic operations
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y

def modulus(x, y):
    return x % y

def exponentiate(x, y):
    return x ** y

def int_divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x // y

# Function to perform the calculation
def calculate():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
        return

    operation = operation_var.get()
    if operation == "Add":
        result = add(num1, num2)
    elif operation == "Subtract":
        result = subtract(num1, num2)
    elif operation == "Multiply":
        result = multiply(num1, num2)
    elif operation == "Divide":
        result = divide(num1, num2)
    elif operation == "Modulus":
        result = modulus(num1, num2)
    elif operation == "Exponentiate":
        result = exponentiate(num1, num2)
    elif operation == "Int Divide":
        result = int_divide(num1, num2)
    else:
        result = "Invalid Operation"

    result_var.set(result)

# Create the main window
root = tk.Tk()
root.title("Enhanced Calculator")
root.geometry("400x300")  # Set the window size

# Variables to store user input and result
entry_num1 = tk.Entry(root, width=20)
entry_num2 = tk.Entry(root, width=20)
operation_var = tk.StringVar(value="Add")
result_var = tk.StringVar()

# Layout of the GUI
tk.Label(root, text="First Number:").grid(row=0, column=0, padx=20, pady=10, sticky="e")
entry_num1.grid(row=0, column=1, padx=20, pady=10)

tk.Label(root, text="Second Number:").grid(row=1, column=0, padx=20, pady=10, sticky="e")
entry_num2.grid(row=1, column=1, padx=20, pady=10)

tk.Label(root, text="Operation:").grid(row=2, column=0, padx=20, pady=10, sticky="e")
operation_menu = tk.OptionMenu(root, operation_var, "Add", "Subtract", "Multiply", "Divide", "Modulus", "Exponentiate", "Int Divide")
operation_menu.grid(row=2, column=1, padx=20, pady=10)

tk.Button(root, text="Calculate", command=calculate).grid(row=3, column=0, columnspan=2, pady=20)

tk.Label(root, text="Result:").grid(row=4, column=0, padx=20, pady=10, sticky="e")
tk.Entry(root, textvariable=result_var, state="readonly").grid(row=4, column=1, padx=20, pady=10)

# Run the main event loop
root.mainloop()
