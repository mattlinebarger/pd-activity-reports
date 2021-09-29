#!/opt/homebrew/bin/python3

import requests
import datetime
import csv

# add your pagerduty api key below (read-only is all that is needed)
apiKey = 'INSERT_YOUR_API_KEY_HERE'

# function to get all schedules via pagerduty api
def get_schedules(apiKey):

    offset = 0
    more = True
    schedules = []

    headers = {
    'Authorization': 'Token token=' + apiKey,
    'Accept': 'application/vnd.pagerduty+json;version=2',
    'Content-Type': 'application/json'
    }

    while (more == True):
        url = 'https://api.pagerduty.com/schedules?limit=100&offset=' + str(offset)

        response = requests.request('GET', url, headers=headers)

        schedules = schedules + response.json()['schedules']

        if (more == True):
            offset = offset + 100

        more = response.json()['more']

    return(schedules)

# function parse through functions and capture only data needed for report
def build_report_data(schedules):
    scheduleDetails = []

    for schedule in schedules:

            scheduleDetails.append({'id': schedule['id'],
                        'name': schedule['name'],
                        'num_of_eps_used': len(schedule['escalation_policies']),
                        'num_of_users': len(schedule['users'])
                        })

    return(scheduleDetails)

# function export the report to csv
def create_csv(schedules):

    fileName = 'active_schedules' + datetime.datetime.now().strftime('_%Y-%m-%d') + '.csv'
    fields = ['id', 'name', 'num_of_eps_used', 'num_of_users']

    with open(fileName, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(schedules)


#  run the functions!
allSchedules = get_schedules(apiKey)
# print(allSchedules)
reportData = build_report_data(allSchedules)
create_csv(reportData)