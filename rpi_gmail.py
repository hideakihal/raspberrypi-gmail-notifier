#! /usr/bin/env python

from __future__ import print_function

import httplib2
import os
import oauth2client
import json
import RPi.GPIO as GPIO
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def led_init(gpio_num):
    GPIO.setup(gpio_num, GPIO.OUT)	# set GPIO5 output

	
def led_on(gpio_num):
    GPIO.output(gpio_num, GPIO.HIGH)	# LED ON

	
def led_off(gpio_num):	
    GPIO.output(gpio_num, GPIO.LOW)	# LED OFF


def flash_led():
    #Flashing number of times
    FLASH_LED_NUM = 10 

    #start
    GPIO.setmode(GPIO.BCM)		# use GPIO Number

    
    gpio_num = 5			# gpio_num --> GPIO5
    led_init(gpio_num)

    for i in range(FLASH_LED_NUM):
        led_on(gpio_num)
        time.sleep(0.5)

        led_off(gpio_num)
        time.sleep(0.5)

    GPIO.cleanup()


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_mail_list(service, user, qu):
    try:
        return service.users().messages().list(userId=user,q=qu).execute() 
    except errors.HttpError, error:
        pass 


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    query = "from: darjeeling42@gmail.com is:unread"

    results = get_mail_list(service, 'me', query) 
    print( json.dumps(results, indent=4))
    if results[u'resultSizeEstimate'] == 0:
        print ('not exist unrad mail')
    else:
        print ('exist unread mail')
        flash_led()

if __name__ == '__main__':
    main()
