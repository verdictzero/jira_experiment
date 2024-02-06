import csv
import re
from datetime import datetime
from atlassian import Jira
import traceback2 as traceback
from colorama import Fore, Style, init

# Initialize colorama
init()

def safe_str(obj):
    try:
        return str(obj)
    except UnicodeEncodeError:
        return obj.encode('ascii', 'replace').decode('ascii')

def convert_time_to_seconds(time_str):
    # A work day is 8 hours and a work week is 5 days
    time_units = {'w': 5 * 8 * 3600, 'd': 8 * 3600, 'h': 3600, 'm': 60, 's': 1}
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
            print(Style.BRIGHT + Fore.YELLOW + "No tickets found in the project." + Style.RESET_ALL)
            return None
    except Exception as e:
        print(Style.BRIGHT + Fore.RED + f"Error fetching tickets: {e}" + Style.RESET_ALL)
        traceback.print_exc()
        return None

def fetch_issues(jira, project_key, start_range, end_range):
    issues_list = []
    for i in range(start_range, end_range + 1):
        issue_key = f"{project_key}-{i}"
        try:
            # Attempt to expand the issue to include the changelog
            issue = jira.issue(issue_key, expand='changelog')
            issues_list.append(issue)
            print(issue['key'], issue['fields']['summary'])
        except Exception as e:
            print(Style.BRIGHT + Fore.YELLOW + f"Could not fetch issue {issue_key}. Error: {e}" + Style.RESET_ALL)
            # traceback.print_exc()

    # ---- DEBUG ----
    print("\n\n------- DEBUG VERBOSE OUTPUT -------\n\n")
    for issue in issues_list:
        issue_key = issue.get('key', 'No Key Found')
        summary = issue['fields'].get('summary', 'No Summary Found')
        status = issue['fields']['status'].get('name', 'No Status Found')
        # Attempt to print some changelog information for debugging
        if 'changelog' in issue:
            print(f"Issue Key: {issue_key}, Summary: {summary}, Status: {status}, Changelog Entries: {len(issue['changelog']['histories'])}")
        else:
            print(f"Issue Key: {issue_key}, Summary: {summary}, Status: {status}, Changelog: Not Retrieved")
    # ---- END DEBUG ----

    return issues_list

def write_issues_to_csv(jira, issues_list, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Remove 'Closed Datetime' and include headers for worklog details
        csv_writer.writerow([
            'Issue Key', 'Summary', 'Status', 'Labels', 'Worklog Comment', 'Author', 
            'Time Spent', 'Time Spent Converted', 'Work Hours', 'Work Days', 'Work Weeks', 
            'Work Months', 'Work Years', 'Inactive', 'Worklog Created', 'Data Extracted Time', 
            'Created', 'Closed Status Set On'
        ])

        for issue in issues_list:
            issue_key = issue['key']
            summary = issue['fields']['summary']
            status = issue['fields']['status']['name']
            labels = ', '.join(issue['fields'].get('labels', []))
            created = issue['fields']['created']

            # Initialize variable for when the status was set to Closed, if applicable
            closed_status_set_on = '' 
            
            # Process the changelog to find when the issue was set to Closed status, if present
            if 'changelog' in issue:
                for history in issue['changelog'].get('histories', []):
                    for item in history.get('items', []):
                        if item.get('field') == 'status' and item.get('toString') == 'Closed':  # Adjust condition as needed
                            closed_status_set_on = history.get('created')
                            break  # Break after finding the first occurrence
                    if closed_status_set_on:  # If found, no need to search further
                        break
            
            # Fetch and process all worklogs for the issue
            worklogs_response = jira.get(f"rest/api/2/issue/{issue_key}/worklog")
            worklogs = worklogs_response.get('worklogs', [])
            if worklogs:
                for worklog in worklogs:
                    comment = worklog.get('comment', "No worklog comment.")
                    author_name = worklog['author']['displayName']
                    time_spent = worklog['timeSpent']
                    worklog_created = worklog['started']

                    time_spent_seconds = convert_time_to_seconds(time_spent)
                    time_spent_hours = time_spent_seconds / 3600
                    time_spent_days = time_spent_seconds / (3600 * 8)
                    time_spent_weeks = time_spent_seconds / (3600 * 8 * 5)
                    time_spent_months = time_spent_seconds / (3600 * 160)
                    time_spent_years = time_spent_hours / (2000)  # Example conversion, adjust as needed

                    inactive = "Yes" if "[X]" in author_name else "No"

                    # Write each worklog entry for the issue to the CSV
                    csv_writer.writerow([
                        safe_str(issue_key), safe_str(summary), safe_str(status), safe_str(labels), 
                        safe_str(comment), safe_str(author_name), safe_str(time_spent), 
                        time_spent_seconds, time_spent_hours, time_spent_days, time_spent_weeks, 
                        time_spent_months, time_spent_years, inactive, safe_str(worklog_created), 
                        datetime.now().isoformat(), safe_str(created), safe_str(closed_status_set_on)
                    ])
            else:
                # If no worklogs are found, write issue details with placeholders for worklog-specific fields
                csv_writer.writerow([
                    safe_str(issue_key), safe_str(summary), safe_str(status), safe_str(labels), 
                    'No worklog comment.', '', '', '', '', '', '', '', '', 'No', '', 
                    datetime.now().isoformat(), safe_str(created), safe_str(closed_status_set_on)
                ])

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

    # Print bold red text
    print(Style.BRIGHT + Fore.GREEN + f"[ Creating {filename} ]")
    print(Style.BRIGHT + Fore.RED + "[ !!! THIS IS GOING TO TAKE A WHILE !!! ]" + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.RED + "[ !!! -- DO NOT CLOSE THIS WINDOW -- !!! ]" + Style.RESET_ALL)
    
    write_issues_to_csv(jira, issues_list, filename)

    print(f"Data written to {filename}")

    return filename
