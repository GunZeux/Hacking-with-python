#!/usr/bin/env python

import subprocess
import optparse
import re

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address")
    (options,args) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify interface, use --help for more info")
        exit(-1)
    if not options.new_mac:
        parser.error("[-] Please specify new MAC address, use --help for more info")
        exit(-1)
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_mac(interface):
    ifconfig_res = subprocess.check_output(["ifconfig", interface])
    mac_addr_res = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_res)

    if mac_addr_res:
        return mac_addr_res.group(0)
    else:
        print("[-] Could not Read MAC address")

options = get_args()
curr_mac = get_mac(options.interface)
print("Current MAC = " + str(curr_mac))

change_mac(options.interface,options.new_mac)

curr_mac = get_mac(options.interface)
if curr_mac == options.new_mac:
    print("[+] MAC address was successfully changed to "+ curr_mac)
else:
    print("[-] MAC address was not successfully changed\nCurrant MAC = "+curr_mac)