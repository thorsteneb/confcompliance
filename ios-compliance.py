#!/usr/bin/env python3

from ciscoconfparse import CiscoConfParse
import json
import csv
import argparse
import pprint
import getconfig
import logging.handlers

def rule_test(rule, config):

# Setting the rule's attiributes
    name = rule['name']
    presence = rule['presence']
    command = rule['command']
    severity = rule['severity']
    if 'child' in rule:
        child = rule['child']
    else:
        child = None
    if 'value' in rule:
        value = rule['value']
    else:
        value = None
    failmsg = rule['failmsg']
    passmsg = rule['passmsg']
    global highestSeverity

#  Testing the config agaist the rule
    all_cmds = config.find_objects(r"^" + command)
    if presence and not all_cmds:
        detail_result.append(failmsg + " Severity: " + str(severity))
        if highestSeverity<severity:
            highestSeverity = severity
        return False
    elif not presence and not all_cmds:
        detail_result.append(passmsg)
        return True

    for cmd in all_cmds:
        #BUGBUG - This mess of ifs should be cleaned up - how?
        if child:
            print ("not yet implemented")
            #if cmd.re_search_children(r"^" + child):
                # if value and value ==
                # BUGBUG - add child processing
        else:
            if value:
                if cmd.text.find(value) != -1:
                    if presence:
                        detail_result.append(passmsg)
                        return True
                    else:
                        detail_result.append(failmsg + ", with command: " + cmd.text)
                        if highestSeverity<severity:
                            highestSeverity = severity
                        return False
                else:
                    if presence:
                        detail_result.append(failmsg + ", with command: " + cmd.text)
                        if highestSeverity<severity:
                            highestSeverity = severity
                        return False
                    else:
                        detail_result.append(passmsg)
                        return True
            if presence:
                detail_result.append(passmsg)
                return True
            else:
                detail_result.append(failmsg + ", with command: " + cmd.text)
                if highestSeverity<severity:
                    highestSeverity = severity
                return False


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Cisco IOS Compliance Check')
    parser.add_argument("--rulesfile", type=str, help='Please enter the filename for compliance rules is JSON format')
    parser.add_argument("--syslog_ip", help="[Optional] Please enter the IP address of the syslog server")
    parser.add_argument('--syslog_port', help="[Optional] Please enter the UDP of the syslog server, default port is 514", type=int, default=514)
    args = parser.parse_args()

    # Arguments verification:
    if args.rulesfile is None:
        raise Exception("Sorry, no rules file is set")

    # Read in json file containing rules
    # BUGBUG - This urgently needs input validation
    if args.rulesfile:
        with open(args.rulesfile, "r") as f:
            rules = json.load(f)

    #Get all device configs and iterate through them
    all_configs = getconfig.get_config_from_cdnac()
    for config in all_configs:
        parse = CiscoConfParse(config["config"])
        # Iterate through rules
        del detail_result[:]
        passed = True
        global highestSeverity
        highestSeverity = 0
        for rule in rules['Rules']:
        #config = ['telnet server enabled','username networkus privilege 15 common-criteria-policy sanpasscomplex secret 5 $1$.nZp$CTnRQGYhnX.rW5BCGCRaw0']
            #Check for rule and append to output
            if rule_test(rule, parse) == False:
                passed = False

        entry = []
        if passed:
            entry.append("Test of device " + config["hostname"] + ", device PASSED")
        else:
            entry.append("Test of device " + config["hostname"] + ", device FAILED, severity " + str(highestSeverity))
        entry.append("-----")
        entry.extend(detail_result)
        entry.append("-----")
        entry.append("")
        result.append(entry)

    pp = pprint.PrettyPrinter(width=120)
    pp.pprint (result)

# Exporting results to a CSV file

    resultcsv = "compliance-check.csv"
    with open(resultcsv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(result)
    print("Compliance check results are in " + resultcsv)

# Setting and sending results via syslog
    if args.syslog_ip:
# Creating the logger
        syslog_logger = logging.getLogger('syslog_logger')
        syslog_logger.setLevel(logging.INFO)

# Creating the logging handler, directing to the syslog server
        handler = logging.handlers.SysLogHandler(address=(args.syslog_ip,514))
        syslog_logger.addHandler(handler)

# Sending the results via syslog
        for res in result:
            syslog_logger.info(res)

if __name__ == '__main__':
    #BUGBUG There has to be a better way than using globals
    result = []
    detail_result = []
    highestSeverity = 0
    main()
