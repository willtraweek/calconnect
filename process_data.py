import subprocess
import json
import csv

data = {
        'host': 'mitchellmorrison57@gmail.com',
        'emails': ['lephuocdinh99@gmail.com'],
        'duration': 45,
        'description': "info about the event"
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
    subprocess.call(['./schedule', 'meetings.txt', '--schedule', '--calendar', data['host']])


process_data(data)
