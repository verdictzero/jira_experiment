import csv
from atlassian import Jira
from datetime import datetime

def safe_str(obj):
    try:
        return str(obj)
    except UnicodeEncodeError:
        # Encode the string to 'ascii', replacing problematic characters with 'X'
        return obj.encode('ascii', 'replace').decode('ascii')

url_user_set = input("Enter your Jira username:").strip()
username_user_set = input("Enter your Jira instance URL:").strip()
password_user_set = input("Enter your Jira private key:").strip()

# Initialize Jira connection
jira = Jira(
    url = url_user_set,
    username = username_user_set,
    password = password_user_set
)

# Get user input
project_key = input("Enter the project key (e.g., TEST): ").strip()
start_range = int(input("Enter the start of the ticket range (e.g., 1): ").strip())
end_range = int(input("Enter the end of the ticket range (e.g., 100): ").strip())

# Temporary storage for issues
issues_list = []

# Loop through the specified ticket range to fetch issue summaries
for i in range(start_range, end_range + 1):
    issue_key = f"{project_key}-{i}"
    try:
        issue = jira.issue(issue_key)
        issues_list.append(issue)
        print(issue['key'], issue['fields']['summary'])
    except Exception as e:
        # If the issue does not exist or any other error occurs, print an error message
        print(f"Could not fetch issue {issue_key}. Error: {e}")

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

print(f"Data written to {filename}")
