#!/usr/bin/env python3


# developed by Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems


import requests
import json
import time
import urllib3
import utils
import logging

from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
from requests.auth import HTTPBasicAuth  # for Basic Auth

# BUGBUG - We need to clean this up so we don't use globals

DNAC_URL = 'https://my.dnac.tld'
DNAC_USER = 'user-with-read-rights'
DNAC_PASS = 'mypassword'

def get_dnac_jwt_token(dnac_auth):
    """NA C - /api/system
    Create the authorization token required to access DNA C
    Call to D/v1/auth/login
    :param dnac_auth - DNA C Basic Auth string
    :return: DNA C JWT token
    """

    url = DNAC_URL + '/dna/system/api/v1/auth/token'
    header = {'content-type': 'application/json'}
    response = requests.post(url, auth=dnac_auth, headers=header, verify=False)
    dnac_jwt_token = response.json()['Token']
    return dnac_jwt_token


def get_all_device_info(dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/api/v1/network-device'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    all_device_response = requests.get(url, headers=header, verify=False)
    all_device_info = all_device_response.json()
    return all_device_info['response']


def get_device_info(device_id, dnac_jwt_token):
    """
    This function will retrieve all the information for the device with the DNA C device id
    :param device_id: DNA C device_id
    :param dnac_jwt_token: DNA C token
    :return: device info
    """
    url = DNAC_URL + '/api/v1/network-device?id=' + device_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    device_response = requests.get(url, headers=header, verify=False)
    device_info = device_response.json()
    return device_info['response'][0]

def get_device_id_name(device_name, dnac_jwt_token):
    """
    This function will find the DNA C device id for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return:
    """
    device_id = None
    device_list = get_all_device_info(dnac_jwt_token)
    for device in device_list:
        if device['hostname'] == device_name:
            device_id = device['id']
    return device_id


def get_device_config(device_name, dnac_jwt_token):
    """
    This function will get the configuration file for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return: configuration file
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/network-device/' + device_id + '/config'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    config_json = response.json()
    config_file = config_json['response']
    return config_file

    # get the DNA Center JWT auth

def get_content_file_id(file_id, dnac_jwt_token):
    """
    This function will download a file specified by the {file_id}
    :param file_id: file id
    :param dnac_jwt_token: DNA C token
    :return: file
    """
    url = DNAC_URL + '/api/v1/file/' + file_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False, stream=True)
    response_json = response.json()
    return response_json

def check_task_id_output(task_id, dnac_jwt_token):
    """
    This function will check the status of the task with the id {task_id}. Loop one seconds increments until task is completed
    :param task_id: task id
    :param dnac_jwt_token: DNA C token
    :return: status - {SUCCESS} or {FAILURE}
    """
    url = DNAC_URL + '/api/v1/task/' + task_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    completed = 'no'
    while completed == 'no':
        try:
            task_response = requests.get(url, headers=header, verify=False)
            task_json = task_response.json()
            task_output = task_json['response']
            completed = 'yes'
        except:
            time.sleep(1)
    return task_output

def get_output_command_runner(command, device_name, dnac_jwt_token):
    """
    This function will return the output of the CLI command specified in the {command}, sent to the device with the
    hostname {device}
    :param command: CLI command
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return: file with the command output
    """

    # get the DNA C device id
    device_id = get_device_id_name(device_name, dnac_jwt_token)

    # get the DNA C task id that will process the CLI command runner
    payload = {
        "commands": [command],
        "deviceUuids": [device_id],
        "timeout": 0
        }
    url = DNAC_URL + '/api/v1/network-device-poller/cli/read-request'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    response_json = response.json()
    task_id = response_json['response']['taskId']

    # get task id status
    time.sleep(1)  # wait for a second to receive the file name
    task_result = check_task_id_output(task_id, dnac_jwt_token)
    print(task_result)
    file_info = json.loads(task_result['progress'])
    file_id = file_info['fileId']

    # get output from file
    time.sleep(2)  # wait for two seconds for the file to be ready
    file_output = get_content_file_id(file_id, dnac_jwt_token)
    command_responses = file_output[0]['commandResponses']
    if command_responses['SUCCESS'] is not {}:
        command_output = command_responses['SUCCESS'][command]
    elif command_responses['FAILURE'] is not {}:
        command_output = command_responses['FAILURE'][command]
    else:
        command_output = command_responses['BLACKLISTED'][command]
    return command_output


def get_config_from_cdnac():

# BUGBUG - we really need to make this secure and just disable warnings
    urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

    DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)
    dnac_jwt_auth = get_dnac_jwt_token(DNAC_AUTH)
    #print('\nThe DNA Center Auth JWT is: ', dnac_jwt_auth)


# retrieve all managed devices info

    all_devices_info = get_all_device_info(dnac_jwt_auth)
#print('The information for all Cisco DNA Center managed devices is: ')
#print(all_devices_info)

#device_name = '3650-SDA1'
#device_config = get_device_config(device_name, dnac_jwt_auth)
#print('The configuration for 3650-SDA1 devices is: ')
#print(device_config)
#temp_run_config = 'temp_run_config.txt'

#print('Creating configuration file: ')
    all_devices_hostnames = []
    all_configs = []
    for device in all_devices_info:
        all_devices_hostnames.append(device['hostname'])
    for device in all_devices_hostnames:
        device_config = get_device_config(device, dnac_jwt_auth)
        device_dict  = {}
        device_dict["hostname"] = device
        device_dict["config"] = device_config.splitlines()
        all_configs.append(device_dict)
    return all_configs
#    print(str(device) + '_config.txt')
#    filename = str(device) + '_config.txt'
#    f_temp = open(filename, 'w')
#    f_temp.write(device_config)
#    f_temp.seek(0)  # reset the file pointer to 0
#    f_temp.close()
