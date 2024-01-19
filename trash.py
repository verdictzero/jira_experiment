def write_issues_to_csv(jira, issues_list, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Adding new headers for work hours, days, weeks, years, and inactive status
        csv_writer.writerow(['Issue Key', 'Summary', 'Status', 'Worklog Comment', 'Author', 'Time Spent', 'Time Spent Converted', 'Work Hours', 'Work Days', 'Work Weeks', 'Work Months', 'Work Years', 'Inactive', 'Worklog Created', 'Data Extracted Time'])

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
                time_spent_days = time_spent_seconds / (3600 * 8) # 8 hours to account for work-day only
                time_spent_weeks = time_spent_seconds / (3600 * 8 * 5) # 5 days to account for work-week only
                time_spent_months = time_spent_seconds / (3600 * 160)
                time_spent_years = (time_spent_hours / 2000)

                inactive = "Yes" if "[X]" in author_name else "No"

                # Update the csv_writer.writerow() to include time_spent_months
                csv_writer.writerow([safe_str(issue_key), safe_str(summary), safe_str(status), safe_str(comment), safe_str(author_name), safe_str(time_spent), time_spent_seconds, time_spent_hours, time_spent_days, time_spent_weeks, time_spent_months, time_spent_years, inactive, safe_str(worklog_created), safe_str(extraction_time)])
        else:
            csv_writer.writerow([safe_str(issue_key), safe_str(summary), safe_str(status), 'No work records found.', '', '', 0, 0, 0, 0, 0, 0, 'No', '', safe_str(extraction_time)])
