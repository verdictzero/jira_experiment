import csv
from datetime import datetime
from atlassian import Jira
from atlassian import utils
import pip_system_certs.wrapt_requests
import argparse
import requests
import traceback2 as traceback
import re

# ATATT3xFfGF0WlzTEcU8ZRxTjgeKVquwSC4A5eH9o1nT7g4NpWtUiXjFhvZvQMC8larABCHEpx9g1uZ3j60Gu1JLMknzBb-NAjc_hpl8Okp52Ni7JqYfigbY7r2Yd3fOV_9xReOfhuZfk5aN1jVvZaoVcYWIkGAkuzrZF0WLPptwqIkLSijq1iE=A4BB6614

def safe_str(obj):
    try:
        return str(obj)
    except UnicodeEncodeError:
        # Encode the string to 'ascii', replacing problematic characters with 'X'
        return obj.encode('ascii', 'replace').decode('ascii')

def convert_time_to_seconds(time_str):
    time_units = {'w': 604800, 'd': 86400, 'h': 3600, 'm': 60, 's': 1}
    total_seconds = 0
    parts = re.findall(r'(\d+)([wdhms])', time_str)
    for amount, unit in parts:
        total_seconds += int(amount) * time_units[unit]
    return total_seconds

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Script to connect to Jira, process a range of tickets, and output to a CSV file.')

# Define the arguments
parser.add_argument('url', type=str, help='Jira URL')
parser.add_argument('username', type=str, help='Jira username')
parser.add_argument('token', type=str, help='Jira token')
parser.add_argument('project_key', type=str, help='Project key (e.g., TEST)')
parser.add_argument('start_range', type=int, help='Start of the ticket range (e.g., 1)')
parser.add_argument('end_range', type=int, help='End of the ticket range (e.g., 100)')

# After parsing the arguments
args = parser.parse_args()

# Debug print statements
print(f"Debug: URL = {args.url}")
print(f"Debug: Username = {args.username}")
print(f"Debug: Token = {args.token}")
print(f"Debug: Project Key = {args.project_key}")
print(f"Debug: Start Range = {args.start_range}")
print(f"Debug: End Range = {args.end_range}")

# Initialize Jira connection
jira = Jira(
    url=args.url,
    username=args.username,
    password=args.token
)

# Define the JQL query
jql_query = f'project = {args.project_key} ORDER BY created DESC'

# Fetch the latest ticket using JQL
try:
    tickets = jira.jql(jql_query, limit=1)['issues']
    if tickets:
        last_ticket = tickets[0]
        print(f"Last ticket key: {last_ticket['key']}")

        # Extracting the numeric part from the ticket key
        match = re.search(r'\d+$', last_ticket['key'])
        if match:
            maximum_upper_limit = int(match.group())
            print(f"Maximum upper limit (integer): {maximum_upper_limit}")
        else:
            print("No numeric part found in the ticket key.")
    else:
        print("No tickets found in the project.")
except Exception as e:
    print(f"Error fetching tickets: {e}")
    traceback.print_exc()

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
        print(f"Could not fetch issue {issue_key}. Error: {e}")
        traceback.print_exc()  # Print detailed traceback

# Create a datetime stamped filename
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'jira_data_{current_time}.csv'

# Prepare CSV file for writing
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Issue Key', 'Summary', 'Status', 'Worklog Comment', 'Author', 'Time Spent', 'Time Spent Converted', 'Worklog Created', 'Data Extracted Time'])

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
                time_spent_seconds = convert_time_to_seconds(time_spent)
                csv_writer.writerow([safe_str(issue_key), safe_str(summary), safe_str(status), safe_str(comment), safe_str(author_name), safe_str(time_spent), time_spent_seconds, safe_str(worklog_created), safe_str(extraction_time)])
        else:
            csv_writer.writerow([safe_str(issue_key), safe_str(summary), safe_str(status), 'No work records found.', '', '', 0, '', safe_str(extraction_time)])

print(f"Data written to {filename}")