import tkinter as tk
from tkinter import messagebox
import your_script_name  # Import your script functions here

def run_script():
    url = url_entry.get()
    username = username_entry.get()
    token = token_entry.get()
    project_key = project_key_entry.get()
    start_range = int(start_range_entry.get())
    end_range = int(end_range_entry.get())

    # Call your script function here, pass the parameters
    # Example: your_script_name.main_function(url, username, token, project_key, start_range, end_range)
    messagebox.showinfo("Info", "Script executed successfully")

# Create the main window
root = tk.Tk()
root.title("Jira Script GUI")

# Create and place widgets
tk.Label(root, text="Jira URL").grid(row=0, column=0)
url_entry = tk.Entry(root)
url_entry.grid(row=0, column=1)

tk.Label(root, text="Username").grid(row=1, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1)

tk.Label(root, text="Token").grid(row=2, column=0)
token_entry = tk.Entry(root)
token_entry.grid(row=2, column=1)

tk.Label(root, text="Project Key").grid(row=3, column=0)
project_key_entry = tk.Entry(root)
project_key_entry.grid(row=3, column=1)

tk.Label(root, text="Start Range").grid(row=4, column=0)
start_range_entry = tk.Entry(root)
start_range_entry.grid(row=4, column=1)

tk.Label(root, text="End Range").grid(row=5, column=0)
end_range_entry = tk.Entry(root)
end_range_entry.grid(row=5, column=1)

run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=6, column=0, columnspan=2)

# Start the event loop
root.mainloop()
