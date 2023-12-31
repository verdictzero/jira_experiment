import tkinter as tk
from tkinter import messagebox
import jdeu_logic_module  # Ensure this is in the same directory

def handle_button_click():
    try:
        url = url_entry.get()
        username = username_entry.get()
        token = token_entry.get()
        project_key = project_key_entry.get()
        start_range = int(start_range_entry.get())
        end_range = int(end_range_entry.get())

        filename = jdeu_logic_module.process_tickets(url, username, token, project_key, start_range, end_range)
        messagebox.showinfo("Success", f"Data written to {filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Jira Data Extraction Utility")
root.geometry("500x300")

# Default values
default_url = "https://defenestrate.atlassian.net"
default_username = "verdict.zero@gmail.com"
default_token = "your_token"
default_project_key = "TEST"
default_start_range = "0"
default_end_range = "0"

tk.Label(root, text="Jira URL:").pack()
url_entry = tk.Entry(root)
url_entry.insert(0, default_url)
url_entry.pack()

tk.Label(root, text="Jira Username:").pack()
username_entry = tk.Entry(root)
username_entry.insert(0, default_username)
username_entry.pack()

tk.Label(root, text="Jira Token:").pack()
token_entry = tk.Entry(root, show="*")  # Masking the token for security
token_entry.insert(0, default_token)
token_entry.pack()

tk.Label(root, text="Project Key:").pack()
project_key_entry = tk.Entry(root)
project_key_entry.insert(0, default_project_key)
project_key_entry.pack()

tk.Label(root, text="Start Range:").pack()
start_range_entry = tk.Entry(root)
start_range_entry.insert(0, default_start_range)
start_range_entry.pack()

tk.Label(root, text="End Range:").pack()
end_range_entry = tk.Entry(root)
end_range_entry.insert(0, default_end_range)
end_range_entry.pack()

process_button = tk.Button(root, text="Process Tickets", command=handle_button_click)
process_button.pack()

root.mainloop()
