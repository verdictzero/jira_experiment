import csv
from atlassian import Jira
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext
import pip_system_certs.wrapt_requests

# https://defenestrate.atlassian.net/
# verdict.zero@gmail.com
# ATATT3xFfGF0zBa7u_mE4lY5w9uBBqroHlmJ_nL5n4w6LiOEDbui9OP2CB0-Rz5NLGEBAxu4qjI5O6Jeth0H9hI_LQ1I2plUGjYJfLTQ8Tw-_RSKvfTer1s974eP6zG8NHcxvyJaFm6VqckMKUd9qT-zTRoh-Wtb-qv74cReJI8efKMfx2LQqps=5A27F67B
# DCGSFX64

# Function to calculate the width of the largest label
def get_max_label_width(labels):
    return max([len(label) for label in labels])

# Labels for the GUI
labels_text = ["Jira Instance URL:", "Jira Username:", "Jira Private Key:", "Project Key:", "Start of Ticket Range:", "End of Ticket Range:"]

# Calculate the width of the largest label
max_label_width = get_max_label_width(labels_text)

def run_script():
    # Retrieve the inputs from the GUI00
    url_B = url_entry.get()
    username_B = username_entry.get()
    password_B = password_entry.get()
    project_key = project_key_entry.get()
    start_range = int(start_range_entry.get())
    end_range = int(end_range_entry.get())

    # Here, integrate the logic of your script using the above inputs
    # For demonstration, this will print the entered values
    output_text.insert(tk.END, "Script executed. Check the console for details.\n")

    # You should replace the print statements in your script with output_text.insert(tk.END, "Your message\n")
    # And handle the script's main logic here

    
    def safe_str(obj):
        try:
            return str(obj)
        except UnicodeEncodeError:
            # Encode the string to 'ascii', replacing problematic characters with 'X'
            return obj.encode('ascii', 'replace').decode('ascii')

    # Initialize Jira connection
    jira = Jira(
        url = url_B,
        username = username_B,
        token = password_B # I initially forgot to use the 'token' input to Jira instead of password, which is why the other variables and input prompts are labled as password
    )

    # Get user input
    # project_key = input("Enter the project key (e.g., TEST): ").strip()
    # start_range = int(input("Enter the start of the ticket range (e.g., 1): ").strip())
    # end_range = int(input("Enter the end of the ticket range (e.g., 100): ").strip())

    # Temporary storage for issues
    issues_list = []

    # Loop through the specified ticket range to fetch issue summaries
    for i in range(start_range, end_range + 1):
        issue_key = f"{project_key}-{i}"
        try:
            issue = jira.issue(issue_key)
            issues_list.append(issue)
            output_text.insert(tk.END,issue['key'], issue['fields']['summary'])
        except Exception as e:
            # If the issue does not exist or any other error occurs, print an error message
            output_text.insert(tk.END,f"Could not fetch issue {issue_key}. Error: {e}")

    # Create a datetime stamped filename
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'jira_data_{current_time}.csv'

    # Prepare CSV file for writing
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Issue Key', 'Summary', 'Status', 'Worklog Comment', 'Author', 'Time Spent', 'Worklog Created', 'Data Extracted Time'])

        # Loop through the fetched issues to extract work logs and write to CSV
        for issue in issues_list:
            issue_key = issue['key']
            summary = issue['fields']['summary']
            status = issue['fields']['status']['name']
            
            worklogs_response = jira.get(f"rest/api/2/issue/{issue_key}/worklog")
            worklogs = worklogs_response.get('worklogs', [])
            extraction_time = datetime.now().isoformat()

            if worklogs:
                for worklog in worklogs:
                    comment = worklog.get('comment', "No comment provided.")
                    author_name = worklog['author']['displayName']
                    time_spent = worklog['timeSpent']
                    worklog_created = worklog['started']
                    
                    # Write to CSV, using safe_str for each string field
                    csv_writer.writerow([safe_str(issue_key), safe_str(summary), safe_str(status), safe_str(comment), safe_str(author_name), safe_str(time_spent), safe_str(worklog_created), safe_str(extraction_time)])
            else:
                csv_writer.writerow([safe_str(issue_key), safe_str(summary), safe_str(status), 'No work records found.', '', '', '', safe_str(extraction_time)])

    output_text.insert(tk.END,f"Data written to {filename}")

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
root.grid_columnconfigure(0, minsize=max_label_width, weight=0)

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