#!/usr/bin/env

# IPv6extender.py
# Last Modified: 2/04/2020
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

try:
    input = raw_input
except NameError:
    pass
# End compatibility (delete section if using Python 3)

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

# Parser description of usage from CLI
parser = argparse.ArgumentParser(description="Utility to convert exported Infoblox IPv6 IPAM data to 128-bit notation")
parser.add_argument("--file", required=True, default=None, type=str, help="name of source CSV file")
args = parser.parse_args()
input_file = args.file

# Sanity check that file inputted by is valid
if os.path.isfile(input_file) is False:
    sys.exit("Error: Invalid file")
# Name creation of destination file based on input file name
output_file = "extended-" + input_file

# Count number of rows on source file to parse for IPv6 data
row_count = sum(1 for row in csv.reader(input_file))

with open(input_file, "r") as ipamfile:
    csv_read = csv.reader(ipamfile, delimiter=",")
    with open(output_file, "a") as addrfile:
        csv_write = csv.writer(addrfile, delimiter=",")
        for row in csv_read:
            for i in range(row_count):
                current_ip = bytes.decode(row[i])
                try:
                    valid_ip = bool(ipaddress.ip_address(current_ip))
                except ValueError:
                    valid_ip = False
                    current_ip = bytes.encode(row[i])
                if valid_ip is True:
                    current_ip = extend_ip(current_ip)
                addrfile.write(current_ip)
                addrfile.write(",")
            addrfile.write("\n")

# Expansion completed message for user including destination file
print("IPv6 addresses extended ->", output_file)

ipamfile.close()
addrfile.close()
# End main
