import tkinter as tk
from tkinter import messagebox
import threading
import jdeu_logic_module  # Ensure this is in the same directory

def process_tickets_thread(url, username, token, project_key, start_range, end_range):
    try:
        filename = jdeu_logic_module.process_tickets(url, username, token, project_key, start_range, end_range)
        messagebox.showinfo("Success", f"Data written to {filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        # Enable the button and clear the warning message after processing
        process_button.config(state=tk.NORMAL)
        warning_label.config(text="")

def handle_button_click():
    # Disable the button
    process_button.config(state=tk.DISABLED) # [ !! - Note: if you comment this out, you can launch multiple threads, and bad things can happen, don't do that. - !! ]

    # Update warning message
    warning_label.config(text="DO NOT CLOSE THIS WINDOW\nTHIS MAY TAKE A WHILE\nSEE CONSOLE FOR PROCESS OUTPUT", fg="red")

    # Start the process in a new thread
    url = url_entry.get()
    username = username_entry.get()
    token = token_entry.get()
    project_key = project_key_entry.get()
    start_range = int(start_range_entry.get())
    end_range = int(end_range_entry.get())

    threading.Thread(target=process_tickets_thread, args=(url, username, token, project_key, start_range, end_range), daemon=True).start()

root = tk.Tk()
root.title("Jira Data Extraction Utility")
root.geometry("500x500")

# Default values
default_url = "https://jira.se2.army.mil"
default_username = "evan.snyder"
default_token = "Nzk3OTY3OTg1NDAxOpS7hLb+j3Y7qnP40Y0WPHOCHyZH"
default_project_key = "DCGSAV32"
default_start_range = "0"
default_end_range = "0"

# Labels and entries with padding
tk.Label(root, text="Jira URL:").pack(pady=2)
url_entry = tk.Entry(root)
url_entry.insert(0, default_url)
url_entry.pack(pady=2)

tk.Label(root, text="Jira Username:").pack(pady=2)
username_entry = tk.Entry(root)
username_entry.insert(0, default_username)
username_entry.pack(pady=2)

tk.Label(root, text="Jira Token:").pack(pady=2)
token_entry = tk.Entry(root, show="*")
token_entry.insert(0, default_token)
token_entry.pack(pady=2)

tk.Label(root, text="Project Key:").pack(pady=2)
project_key_entry = tk.Entry(root)
project_key_entry.insert(0, default_project_key)
project_key_entry.pack(pady=2)

tk.Label(root, text="Start Range:").pack(pady=2)
start_range_entry = tk.Entry(root)
start_range_entry.insert(0, default_start_range)
start_range_entry.pack(pady=2)

tk.Label(root, text="End Range:").pack(pady=2)
end_range_entry = tk.Entry(root)
end_range_entry.insert(0, default_end_range)
end_range_entry.pack(pady=2)

# Process button with padding
process_button = tk.Button(root, text="Process Tickets", command=handle_button_click)
process_button.pack(pady=2)

# Warning label with padding
warning_label = tk.Label(root, text="", font=("Helvetica", 10, "bold"))
warning_label.pack(pady=2)

root.mainloop()
