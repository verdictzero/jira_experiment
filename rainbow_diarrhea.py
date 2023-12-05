import tkinter as tk
from tkinter import Entry

# Create the main window
root = tk.Tk()
root.title("Rainbow Buttons and Gradient Text Boxes")

# Define rainbow colors and gradient colors
rainbow_colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
gradient_colors = ["#000000", "#404040", "#808080", "#C0C0C0", "#FFFFFF"]

# Function to determine the text color based on background brightness
def get_text_color(bg_color):
    if bg_color in ["#000000", "#404040", "#808080"]:
        return "white"
    else:
        return "black"

# Create and place rainbow buttons
for i, color in enumerate(rainbow_colors):
    button = tk.Button(root, text=color.capitalize(), bg=color, fg="white")
    button.grid(row=0, column=i, padx=10, pady=10)

# Create and place gradient text boxes
for i, color in enumerate(gradient_colors):
    text_color = get_text_color(color)
    entry = Entry(root, bg=color, fg=text_color)
    entry.grid(row=1, column=i, padx=10, pady=10, sticky="ew")

# Start the Tkinter event loop
root.mainloop()