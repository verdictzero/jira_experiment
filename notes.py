import tkinter as tk
import csv
from atlassian import Jira
from datetime import datetime

# Function to calculate the width of the largest label
def get_max_label_width(labels):
    return max([len(label) for label in labels])

# Labels for the GUI
labels_text = ["Jira Instance URL:", "Jira Username:", "Jira Private Key:", "Project Key:", "Start of Ticket Range:", "End of Ticket Range:"]

# Calculate the width of the largest label
max_label_width = get_max_label_width(labels_text)

def run_script():
    # Retrieve the inputs from the GUI
    url_B = url_entry.get()
    username_B = username_entry.get()
    password_B = password_entry.get()
    project_key = project_key_entry.get()
    start_range = int(start_range_entry.get())
    end_range = int(end_range_entry.get())

    # Here, integrate the logic of your script using the above inputs
    # For demonstration, this will print the entered values
    output_text.insert(tk.END, "Script executed. Check the console for details.\n")

    # ... (rest of your script logic for connecting to Jira and processing data)

# Setting up the main window
root = tk.Tk()
root.title("Jira Data Extractor")

# Creating input fields for Jira credentials and project details
url_entry, username_entry, password_entry, project_key_entry, start_range_entry, end_range_entry = [None] * 6
entries = [url_entry, username_entry, password_entry, project_key_entry, start_range_entry, end_range_entry]

for i, label_text in enumerate(labels_text):
    label = tk.Label(root, text=label_text, anchor='w', width=max_label_width)
    label.grid(row=i, column=0, padx=10, pady=10, sticky='w')
    entries[i] = tk.Entry(root)
    entries[i].grid(row=i, column=1, padx=10, pady=10, sticky='ew')

# Unpack the entries for easier access
url_entry, username_entry, password_entry, project_key_entry, start_range_entry, end_range_entry = entries

# Configure the column 0 (label column) to have a fixed size
root.grid_columnconfigure(0, minsize=max_label_width)

# Configure the column 1 (entry column) to expand
root.grid_columnconfigure(1, weight=1)

# Button to run the script
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=len(labels_text), column=0, columnspan=2, padx=10, pady=10)

# Create a ScrolledText widget
output_text = scrolledtext.ScrolledText(root, width=40, height=10)
output_text.grid(row=len(labels_text) + 1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Configure the grid to resize
root.grid_rowconfigure(len(labels_text) + 1, weight=1)  # Allow row for ScrolledText to resize
root.grid_columnconfigure(0, weight=1)  # Allow column 0 to resize
root.grid_columnconfigure(1, weight=1)  # Allow column 1 to resize

# Start the GUI event loop
root.mainloop()
