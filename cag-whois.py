#!/usr/bin/env python3

# We need: os for pause in Windows, re to seach for the lines we need, urllib to query the staff pages.
import os
import re
import urllib.request

# First, we need to define the pages we are lookign for employee information on.
# Format: "Name", "URL", "Name", "URL", etc. Use a Null string if no name is desired.

# A = Dealer Inspire Pages.
teamPagesA = ["Austin Infiniti", "https://www.austininfiniti.com/about-us/staff/", "Austin Subaru", "https://www.austinsubaru.com/about-us/staff/", "First Texas Honda", "https://www.firsttexashonda.com/staff/", "Mercedes-Benz of Austin", "https://www.mercedesbenzofaustin.com/about-us/staff/", "Merceces-Benz of San Juan", "https://www.mbsanjuantx.com/about-us/staff/"]

# B = Fixed Ops Digital Pages.
teamPagesB = ["Continental Collision", "https://www.continentalcollision.com/team-members/"]

# C = Dealer dot Com Pages.
teamPagesC = ["Audi San Juan", "https://www.audisanjuan.com/dealership/staff.htm"]

# Some sites don't like being spidered, adding headers to tell them we're a real browser, promise.
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

# Function to check our first set of URLs
def checkStaffA(staffURL, names):
    # Grabbing the page.
	webpage = urllib.request.urlopen(staffURL).read().decode('utf-8')
    # Intializing an empty array to append our results to.
    results = []
    # For each name, we want to grab it if it appears on the site, along with their title, and top gun status, along with some blobs of code.
    for i in range(0, len(names)):
        results.append(str(re.findall(rf".*<h3>.*{names[i]}.*</h3>\n.*", webpage, re.IGNORECASE)))
    # Now we loop through the output glob we got for each name, change some formatting, and remove the bits we don't want.
    for i in range (0, len(results)):
        results[i] = str(re.sub(r", Jr", " Jr", results[i]))
        results[i] = str(re.sub(r"\s{2,50}", "", results[i]))
        results[i] = str(re.sub(r", Top"," - Top", results[i]))
        results[i] = str(re.sub(r"(\\t)*<h3>", "", results[i]))
        results[i] = str(re.sub(r"(\\t)*<h4>", "", results[i]))
        results[i] = str(re.sub(r"\s<br>", " -", results[i]))
        results[i] = str(re.sub(r"<br>", " -", results[i]))
        results[i] = str(re.sub(r"</h3>", "", results[i]))
        results[i] = str(re.sub(r"</h4>", "", results[i]))
        results[i] = str(re.sub(r"]", "", results[i]))
        results[i] = str(re.sub(r"\[", " ", results[i]))
        results[i] = str(re.sub(r"'", "", results[i]))
        results[i] = str(re.sub(r"(\\n)", "\n", results[i]))
    # We've got our results, so let's print them!
    printOut(results)

# Function to check our second set of URLs
def checkStaffB(staffURL, names):
    # Grabbing the page.
	webpage = urllib.request.urlopen(staffURL).read().decode('utf-8')
    # Intializing an empty array to append our results to.
    results = []
    # For each name, we want to grab it if it appears on the site, along with their title, and top gun status, along with some blobs of code.
    for i in range(0, len(names)):
        results.append(str(re.findall(rf".*<h3>.*{names[i]}.*</h3>.*\n[T,o,p,\ ,G,u,n]{{0,8}}[0-9]{{0,4}}", webpage, re.IGNORECASE)))
    # Now we loop through the output glob we got for each name, change some formatting, and remove the bits we don't want.
    for i in range (0, len(results)):
        results[i] = str(re.sub(r", Jr", " Jr", results[i]))
        results[i] = str(re.sub(r"\\nTop", " - Top", results[i]))
        results[i] = str(re.sub(r"\\t\\t\\t<div class=\"team-member.*?<h3>", "", results[i]))
        results[i] = str(re.sub(r"<br \/>", "", results[i]))
        results[i] = str(re.sub(r"<\/p>.*?\\n", "", results[i], re.IGNORECASE))
        results[i] = str(re.sub(r"\[", "", results[i]))
        results[i] = str(re.sub(r"\]", "", results[i]))
        results[i] = str(re.sub(r"\'", "", results[i]))
        results[i] = str(re.sub(r"<\/h3><p>", "\n", results[i]))
    printOut(results)

# Function to check our third set of URLs
def checkStaffC(staffURL, names):
    # Grabbing the page.
	webpage = urllib.request.urlopen(staffURL).read().decode('utf-8')
    # Intializing an empty array to append our results to.
    results = []
    # For each name, we want to grab it if it appears on the site, along with their title, and top gun status, along with some blobs of code.
    for i in range(0, len(names)):
        results.append(str(re.findall(rf"\">\n.*?{names[i]}.*?\n.*<.*?\n<.*?\n<.*", webpage, re.IGNORECASE)))
    # Now we loop through the output glob we got for each name, change some formatting, and remove the bits we don't want.
    for i in range (0, len(results)):
        results[i] = str(re.sub(r", Jr", " Jr", results[i]))
        results[i] = str(re.sub(r"\">\\n", "", results[i]))
        results[i] = str(re.sub(r"<\/dd>", "", results[i]))
        results[i] = str(re.sub(r"•", "-", results[i]))
        results[i] = str(re.sub(r"\[", "", results[i]))
        results[i] = str(re.sub(r"\]", "", results[i]))
        results[i] = str(re.sub(r"\'", "", results[i]))
        results[i] = str(re.sub(r"\\n<.*?\">", "\n", results[i]))
    printOut(results)

# Function to print out our results.
def printOut(results):
	# Intializing an empty array to append our output to.
    output = []
	# Looping through the results array and pulling out the clumped up entries.
    for clumpedArray in results:
        # We split them into a temp array, then add them onto our output array.
		tempArray = (clumpedArray.split(","))
        output += tempArray
    # Loop through our results and get rid of those pesky extra spaces for some sites.
    for op in range(0, len(output)):
        output[op] = re.sub(r"^\s", "", str(output[op]))
    output = list(set(output))
    # And now we loop through our list of results and print!
    for entry in output:
        print(entry, "\n")

		
# Getting names to search for from the user.
names = input("Please input names you would like to search for: ").split(" ")

# This is where we actually do the thing		
for location in range (0, len(teamPagesA), 2):
    print("\n=====", teamPagesA[location], "=====")
    checkStaffA(teamPagesA[location + 1],names)

for location in range (0, len(teamPagesB), 2):
    print("\n=====", teamPagesB[location], "=====")
    checkStaffB(teamPagesB[location + 1],names)

for location in range (0, len(teamPagesC), 2):
    print("\n=====", teamPagesC[location], "=====")
    checkStaffC(teamPagesC[location + 1],names)

# Pause if we are running in Windows, to allow users to run the script easily from their file manager or desktop
try:
    os.system('pause')
except NameError:
    sys.exit()
