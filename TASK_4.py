import tkinter as tk
from tkinter import messagebox
import random

# Function to determine the winner
def determine_winner(user_choice, comp_choice):
    if user_choice == comp_choice:
        return "It's a tie!"
    elif (user_choice == "Rock" and comp_choice == "Scissors") or \
         (user_choice == "Scissors" and comp_choice == "Paper") or \
         (user_choice == "Paper" and comp_choice == "Rock"):
        global user_score
        user_score += 1
        return "You win!"
    else:
        global comp_score
        comp_score += 1
        return "Computer wins!"

# Function to update the result and scores
def update_result(user_choice):
    comp_choice = random.choice(["Rock", "Paper", "Scissors"])
    result = determine_winner(user_choice, comp_choice)
    
    result_var.set(f"Your choice: {user_choice}\nComputer's choice: {comp_choice}\nResult: {result}")
    user_score_var.set(f"Your Score: {user_score}")
    comp_score_var.set(f"Computer's Score: {comp_score}")

# Function to reset the game
def reset_game():
    global user_score, comp_score
    user_score = 0
    comp_score = 0
    user_score_var.set(f"Your Score: {user_score}")
    comp_score_var.set(f"Computer's Score: {comp_score}")
    result_var.set("Make your choice!")

# Function to exit the game
def exit_game():
    root.quit()

# Initialize scores
user_score = 0
comp_score = 0

# Create the main window
root = tk.Tk()
root.title("Rock-Paper-Scissors")
root.geometry("400x300")  # Set the window size

# Variables to store results and scores
result_var = tk.StringVar()
result_var.set("Make your choice!")

user_score_var = tk.StringVar()
user_score_var.set(f"Your Score: {user_score}")

comp_score_var = tk.StringVar()
comp_score_var.set(f"Computer's Score: {comp_score}")

# Layout of the GUI
tk.Label(root, textvariable=result_var, wraplength=300, justify="center").pack(pady=20)

tk.Button(root, text="Rock", command=lambda: update_result("Rock")).pack(side="left", padx=20)
tk.Button(root, text="Paper", command=lambda: update_result("Paper")).pack(side="left", padx=20)
tk.Button(root, text="Scissors", command=lambda: update_result("Scissors")).pack(side="left", padx=20)

tk.Label(root, textvariable=user_score_var).pack(pady=10)
tk.Label(root, textvariable=comp_score_var).pack(pady=10)

tk.Button(root, text="Play Again", command=reset_game).pack(side="left", padx=20, pady=10)
tk.Button(root, text="Exit", command=exit_game).pack(side="right", padx=20, pady=10)

# Run the main event loop
root.mainloop()