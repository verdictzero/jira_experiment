
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def run_script():
    # Collecting the user inputs
    url = url_entry.get()
    username = username_entry.get()
    token = token_entry.get()
    project_key = project_key_entry.get()
    start_range = start_range_entry.get()
    end_range = end_range_entry.get()

    # Validate inputs
    if not (url and username and token and project_key and start_range and end_range):
        messagebox.showwarning("Warning", "All fields are required")
        return

    try:
        # Convert range values to integers
        start_range = int(start_range)
        end_range = int(end_range)
    except ValueError:
        messagebox.showwarning("Warning", "Start and End Range must be integers")
        return

    # Path to the script - adjust as necessary
    script_path = 'jira_api_test_30A.py'

    # Constructing the command
    cmd = [sys.executable, script_path, url, username, token, project_key, str(start_range), str(end_range)]

    # Open a new terminal window and run the script with the provided arguments
    subprocess.Popen(["start", "cmd", "/k"] + cmd, shell=True)

# Creating the main window
root = tk.Tk()
root.title("Jira API Script Runner")

# Creating input fields
tk.Label(root, text="Jira URL:").grid(row=0, column=0)
url_entry = tk.Entry(root)
url_entry.grid(row=0, column=1)

tk.Label(root, text="Jira Username:").grid(row=1, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1)

tk.Label(root, text="Jira Token:").grid(row=2, column=0)
token_entry = tk.Entry(root)
token_entry.grid(row=2, column=1)

tk.Label(root, text="Project Key:").grid(row=3, column=0)
project_key_entry = tk.Entry(root)
project_key_entry.grid(row=3, column=1)

tk.Label(root, text="Start Range:").grid(row=4, column=0)
start_range_entry = tk.Entry(root)
start_range_entry.grid(row=4, column=1)

tk.Label(root, text="End Range:").grid(row=5, column=0)
end_range_entry = tk.Entry(root)
end_range_entry.grid(row=5, column=1)

# Run button
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=6, column=0, columnspan=2)

# Start the GUI loop
root.mainloop()
