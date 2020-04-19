import subprocess
import json
import csv

start_date = '2020-04-22'
data = {
        'host': 'lephuocdinh99@gmail.com',
        'emails': ['mitchellmorrison57@gmail.com', 'jim.erso.prescott@gmail.com'],
        'duration': 60,
        'description': "test event",
        'start_date': start_date
    }


def process_data(data):
    "format data from dictionary and set creds to credentials"

    # set credentials to a JSON file called credentials.txt
    # get_credentials should navigate back a directory outside the local folder and get creds
    # with open('../cred/credentials.json', 'w') as json_file:
    #     json.dumps(credentials, json_file)

#    prints all necesssary data to meetings.txt for running script
    f = open("meetings.txt", 'w')
    f.write("[" + str(data['duration']) + "] " + data['description'] + ": ")
    # f.write(data['host'] + ", ")
    f.write(', '.join(str(i) for i in data['emails']) + '\n')
    f.close()

#    run subsystem process to run the whole code
    subprocess.call(['./schedule', data['start_date'], 'meetings.txt', '--schedule', '--calendar', data['host']])
    # subprocess.call(['./schedule', data['start_date'], 'meetings.txt', '--calendar', data['host']])


process_data(data)
