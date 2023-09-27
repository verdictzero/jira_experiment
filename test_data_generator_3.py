import csv
from atlassian import Jira
from datetime import datetime, timedelta
import random
import requests
import sys

# Terminal color setup
GREEN = '\033[32m'
RESET = '\033[0m'
BG_BLACK = '\033[40m'

def print_green_on_black(message):
    sys.stdout.write(GREEN + BG_BLACK + message + RESET + '\n')

print_green_on_black("Initializing script...")

# Jira Configuration
JIRA_URL = 'https://defenestrate.atlassian.net'
JIRA_USER = 'verdict.zero@gmail.com'
JIRA_PASS = 'ATATT3xFfGF0mlrNZNButIwlwlR5A7FAf0nDyRFDlAoU5qHe1ORP9fqMLDu7Bh3YP9MI1-PSJZyAHmFT1Sv7-PqTXvajyURo14R2nQgk-V0ajK44RtLyhmEEgfEj0mgKYEXtnpKQOafO3nsoBWKToqE97uzwaPq55FTGqRNJMjVQuzUf3dIivOQ=5986C7DA'
PROJECT_KEY = 'TEST'
STATES = ['To Do', 'In Progress', 'Done']
WORDS = ["sample", "test", "demo", "random", "example", "data", "issue", "bug", "feature", "task"]

print_green_on_black("Configured Jira settings.")

def random_text(words, max_length):
    return ' '.join(random.choice(words) for _ in range(random.randint(1, max_length)))

# For authentication
auth = (JIRA_USER, JIRA_PASS)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

ticket_ids = []

print_green_on_black("Starting to create random tickets...")

# Create random tickets
for _ in range(10):  # Generate 10 tickets. Adjust as needed.
    summary = random_text(WORDS, 6)
    description = random_text(WORDS, 20)
    data = {
        "fields": {
            'project': {'key': PROJECT_KEY},
            'summary': summary,
            'description': description,
            'issuetype': {'name': 'Task'},
        }
    }
    response = requests.post(f"{JIRA_URL}/rest/api/2/issue", json=data, headers=headers, auth=auth)
    response.raise_for_status()
    issue = response.json()
    ticket_ids.append(issue['id'])
    print_green_on_black(f"Created ticket with ID: {issue['id']}")

print_green_on_black(f"{len(ticket_ids)} tickets created successfully.")

# Select a subset of the created tickets for adding worklogs and state transitions
selected_tickets = random.sample(ticket_ids, len(ticket_ids) // 2)

print_green_on_black("Starting to transition ticket states...")

# Randomly transition some of the tickets to different states
for ticket_id in ticket_ids:
    random_state = random.choice(STATES)
    try:
        jira.issue_transition(issue_id=ticket_id, state=random_state)
        print_green_on_black(f"Transitioned ticket {ticket_id} to state: {random_state}")
    except Exception:
        pass  # If the state transition is not possible, just ignore and continue

print_green_on_black("Ticket state transitions completed.")
print_green_on_black("Starting to generate random work logs...")

for ticket_id in selected_tickets:
    hours_logged = random.randint(1, 8)
    log_date = datetime.now() - timedelta(days=random.randint(0, 15))
    worklog_url = f"{JIRA_URL}/rest/api/2/issue/{ticket_id}/worklog"
    worklog_data = {
        "started": log_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+0000',
        "timeSpent": f"{hours_logged}h"
    }
    response = requests.post(worklog_url, json=worklog_data, headers=headers, auth=auth)
    response.raise_for_status()
    print_green_on_black(f"Added worklog to ticket {ticket_id} for {hours_logged} hours on {log_date.strftime('%Y-%m-%d')}.")

print_green_on_black("Worklogs created successfully!")
print_green_on_black("Script execution completed!")