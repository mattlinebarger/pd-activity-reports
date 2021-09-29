#!/opt/homebrew/bin/python3

import requests
import datetime
import csv

# add your pagerduty api key below (read-only is all that is needed)
apiKey = 'INSERT_YOUR_API_KEY_HERE'

# function to get all services via pagerduty api
def get_services(apiKey):

    offset = 0
    more = True
    services = []

    headers = {
    'Authorization': 'Token token=' + apiKey,
    'Accept': 'application/vnd.pagerduty+json;version=2',
    'Content-Type': 'application/json'
    }

    while (more == True):
        url = 'https://api.pagerduty.com/services?limit=100&offset=' + str(offset)

        response = requests.request('GET', url, headers=headers)

        services = services + response.json()['services']

        if (more == True):
            offset = offset + 100

        more = response.json()['more']

    return(services)

# function parse through functions and capture only data needed for report
def build_report_data(services):
    serviceDetails = []

    for service in services:

        # adding a value if no incident has been created on the service
        if (service['last_incident_timestamp'] == None):
            lastIncTime = 'No incidents so far.'
        else:
            lastIncTime = service['last_incident_timestamp']

        serviceDetails.append({'id': service['id'],
                            'name': service['name'],
                            'status': service['status'],
                            'last_incident_timestamp': lastIncTime
                            })

    return(serviceDetails)

# function export the report to csv
def create_csv(services):

    fileName = 'active_services' + datetime.datetime.now().strftime('_%Y-%m-%d') + '.csv'
    fields = ['id', 'name', 'status', 'last_incident_timestamp']

    with open(fileName, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(services)


#  run the functions!
allServices = get_services(apiKey)
reportData = build_report_data(allServices)
create_csv(reportData)