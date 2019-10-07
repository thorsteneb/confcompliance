#!/usr/bin/env python3

from ciscoconfparse import CiscoConfParse
import json
import csv
import argparse
import pprint
import getconfig

def rule_test(rule, config):
    name = rule['name']
    presence = rule['presence']
    command = rule['command']
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

    all_cmds = config.find_objects(r"^" + command)
    if presence and not all_cmds:
        detail_result.append(failmsg)
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
                        return False
                else:
                    if presence:
                        detail_result.append(failmsg + ", with command: " + cmd.text)
                        return False
                    else:
                        detail_result.append(passmsg)
                        return True
            if presence:
                detail_result.append(passmsg)
                return True
            else:
                detail_result.append(failmsg + ", with command: " + cmd.text)
                return False


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("rulesfile")
    args = parser.parse_args()

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
        for rule in rules['Rules']:
        #config = ['telnet server enabled','username networkus privilege 15 common-criteria-policy sanpasscomplex secret 5 $1$.nZp$CTnRQGYhnX.rW5BCGCRaw0']
            #Check for rule and append to output
            if rule_test(rule, parse) == False:
                passed = False

        entry = []
        if passed:
            entry.append("Test of device " + config["hostname"] + " , device PASSED")
        else:
            entry.append("Test of device " + config["hostname"] + " , device FAILED")
        entry.append("-----")
        entry.extend(detail_result)
        entry.append("-----")
        entry.append("")
        result.append(entry)

    pp = pprint.PrettyPrinter(width=120)
    pp.pprint (result)

    resultcsv = "compliance-check.csv"
    with open(resultcsv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(result)
    print("Compliance check results are in " + resultcsv)

if __name__ == '__main__':
    #BUGBUG There has to be a better way than using globals
    result = []
    detail_result = []
    main()
