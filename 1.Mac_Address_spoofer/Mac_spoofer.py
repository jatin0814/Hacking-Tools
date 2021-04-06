#for linux
#!/usr/bin/env python

import subprocess
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface name")
    parser.add_option("-m", "--mac", dest="new_mac_add", help="new MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify interface,for more help use --help")
    elif not options.new_mac_add:
        parser.error("[-] Please specify new mac,for more help use --help")
    return options


def Change_mac(interface, new_mac_add):
    print("[+] Changing mac address of interface " + interface + " to " + new_mac_add)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_add])
    subprocess.call(["ifconfig", interface, "up"])


options = get_arguments()
Change_mac(options.interface, options.new_mac_add)
