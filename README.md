# confcompliance
## Cisco DNA Center / IOS Config Compliance tool
Configuration Compliance Manager for Cisco DNA Center

This is currently a proof of concept, not a full featured tool. Created during SEVT Hackathon.
This code will pull all device configurations from Cisco DNA Center's inventory, and check configuration against compliance rules formatted in json.

* Technology stack: Python
* Status:  Alpha, designed to prove the ability and openess of Cisco DNA Center.

## Business/Technical Challenge

Customers need a way to prove configuration compliance for IOS / IOS-XE / IOS-XR / NX-OS devices. These devices may very well be Brownfield and while they are imported into Cisco DNA Center, are not provisioned by Cisco DNA Center. Because of this brownfield requirement, a separate tool is desirable, even as Cisco DNA Center is roadmapped to receive configuration compliance features for devices that are provisioned by CDNAC.

Customers need a way to write their own rules for configuration compliance, and have them vetted against running configuration on a schedule and generate a report, by site and device type / device tag.


## Proposed Solution

A Python program that verifies devices against compliance rules. Compliance rules are defined in JSON, as are device groups. The program pulls device inventory from CDNAC, matches compliance rules per device group (defined by site, type, tag), and reports on, and possibly alerts on, compliance violation, with a severity that is defined in the compliance rules.


The current PoC needs to be expanded to include:
- Better backend logic, expand compliance rules and introduce device rules
- Refactor to use CDNAC SDK
- Severity and syslog implemented as a first pass
- CSV to JSON converter
- Web frontend
- Reporting
- Alerting


### Cisco Products Technologies/ Services


Our solution will levegerage the following Cisco technologies

* [DNA Center (DNA-C)](http://cisco.com/go/dna)

## Team Members


* Thorsten Behrens <tbehrens@cisco.com> - GES NE Americas
* Jorge Banegas <jbanegas@cisco.com> - GVE DevOps / CSAP
* Oren Brigg <obrigg@cisco.com> - GEO Israel - Data Center AF
* Tomer Kopel <tkopel@cisco.com> - GEO Israel - Shared
* Alif Mousa <alimousa@cisco.com> - APO - Engineering - HQ
* Mentor: Gabi Zapodeanu <gzapodea@cisco.com> - ENB - TME


## Solution Components


- Python + Flash
- CDNAC SDK
- ciscoconfparse
- FrontEnd TBD - could be Bootstrap or Heroku, depending on team skillset and agile direction
- Docker TBD - if time allows, docker-compose would make deployment of the tool very easy

## Usage

```
python ios-compliance.py --rulesfile <JSON rule file> --syslog_ip <IP address of the syslog server> --syslog_port <syslog port, if not 514>
```
* rulesfile - path to the JSON file containing the compliance rules.
* syslog_ip - IP address of a syslog server (optional) to send the results to.
* syslog_port - In case the syslog server is listening to a port other than 514 - specify which


## Installation

Currently, to be amended as project progresses:
- Install Git
- Install Python 3 / Pip 3
- Pull project from github
- ```pip3 install -r requirements.txt```

## Documentation

* [The data model](./hackathon_data_model.txt), to be expanded for better compliance rules and device groups.
* [Sample compliance rules](./secrules.json) for reference.


## License

Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE.md)

## Code of Conduct

Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing

See our contributing guidelines [here](./CONTRIBUTING.md)
