#!/opt/homebrew/bin/python3

import requests
import datetime
import csv

# add your pagerduty api key below (read-only is all that is needed)
apiKey = 'INSERT_YOUR_API_KEY_HERE'

# function to get all escalation policies via pagerduty api
def get_eps(apiKey):

    offset = 0
    more = True
    eps = []

    headers = {
    'Authorization': 'Token token=' + apiKey,
    'Accept': 'application/vnd.pagerduty+json;version=2',
    'Content-Type': 'application/json'
    }

    while (more == True):
        url = 'https://api.pagerduty.com/escalation_policies?limit=100&offset=' + str(offset)

        response = requests.request('GET', url, headers=headers)

        eps = eps + response.json()['escalation_policies']

        if (more == True):
            offset = offset + 100

        more = response.json()['more']

    return(eps)

# function parse through functions and capture only data needed for report
def build_report_data(eps):
    epDetails = []

    for ep in eps:

            epDetails.append({'id': ep['id'],
                        'name': ep['name'],
                        'num_of_services_used': len(ep['services'])
                        })

    return(epDetails)

# function export the report to csv
def create_csv(eps):

    fileName = 'active_eps' + datetime.datetime.now().strftime('_%Y-%m-%d') + '.csv'
    fields = ['id', 'name', 'num_of_services_used']

    with open(fileName, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(eps)


#  run the functions!
allEps = get_eps(apiKey)
reportData = build_report_data(allEps)
create_csv(reportData)