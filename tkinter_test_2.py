import tkinter as tk
from tkinter import messagebox, filedialog

def process_and_display_input():
    user_input = entry.get()
    processed_output = f"Processed: {user_input}"
    
    # Display in Text widget
    text_area.delete('1.0', tk.END)  # Clear previous text
    text_area.insert(tk.END, processed_output)

    # Save to file
    save_to_file(processed_output)

def save_to_file(text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text)
        messagebox.showinfo("Information", f"Output saved to {file_path}")

# Initialize the main window
root = tk.Tk()
root.title("Tkinter Application - Input, Process, and Save")
root.geometry("500x500")

# Entry for user input
entry = tk.Entry(root, width=50)
entry.pack(anchor=tk.W, padx=10)

# Button to process input
process_button = tk.Button(root, text="Process Input", command=process_and_display_input)
process_button.pack(anchor=tk.W, padx=10)

# Text area for displaying output
text_area = tk.Text(root, height=10, width=50)
text_area.pack(anchor=tk.W, padx=10)

# Start the main loop
root.mainloop()
