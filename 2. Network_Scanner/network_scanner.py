#!/usr/bin/env python

import scapy.all as scapy
import argparse


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify Target IP,for more information use --help")
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    # broadcast.show()

    arp_request_broadcast = broadcast / arp_request
    # arp_request_broadcast.show()
    # answered, unanswered = scapy.srp(arp_request_broadcast, timeout=1)
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    answer = []
    for element in answered_list:
        answer.append({"IP": element[1].psrc, "MAC": element[1].hwsrc})
    return answer

    # print('<-------------------------------------------------------------->')
    # print(unanswered.summary())
    # print(arp_request.summary())
    # scapy.ls(scapy.ARP())


def print_result(answer_list):
    print("IP\t\t\tMAC ADDRESS\n-----------------------------------------")
    for element in answer_list:
        print(element["IP"] + "\t\t" + element["MAC"])


options = get_argument()
answered_list = scan(options.target)
print_result(answered_list)
