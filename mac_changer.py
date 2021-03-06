#!/usr/bin/env python

import subprocess  # The subprocess module allows to execute system commands
import optparse  # allows arguments from user, parse & use them in our code
import re # regular expressions


def get_arguments():
    parser = optparse.OptionParser() # object of OptionParser class
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC, use --help for more info")    
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    # to run shell command in foreground and wait for command to complete execution, we use shell=True
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        # it returns object of regex and to grab first value
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arguments() # to get arguments from terminal

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)  # to get interface and mac value from options

current_mac = get_current_mac(options.interface) # to get updated value of mac

if current_mac == options.new_mac:
    print("[+] MAC address changed successfully to " + current_mac)
else:
    print("[-] MAC address did not change")
