#!/usr/bin/env

# IPv6extender.py
# Last Modified: 2/02/2020
# Author:        Arthur Mills
# License:       GNU Lesser General Public License, version 3
# Description:
# Polls IP addresses from Infoblox IPAM CSV export;
# captures all IP address data and converts IPv6 addresses into 128-bit notation

# Utilizes pypi.org backport of ipaddress module for Python 2.x users
# https://pypi.org/project/ipaddress/

# Python 2 -> Python 3 compatibility
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    input = raw_input
except NameError:
    pass
# End compatibility

# Python module imports
import sys
import os.path
import csv
import argparse
import ipaddress


# Function declarations
def extend_ip(ipaddr):
    addr = ipaddr
    ip_version = ipaddress.ip_address(ipaddr).version
    if ip_version == 6:
        addr = ipaddress.ip_address(ipaddr).exploded
    return addr


# Main program
addrfile = open("ExtendedAddresses.csv", "ab")

parser = argparse.ArgumentParser(description="Converts Infoblox IPAM exported IPv6 addresses to 128-bit notation")
parser.add_argument("--file", required=True, default=None, type=str, help="name of source CSV file")

args = parser.parse_args()
filename = args.file

if os.path.isfile(filename) is False:
    sys.exit("Error: Invalid file")

with open(filename, "rb") as ipamfile:
    csv_read = csv.reader(ipamfile)
    for row in csv_read:
        current_ip = unicode(row[1], "utf-8")
        try:
            valid_ip = bool(ipaddress.ip_address(current_ip))
        except ValueError:
            valid_ip = False
        if valid_ip is True:
            current_ip = extend_ip(current_ip)
            addrfile.write(current_ip)
            addrfile.write(",\n")

print("IP data exported -> ExtendedAddresses.csv")

ipamfile.close()
addrfile.close()
# End main
