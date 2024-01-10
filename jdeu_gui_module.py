import tkinter as tk
from tkinter import messagebox
import jdeu_logic_module  # Ensure this is in the same directory

def handle_button_click():
    try:
        # Disable the button
        process_button.config(state=tk.DISABLED)

        # Update warning message
        warning_label.config(text="DO NOT CLOSE THIS WINDOW\nTHIS MAY TAKE A WHILE\nSEE CONSOLE FOR PROCESS OUTPUT", fg="red")

        url = url_entry.get()
        username = username_entry.get()
        token = token_entry.get()
        project_key = project_key_entry.get()
        start_range = int(start_range_entry.get())
        end_range = int(end_range_entry.get())

        filename = jdeu_logic_module.process_tickets(url, username, token, project_key, start_range, end_range)
        messagebox.showinfo("Success", f"Data written to {filename}")

        # Enable the button and clear the warning message after processing
        process_button.config(state=tk.NORMAL)
        warning_label.config(text="")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        process_button.config(state=tk.NORMAL)
        warning_label.config(text="")

root = tk.Tk()
root.title("Jira Data Extraction Utility")
root.geometry("500x300")

# Default values
default_url = "https://jira.se2.army.mil"
default_username = "evan.snyder"
default_token = "Nzk3OTY3OTg1NDAxOpS7hLb+j3Y7qnP40Y0WPHOCHyZH"
default_project_key = "DCGSAV32"
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

# Label for warning message
warning_label = tk.Label(root, text="", font=("Helvetica", 10, "bold"))
warning_label.pack()

root.mainloop()
