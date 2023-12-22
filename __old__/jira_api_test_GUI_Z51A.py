import csv
import re
import argparse
from datetime import datetime
from atlassian import Jira
import traceback2 as traceback
import tkinter as tk
from tkinter import messagebox

# ... [Your existing imports and function definitions] ...

def handle_button_click():
    try:
        args = type('Args', (object,), {
            'url': url_entry.get(),
            'username': username_entry.get(),
            'token': token_entry.get(),
            'project_key': project_key_entry.get(),
            'start_range': int(start_range_entry.get()),
            'end_range': int(end_range_entry.get())
        })
        jira = initialize_jira_connection(args)

        # [The rest of your main function logic]

        messagebox.showinfo("Success", f"Data written to {filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Jira Ticket Processor")

tk.Label(root, text="Jira URL:").pack()
url_entry = tk.Entry(root)
url_entry.pack()

tk.Label(root, text="Jira Username:").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Jira Token:").pack()
token_entry = tk.Entry(root)
token_entry.pack()

tk.Label(root, text="Project Key:").pack()
project_key_entry = tk.Entry(root)
project_key_entry.pack()

tk.Label(root, text="Start Range:").pack()
start_range_entry = tk.Entry(root)
start_range_entry.pack()

tk.Label(root, text="End Range:").pack()
end_range_entry = tk.Entry(root)
end_range_entry.pack()

process_button = tk.Button(root, text="Process Tickets", command=handle_button_click)
process_button.pack()

root.mainloop()
