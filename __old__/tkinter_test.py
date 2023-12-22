import tkinter as tk
from tkinter import messagebox

def on_button_click():
    messagebox.showinfo("Information", "Button Clicked!")

# Initialize the main window
root = tk.Tk()
root.title("Tkinter UI Example - Left Aligned with Padding")
root.geometry("400x400")

# Define padding
left_padding = 10

# Label
label = tk.Label(root, text="Welcome to Tkinter!")
label.pack(anchor=tk.W, padx=left_padding)

# Button
button = tk.Button(root, text="Click Me!", command=on_button_click)
button.pack(anchor=tk.W, padx=left_padding)

# Entry
entry = tk.Entry(root)
entry.pack(anchor=tk.W, padx=left_padding)

# Text
text_area = tk.Text(root, height=5, width=30)
text_area.pack(anchor=tk.W, padx=left_padding)

# Checkbutton
check_var = tk.BooleanVar()
checkbutton = tk.Checkbutton(root, text="Check me", variable=check_var)
checkbutton.pack(anchor=tk.W, padx=left_padding)

# Radiobutton
radio_var = tk.StringVar()
radio1 = tk.Radiobutton(root, text="Option 1", variable=radio_var, value="Option 1")
radio1.pack(anchor=tk.W, padx=left_padding)
radio2 = tk.Radiobutton(root, text="Option 2", variable=radio_var, value="Option 2")
radio2.pack(anchor=tk.W, padx=left_padding)

# Listbox
listbox = tk.Listbox(root)
listbox.insert(1, "Item 1")
listbox.insert(2, "Item 2")
listbox.pack(anchor=tk.W, padx=left_padding)

# Scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Frame
frame = tk.Frame(root, bg="light grey")
frame.pack(fill=tk.BOTH, expand=True, anchor=tk.W, padx=left_padding)

# Menu
menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

# Start the main loop
root.mainloop()
