import tkinter as tk
from tkinter import scrolledtext

def run_script():
    # Retrieve the inputs from the GUI
    url = url_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    project_key = project_key_entry.get()
    start_range = start_range_entry.get()
    end_range = end_range_entry.get()

    # Here, integrate the logic of your script using the above inputs
    # For demonstration, this will print the entered values
    output_text.insert(tk.END, "Script executed. Check the console for details.\n")

    # You should replace the print statements in your script with output_text.insert(tk.END, "Your message\n")
    # And handle the script's main logic here

    

# Setting up the main window
root = tk.Tk()
root.title("Jira Data Extractor")

# Creating input fields for Jira credentials and project details
tk.Label(root, text="Jira Instance URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root)
url_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Jira Username:").grid(row=1, column=0, padx=10, pady=10)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Jira Private Key:").grid(row=2, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show='*')
password_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Project Key:").grid(row=3, column=0, padx=10, pady=10)
project_key_entry = tk.Entry(root)
project_key_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Start of Ticket Range:").grid(row=4, column=0, padx=10, pady=10)
start_range_entry = tk.Entry(root)
start_range_entry.grid(row=4, column=1, padx=10, pady=10)

tk.Label(root, text="End of Ticket Range:").grid(row=5, column=0, padx=10, pady=10)
end_range_entry = tk.Entry(root)
end_range_entry.grid(row=5, column=1, padx=10, pady=10)

# Button to run the script
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Output area
output_text = scrolledtext.ScrolledText(root, width=40, height=10)
output_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
