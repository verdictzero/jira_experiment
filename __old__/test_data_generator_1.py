import csv
from atlassian import Jira
from datetime import datetime, timedelta
import random
import requests

jira = Jira

# Jira Configuration
JIRA_URL = 'https://defenestrate.atlassian.net'
JIRA_USER = 'verdict.zero@gmail.com'
JIRA_PASS = 'ATATT3xFfGF0mlrNZNButIwlwlR5A7FAf0nDyRFDlAoU5qHe1ORP9fqMLDu7Bh3YP9MI1-PSJZyAHmFT1Sv7-PqTXvajyURo14R2nQgk-V0ajK44RtLyhmEEgfEj0mgKYEXtnpKQOafO3nsoBWKToqE97uzwaPq55FTGqRNJMjVQuzUf3dIivOQ=5986C7DA'
PROJECT_KEY = 'TEST'
STATES = ['To Do', 'In Progress', 'Done']
WORDS = ["sample", "test", "demo", "random", "example", "data", "issue", "bug", "feature", "task"]

def random_text(words, max_length):
    return ' '.join(random.choice(words) for _ in range(random.randint(1, max_length)))

# For authentication
auth = (JIRA_USER, JIRA_PASS)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

ticket_ids = []

# Create random tickets
for _ in range(10):  # Generate 10 tickets. Adjust as needed.
    summary = random_text(WORDS, 6)
    description = random_text(WORDS, 20)
    data = {
        "fields": {
            'project': {'key': PROJECT_KEY},
            'summary': summary,
            'description': description,
            'issuetype': {'name': 'Task'},  # Assuming a Task. Adjust as per your project settings.
        }
    }

    response = requests.post(f"{JIRA_URL}/rest/api/2/issue", json=data, headers=headers, auth=auth)
    response.raise_for_status()
    issue = response.json()
    ticket_ids.append(issue['id'])

# Randomly transition some of the tickets to different states
for ticket_id in ticket_ids:
    random_state = random.choice(STATES)
    try:
        jira.issue_transition(issue_id=ticket_id, state=random_state)
    except Exception:
        pass  # If the state transition is not possible, just ignore and continue

from atlassian import Jira

jira = Jira(
    url=JIRA_URL,
    username=JIRA_USER,
    password=JIRA_PASS
)

# Generate random work logs for a subset of tickets
selected_tickets = random.sample(ticket_ids, len(ticket_ids) // 2)  # Selecting half of the tickets

for ticket_id in selected_tickets:
    hours_logged = random.randint(1, 8)
    log_date = datetime.now() - timedelta(days=random.randint(0, 15))
    jira.add_worklog(issue_id=ticket_id, time_spent=f"{hours_logged}h", started=log_date)

print("Tickets and worklogs created!")
