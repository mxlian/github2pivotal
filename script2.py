#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Export your open github issues into a csv format for pivotal tracker import
"""
import csv
from pygithub3 import Github

# api settings for github
git_username = 'mxlian'
git_pass = 'put_your_password_here'
git_api_token = 'put_your_api_token_here'
git_repo = 'username/repo_name'

# import all issues as this story type
default_story_type = 'feature'

# csv name
csv_name = "open_git_hub_issues.csv"


def run_csv():
    pivotal_csv = csv.writer(open(csv_name, 'wb'), delimiter=',')
    #github = Github(username=git_username, api_token=git_api_token)
    github = Github(login=git_username, password=git_pass)

    # pivotals csv headers
    headers = [
        'Id',
        'Title',
        'Labels',
        'Type',
        'Estimate',
        'Current State',
        'Created At',
        'Accepted At',
        'Deadline',
        'Requested By',
        'Owned By',
        'Description',
        'Comment',
        'Comment'
    ]

    # write pivotals header rows
    pivotal_csv.writerow(headers)

    # get the git issues and write the rows to the csv
    git_issues = github.issues.list_by_repo(
        user='mscdev',
        repo='vtfx',
        state="open",
    )

    # print git_issues.all()

    for git_issue in git_issues.all():

        print "{0.number} {0.state} {0.created_at} - {0.title}".format(git_issue)


        labels = ','.join(l.name for l in git_issue.labels)
        if 'bug' in labels.lower():
            story_type = 'bug'
        else:
            story_type = default_story_type

        if git_issue.closed_at:
            accepted_at = git_issue.closed_at
            current_state = 'Accepted'
            estimate = '1'
        else:
            accepted_at = ''
            current_state = 'Unscheduled'
            estimate = '-1'

        # alot of these are blank because they are not really
        # needed but if you need them just fill them out
        story = [
            '',  # id
            git_issue.title.encode('utf-8', errors='replace'),  # title
            labels.encode('utf-8', errors='replace'),  # labels
            story_type,  # type:  Feature, Release, Bug, Chore, and Epic.
            estimate,  # estimate
            current_state,  # current state: Current State are Unscheduled (meaning the story is in the Icebox), Unstarted (i.e., in the Backlog), Planned (i.e., in Current for manually planned projects), Started, Finished, Delivered, Accepted, and Rejected
            git_issue.created_at,  # created at
            accepted_at,  # accepted at
            '',  # deadline
            '',  # requested by
            '',  # owned by
            git_issue.body.encode('utf-8', errors='replace'),  # description
            '',  # note 1
            '',  # note 2
        ]
        pivotal_csv.writerow(story)


if __name__ == '__main__':
    run_csv()
