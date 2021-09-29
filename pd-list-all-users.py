#!/opt/homebrew/bin/python3

import requests
import datetime
import csv

# add your pagerduty api key below (read-only is all that is needed)
apiKey = 'INSERT_YOUR_API_KEY_HERE'

# function to get all users via pagerduty api
def get_users(apiKey):

    offset = 0
    more = True
    users = []

    headers = {
    'Authorization': 'Token token=' + apiKey,
    'Accept': 'application/vnd.pagerduty+json;version=2',
    'Content-Type': 'application/json'
    }

    while (more == True):
        url = 'https://api.pagerduty.com/users?limit=100&offset=' + str(offset)

        response = requests.request('GET', url, headers=headers)

        users = users + response.json()['users']

        if (more == True):
            offset = offset + 100

        more = response.json()['more']

    return(users)

# function to get the active session of a user via pagerduty api
def get_active_user_session(apiKey, id):

    headers = {
    'Authorization': 'Token token=' + apiKey,
    'Accept': 'application/vnd.pagerduty+json;version=2',
    'Content-Type': 'application/json'
    }

    url = 'https://api.pagerduty.com/users/' + id + '/sessions'

    response = requests.request('GET', url, headers=headers)

    sessions = response.json()['user_sessions']

    return(sessions)

# function parse through functions and capture only data needed for report
def build_report_data(apiKey, users):
    userDetails = []
    roles = {
        'admin': 'Global Admin',
        'limited_user': 'Responder',
        'observer': 'Observer',
        'owner': 'Account Owner',
        'read_only_limited_user': 'Limited Stakeholder',
        'read_only_user': 'Stakeholder',
        'restricted_access': 'Restricted Access',
        'user': 'Manager'
    }

    for user in users:

            activeSessions = get_active_user_session(apiKey, user['id'])

            userDetails.append({'id': user['id'],
                        'name': user['name'],
                        'role': roles[user['role']],
                        'num_of_teams_user_is_on': len(user['teams']),
                        'num_of_active_sessions': len(activeSessions)
                        })

    return(userDetails)

# function export the report to csv
def create_csv(schedules):

    fileName = 'active_schedules' + datetime.datetime.now().strftime('_%Y-%m-%d') + '.csv'
    fields = ['id', 'name', 'role', 'num_of_teams_user_is_on', 'num_of_active_sessions']

    with open(fileName, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(schedules)


#  run the functions!
allUsers = get_users(apiKey)
reportData = build_report_data(apiKey, allUsers)
create_csv(reportData)