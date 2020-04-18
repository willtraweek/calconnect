# get OAuth credentials
from oauth2client import client, tools
from credentials  import scopes, store, creds

def main():
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('../google_credentials/client_secret.json', scopes)
        print('got here')
        tools.run_flow(flow, store)
        return
    else: 
        print('already have credentials')


if __name__ == '__main__':
    main()
