"""
Implement AT API functionality.

Author: Doug
Created: 23/09/2018
"""

import os
# import sys
# from pathlib import path
# import os.path
import requests
import json

import gzip

import time


F_CREDENTIALS = '.api-key'
AT_BASE_URL = 'https://api.at.govt.nz/v2/'
AT_VEHICLE_LOCATIONS = AT_BASE_URL + 'public/realtime/vehiclelocations'
AT_BUS_ROUTES = 'https://api.at.govt.nz/v2/gtfs/routes'
BASE_DIR = os.getcwd()
FILE_JSON_GZ = os.path.join(BASE_DIR, 'data', 'atdata10_json.gz')

XR = 100
IR = 60


def get_key():
    """Load key from credentials file"""

    with open(F_CREDENTIALS) as f:
        api_key = f.readline()

    return api_key


def get_bus_locations(api_key):
    """Retrieve bus location from the AT API"""

    try:
        response = requests.get(AT_VEHICLE_LOCATIONS, headers={
            'Ocp-Apim-Subscription-Key': get_key()})
    except Exception as e:
        print('Error retrieving data from API:', e)
        raise e

    return response.json()


if __name__ == '__main__':
    for x in range(XR):
        for i in range(IR):
            # print(get_key())
            current_locations = get_bus_locations(get_key())

            # print(current_locations)
            print("Loop "+str(x*XR+i+1)+" API status is: " +
                  current_locations['status'])
            print("    Header time: " +
                  str(current_locations['response']['header']['timestamp']))
            # print("Error status is: " + str(current_locations['error']))
            # print(str(next(iter(current_locations))))
            # print(json.dumps(current_locations, indent=2, sort_keys=True))
            # for k in current_locations['response']['entity']:
            #     print(k)
            # print("Response headers: " +
            #   str(current_locations['response']['header']))
            with gzip.GzipFile(FILE_JSON_GZ, 'a') as outfile:
                str_ = json.dumps(current_locations['response'], indent=4,
                                  sort_keys=True, separators=(',', ': '),
                                  ensure_ascii=False)
                outfile.write(str_.encode('utf-8'))
            time.sleep(20)

            # with gzip.GzipFile(FILE_JSON_GZ, 'r') as infile:
            #     json_bytes = infile.read()
            # json_str = json_bytes.decode('utf-8')
            # read_data = json.loads(json_str)
            # print(read_data)
        outfile.close()
        print("Finished inner loop")
        time.sleep(4)
    print("Finished this run")
