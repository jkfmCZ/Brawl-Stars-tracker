import pandas as pd
import json, os, requests, logging,  urllib.parse
import plotly.express as px


# docsne
data = "/home/jkfm/Documents/GitHub/Brawl-Stars-tracker/brawl.json"
pl_tag = "#2Q0U9PJLP"

with open(data, 'r', encoding='utf-8') as file:
    data = json.load(file)
df = pd.DataFrame(data["items"])

print(df,df.info())

battles_df = pd.json_normalize(df['battle'])
# print(battles_df.info())
team_count = []
teams_df = pd.json_normalize(battles_df["teams"])
for x in teams_df:
    team_count.append(teams_df[x])



teams_df =  pd.concat(team_count)
teams_df = pd.json_normalize(teams_df.explode('brawlers'))
pl_brawlers = teams_df[teams_df["tag"] == pl_tag]
teamates_df = teams_df[teams_df["tag"] != pl_tag]
# print(teamates_df)
results = battles_df["result"].combine_first(battles_df["rank"])



# teamsdd = pd.json_normalize(teams_df["tag"])

brawler_trophy = teamates_df.groupby("brawler.name")
# print(brawler_trophy["brawler.trophies"].mean())
# print(brawler_trophy["brawler.name"].first())

# print(battles_df["rank"].fillna(0).info(), battles_df["mode"].info())
# print(battles_df["rank"])
# print(teamates_df["brawler.power"])




