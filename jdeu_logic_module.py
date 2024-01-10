import csv
import re
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

def initialize_jira_connection(url, username, token):
    return Jira(url=url, username=username, token=token)  # !! IMPORTANT !! --- change to token=token when using with SE2 --- (and password=token for Jira Cloud)

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
        # Adding new headers for work hours, days, weeks, years, and inactive status
        csv_writer.writerow(['Issue Key', 'Summary', 'Status', 'Worklog Comment', 'Author', 'Time Spent', 'Time Spent Converted', 'Work Hours', 'Work Days', 'Work Weeks', 'Work Years', 'Inactive', 'Worklog Created', 'Data Extracted Time'])

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
                    time_spent_hours = time_spent_seconds / 3600
                    time_spent_days = time_spent_seconds / (3600 * 24)
                    time_spent_weeks = time_spent_seconds / (3600 * 24 * 7)
                    time_spent_years = time_spent_seconds / (3600 * 24 * 365)

                    inactive = "Yes" if "[X]" in author_name else "No"

                    csv_writer.writerow([safe_str(issue_key), safe_str(summary), safe_str(status), safe_str(comment), safe_str(author_name), safe_str(time_spent), time_spent_seconds, time_spent_hours, time_spent_days, time_spent_weeks, time_spent_years, inactive, safe_str(worklog_created), safe_str(extraction_time)])
            else:
                csv_writer.writerow([safe_str(issue_key), safe_str(summary), safe_str(status), 'No work records found.', '', '', 0, 0, 0, 0, 0, 'No', '', safe_str(extraction_time)])

def process_tickets(url, username, token, project_key, start_range, end_range):
    jira = initialize_jira_connection(url, username, token)

    print(f"DEBUG: URL = {url}")
    print(f"DEBUG: Username = {username}")
    print(f"DEBUG: Token = {token}")
    print(f"DEBUG: Project Key = {project_key}")
    print(f"DEBUG: Start Range = {start_range}")
    print(f"DEBUG: End Range = {end_range}")

    last_ticket = fetch_latest_ticket(jira, project_key)
    if last_ticket:
        print(f"DEBUG: Last Ticket = {last_ticket['key']}")

    issues_list = fetch_issues(jira, project_key, start_range, end_range)
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'jira_data_{current_time}.csv'
    write_issues_to_csv(jira, issues_list, filename)
    print(f"Data written to {filename}")

    return filename
