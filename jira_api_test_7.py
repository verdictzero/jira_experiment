from atlassian import Jira

jira = Jira(
    url='https://defenestrate.atlassian.net',
    username='verdict.zero@gmail.com',
    password='ATATT3xFfGF0RJRtazGOAYhBTV6utKJ3dxe8zWxgsUYgziNrLDpaqXGCu-2soOyxfMOgDu774CyRQfTk-WWTa7CyCdtIaKP8XmzGs57AEo67uW5xHI64b3bc1-H2Vdm51AlpC34W4Grd9wlGQYzO0Zpv-jlTyC7ovVmPqLP6HVsA3GsNS_dnXSA=B38CE11C'
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

# Loop through the fetched issues to extract work logs
for issue in issues_list:
    issue_key = issue['key']
    print(f"\n{issue_key} {issue['fields']['summary']}")
    
    worklogs_response = jira.get(f"rest/api/2/issue/{issue_key}/worklog")
    worklogs = worklogs_response.get('worklogs', [])
    
    if worklogs:
        for worklog in worklogs:
            comment = worklog.get('comment', "No comment provided.")
            author_name = worklog['author']['displayName']
            time_spent = worklog['timeSpent']
            print(f"    + {comment} (Logged by: {author_name}, Time spent: {time_spent})")
    else:
        print("    - No work records found.")