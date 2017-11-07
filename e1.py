#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup as bs
resp = requests.get("http://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2016/office_id:1/stage:General")
soup = bs(resp.content, "html.parser")

#scrape election year and id from the website
rows = soup.find_all("tr","election_item")
ID = [x.get("id").rpartition('-')[2] for x in rows]
year = [x.find("td").contents[0] for x in rows]
elections_id = [year[x] + " " + ID[x] for x in range(len(ID))]

#print the elections id list and save it in "ELECTION_ID.txt"
print(elections_id)
file_name = "ELECTION_ID"
with open(file_name, "w") as out:
    for item in elections_id:
        out.write("{}\n".format(item))
