import csv
import re
import argparse
from datetime import datetime
from atlassian import Jira
import traceback2 as traceback

def safe_str(obj):
    try:
        return str(obj)
    except UnicodeEncodeError:
        return obj.encode('ascii', 'replace').decode('ascii')

def convert_time_to_seconds(time_str):
    time_units = {'w': 604800, 'd': 86400, 'h': 3600, 'm': 60, 's': 1}
    total_seconds = 0
    parts = re.findall(r'(\d+)([wdhms])', time_str)
    for amount, unit in parts:
        total_seconds += int(amount) * time_units[unit]
    return total_seconds

def parse_arguments():
    parser = argparse.ArgumentParser(description='Script to connect to Jira, process a range of tickets, and output to a CSV file.')
    parser.add_argument('url', type=str, help='Jira URL')
    parser.add_argument('username', type=str, help='Jira username')
    parser.add_argument('token', type=str, help='Jira token')
    parser.add_argument('project_key', type=str, help='Project key (e.g., TEST)')
    parser.add_argument('start_range', type=int, help='Start of the ticket range (e.g., 1)')
    parser.add_argument('end_range', type=int, help='End of the ticket range (e.g., 100)')
    return parser.parse_args()

def initialize_jira_connection(args):
    return Jira(url=args.url, username=args.username, password=args.token) # !! IMPORTANT !! --- change to token=args.token when using with SE2

def fetch_latest_ticket(jira, project_key):
    jql_query = f'project = {project_key} ORDER BY created DESC'
    try:
        tickets = jira.jql(jql_query, limit=1)['issues']
        if tickets:
            return tickets[0]
        else:
            print("No tickets found in the project.")
            return None
    except Exception as e:
        print(f"Error fetching tickets: {e}")
        traceback.print_exc()
        return None

def fetch_issues(jira, project_key, start_range, end_range):
    issues_list = []
    for i in range(start_range, end_range + 1):
        issue_key = f"{project_key}-{i}"
        try:
            issue = jira.issue(issue_key)
            issues_list.append(issue)
            print(issue['key'], issue['fields']['summary'])
        except Exception as e:
            print(f"Could not fetch issue {issue_key}. Error: {e}")
            # traceback.print_exc()
    return issues_list

def write_issues_to_csv(jira, issues_list, filename):
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

                    time_spent_seconds = convert_time_to_seconds(time_spent)
                    csv_writer.writerow([safe_str(issue_key), safe_str(summary), safe_str(status), safe_str(comment), safe_str(author_name), safe_str(time_spent), time_spent_seconds, safe_str(worklog_created), safe_str(extraction_time)])
            else:
                csv_writer.writerow([safe_str(issue_key), safe_str(summary), safe_str(status), 'No work records found.', '', '', 0, '', safe_str(extraction_time)])

def main():
    args = parse_arguments()
    jira = initialize_jira_connection(args)

    # Debug print statements
    print(f"DEBUG: URL = {args.url}")
    print(f"DEBUG: Username = {args.username}")
    print(f"DEBUG: Token = {args.token}")
    print(f"DEBUG: Project Key = {args.project_key}")
    print(f"DEBUG: Start Range = {args.start_range}")
    print(f"DEBUG: End Range = {args.end_range}")

    last_ticket = fetch_latest_ticket(jira, args.project_key)
    if last_ticket:
        print(f"DEBUG: Last Ticket = {last_ticket['key']}")

    issues_list = fetch_issues(jira, args.project_key, args.start_range, args.end_range)
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'jira_data_{current_time}.csv'
    write_issues_to_csv(jira, issues_list, filename)
    print(f"Data written to {filename}")

if __name__ == "__main__":
    main()
