import csv
from datetime import datetime
from atlassian import Jira
from atlassian import utils
import pip_system_certs.wrapt_requests
import argparse

def safe_str(obj):
    try:
        return str(obj)
    except UnicodeEncodeError:
        # Encode the string to 'ascii', replacing problematic characters with 'X'
        return obj.encode('ascii', 'replace').decode('ascii')

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Script to connect to Jira, process a range of tickets, and output to a CSV file.')

# Define the arguments
parser.add_argument('url', type=str, help='Jira URL')
parser.add_argument('username', type=str, help='Jira username')
parser.add_argument('token', type=str, help='Jira token')
parser.add_argument('project_key', type=str, help='Project key (e.g., TEST)')
parser.add_argument('start_range', type=int, help='Start of the ticket range (e.g., 1)')
parser.add_argument('end_range', type=int, help='End of the ticket range (e.g., 100)')

# Parse the arguments
args = parser.parse_args()

# Initialize Jira connection
jira = Jira(
    url=args.url,
    username=args.username,
    token=args.token
)

# Use the arguments
project_key = args.project_key
start_range = args.start_range
end_range = args.end_range

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
