#!/usr/bin/env python3

# We need: os for pause in Windows, socket for reverse dns lookup, ssl for our https connection, urllib to open the URL for our XML file,
# sys to exit, and xml.etree.ElementTree (way too much to type) to get data out of our xml file in a sane fashion.
import os
import socket
import ssl
import sys
import urllib.request
import xml.etree.ElementTree as ET

# Please enter your firewall's hostname or IP and API Key here:
fwAddress = "0.0.0.0"
fwAPIKey = "F00b4r"

# Testing to see if you can read >.>
if fwAddress == "0.0.0.0" or fwAPIKey == "F00b4r":
    sys.exit("Please enter your firewall's address and/or your API key into the fwAddress and fwAPIKey variables, respectively.")

# Set up our empty lists to append to later.
comboList, ipList, userList = [], [], []

# This allows us to connect over https to our firewall with it's self-signed cert.
ssl._create_default_https_context = ssl._create_unverified_context

# Store the location of the user XML file to paloURL
paloURL = "https://" + fwAddress + "/api/?key=" + fwAPIKey + "&type=op&cmd=<show><user><ip-user-mapping><all></all></ip-user-mapping></user></show>"

# Get the name we're looking for from user input.
userName = str.lower(input("Input user\'s name(or leave blank for all users and hosts): "))

# Go and get the XML file.
paloData = str(urllib.request.urlopen(paloURL).read())[2:-1]

# This makes an Element Tree from our XML file.
paloTree = ET.fromstring(paloData)

# Take all the IP elements from the tree, then loop through them and append to our IP list.
ips = paloTree.findall('.//ip')
for each in ips:
    ipList.append(each.text)

# Take all the user elements from the tree, then loop through them and append to our user list.
users = paloTree.findall('.//user')
for each in users:
    userList.append(each.text)

# Loop through the IP list
for i in range(0, len(ipList)):
    # Checks to see if the current entry on the user's list is the one we were supplied.
    if userName in userList[i]:

        # Here, we try to do a reverse lookup on the IP and then add our user and hostname combo to our combo list, however...
        # If the IP is invalid, or there is no hostname match, we add the user and "IP" combo to our combo list.
        # We only want the 13th character and on to drop the domain name off the user.
        try:
            hostName = socket.gethostbyaddr(ipList[i])[0]
            comboList.append(userList[i][13::] + " - " + hostName)
        except OSError:
            comboList.append(userList[i][13::] + " - " + ipList[i])

# Check to see if we have any list entries. If we do, print them one by one! If not, let them know we didn't find anything.
if comboList:
    comboList.sort()
    for entry in range(0, len(comboList)):
        print(comboList[entry])
else:
    print("No user name matches found.")

# Pause if we are running in Windows, to allow users to run the script easily from their file manager or desktop
if os.name == "nt":
    os.system('pause')
