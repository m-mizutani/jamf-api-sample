#!/usr/bin/env python

#
# Document: https://ckpd.jamfcloud.com/uapi/doc/
#
# [Prerequisite]
# Set environment variables from your JAMF account
#
# - JAMF_USER: Jamf username
# - JAMF_PASS: Jamf password
# - ENDPOINT:  API endpoint URL, e.g. https://xxx.jamfcloud.com/uapi

import requests
import os
import json


ENDPOINT = os.environ['ENDPOINT']


def get_token(username, password):
    token_url = '{}/auth/tokens'.format(ENDPOINT)
    hdr = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
    
    res = requests.post(token_url, headers=hdr, auth=(username, password))
    if res.status_code != 200:
        raise Exception('Unexpected response code: {}'.format(res.status_code))

    # token will expires in 30 min
    return res.json().get('token')


def main():
    username = os.environ.get('JAMF_USER')
    password = os.environ.get('JAMF_PASS')
    if not username or not password:
        raise Exception('Env var, JAMF_USER and JAMF_PASS are required')

    token = get_token(username, password)

    hdr = {
        'Accept': 'application/json',
        'Authorization': 'jamf-token {}'.format(token),
    }

    url = '{}/user'.format(ENDPOINT)
    res = requests.get(url, headers=hdr)
    print(json.dumps(res.json(), indent=4))


if __name__ == '__main__':
    main()
