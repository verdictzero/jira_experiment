import csv
from atlassian import Jira
from datetime import datetime

# Initialize Jira connection
jira = Jira(
    url='https://defenestrate.atlassian.net',
    username='verdict.zero@gmail.com',
    password='ATATT3xFfGF0mlrNZNButIwlwlR5A7FAf0nDyRFDlAoU5qHe1ORP9fqMLDu7Bh3YP9MI1-PSJZyAHmFT1Sv7-PqTXvajyURo14R2nQgk-V0ajK44RtLyhmEEgfEj0mgKYEXtnpKQOafO3nsoBWKToqE97uzwaPq55FTGqRNJMjVQuzUf3dIivOQ=5986C7DA'
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
with open(filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Issue Key', 'Summary', 'Worklog Comment', 'Author', 'Time Spent'])

    # Loop through the fetched issues to extract work logs and write to CSV
    for issue in issues_list:
        issue_key = issue['key']
        summary = issue['fields']['summary']
        
        worklogs_response = jira.get(f"rest/api/2/issue/{issue_key}/worklog")
        worklogs = worklogs_response.get('worklogs', [])
        
        if worklogs:
            for worklog in worklogs:
                comment = worklog.get('comment', "No comment provided.")
                author_name = worklog['author']['displayName']
                time_spent = worklog['timeSpent']
                
                # Write to CSV
                csv_writer.writerow([issue_key, summary, comment, author_name, time_spent])
        else:
            csv_writer.writerow([issue_key, summary, 'No work records found.', '', ''])

print(f"Data written to {filename}")
