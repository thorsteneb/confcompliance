# confcompliance
## Cisco DNA Center / IOS Config Compliance tool
This is a proof of concept, not a full featured tool. Created during SEVT Hackathon.
This code will pull all device configurations from Cisco DNA Center's inventory, and check configuration against compliance rules formatted in json.

* Technology stack: Python
* Status:  Alpha, designed to prove the ability and openess of Cisco DNA Center.

## How to setup
### Cisco DNA-C
#### Prerequisites
* Enable Cisco DNA-C as a Platform
  * How-To Guide https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/dna-center-platform/1-2-5/user_guide/b_dnac_platform_ug_1_2_5/b_dnac_platform_ug_1_2_5_chapter_01.html
* Enable "DNA Center REST API" Bundle

## How to run
```
python ios-compliance.py --rulesfile <JSON rule file> --syslog_ip <IP address of the syslog server> --syslog_port <syslog port, if not 514>
```
* rulesfile - path to the JSON file containing the compliance rules.
* syslog_ip - IP address of a syslog server (optional) to send the results to.
* syslog_port - In case the syslog server is listening to a port other than 514 - specify which

## Licensing info
Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
