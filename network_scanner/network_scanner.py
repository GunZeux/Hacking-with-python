#!usr/bin/env python

import scapy.all as scapy
import optparse


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-t","--target",dest="target",help="range of target ip")
    (options,args) = parser.parse_args()
    if not options.target:
        print("[-] Please specify Target ip range")
        exit(-1)
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broad = broadcast/arp_request
    answered_list = scapy.srp(arp_req_broad,timeout=1,verbose=False)[0]
    client_lst = []
    for ele in answered_list:
        client_dict = {"ip":ele[1].psrc, "mac":ele[1].hwsrc}
        client_lst.append(client_dict)

    return client_lst


def print_res(res_lst):
    print("_________________________________________")
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for ele in res_lst:
        print(ele["ip"] + "\t\t" + ele["mac"])


options = get_args()
scan_res = scan(options.target)
print_res(scan_res)