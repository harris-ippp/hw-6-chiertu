#!/usr/bin/env python
import os
import requests

#download the data for every year in the ELECTION_ID list
for line in open("ELECTION_ID"):
    resp = requests.get("http://historical.elections.virginia.gov/elections/download/{}/precincts_include:0/".format(line[5:10]))
    file_name = line.partition(' ')[0] +".csv"
    with open(file_name, "w") as out:
        out.write(resp.text)

#rename the data file for year 2016
os.rename("2016.csv","president_general_2016.csv")
