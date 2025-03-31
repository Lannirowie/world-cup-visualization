import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')

# Get the correct table
tables = soup.find_all("table", {"class": "wikitable"})
finals_table = tables[1]  # second table contains actual final results

# Parse table into DataFrame
data = []
for row in finals_table.find_all("tr")[1:]:
    cols = row.find_all(["th", "td"])
    if len(cols) >= 6:
        year = cols[0].text.strip()
        winner = cols[1].text.strip()
        runner_up = cols[3].text.strip()
        data.append([year, winner, runner_up])

df = pd.DataFrame(data, columns=["Year", "Winner", "RunnerUp"])

# Normalize "Germany" and "West Germany"
df["Winner"] = df["Winner"].replace("West Germany", "Germany")
df["RunnerUp"] = df["RunnerUp"].replace("West Germany", "Germany")

# Save to CSV
df.to_csv("world_cup_finals.csv", index=False)
print("Data saved.")