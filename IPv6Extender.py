#!/usr/bin/env

# IPv6Extender.py
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
import os.path
import csv
import ipaddress


# Function declarations
def extend_ip(ipaddr):
    addr = ipaddr
    ip_version = ipaddress.ip_address(ipaddr).version
    if ip_version == 6:
        addr = ipaddress.ip_address(ipaddr).exploded
    return addr


# Local variable declarations
is_dir = False
is_file = False
dirname = ""
filename = ""
fullpath = ""
addrfile = open("ExtendedAddresses.csv", "ab")

# Main program
while is_dir is False:
    print("Enter /path/directory/:")
    dirname = input()
    is_dir = os.path.isdir(dirname)
    if is_dir is False:
        print("Invalid directory.")
while is_file is False:
    print("Enter name.csv of CSV file:")
    filename = input()
    fullpath = dirname + filename
    is_file = os.path.exists(fullpath)
    if is_file is False:
        print("Invalid filename.")

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
