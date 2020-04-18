import json                 # reading in json file
import sys
import pprint
pp = pprint.PrettyPrinter() # pretty printing json data

def prettyPrint(fileName):
    data = json.load(open('../google_credentials/' + fileName))
    print('')
    pp.pprint(data)
    print('')

if __name__ == '__main__': 
    prettyPrint(sys.argv[1])
    prettyPrint(sys.argv[2])
