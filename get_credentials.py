# get OAuth credentials
from oauth2client import client, tools
from credentials  import scopes, store, creds

if __name__ == '__main__':
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('../google_credentials/client_secret.json', scopes)
        tools.run_flow(flow, store)
    else: print('already have credentials')
