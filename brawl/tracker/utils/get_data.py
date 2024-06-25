import pandas as pd
import json, os, requests, logging,  urllib.parse
from tracker.models import Brawl_Tags
from datetime import datetime, date
from dotenv import load_dotenv
#tvuj api key
load_dotenv()
# api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjA2MWZkZjI1LTIwMjgtNGEwNC1iNmFhLTEzYWM0ZWE0OGYyNCIsImlhdCI6MTcxOTA2MDQ3NCwic3ViIjoiZGV2ZWxvcGVyLzdjZjRiYzY2LTE1NTgtMjJjYS02NWIwLTNjOWJkNzMzYWY5ZCIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNzguODAuMTEyLjYwIl0sInR5cGUiOiJjbGllbnQifV19.8OdKxcPZ22j6rFcC_jWW_m6VoTUph6KcrOs0vbqEKclabCwrmrjBRHx-cLSLeiTH79ML2SWG9H5cEZdY6mQ7kw"
api_key = os.getenv('API_KEY')
if not api_key:
    print("API key not found in environment variables.")
    exit()

def battle_log(player_tag):
    url = f"https://api.brawlstars.com/v1/players/{urllib.parse.quote(player_tag)}/battlelog"
    
    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
    if response.status_code != 200:
        print(f"Failed to retrieve data for {player_tag}: {response.status_code}")
        return []
    df = response.json()
    #jenom battle
    df = pd.DataFrame(df["items"])
    df_battle= pd.json_normalize(df["battle"])
    dates=[]
    for x in df["battleTime"]:
        dates.append(datetime.strptime(x[:8], '%Y%m%d').date())
    df_battle["time"] = dates
    return df_battle
# print(battle_log("#232Q0U9PJLP"))
# df = pd.json_normalize(df['battle'])

def player_log(player_tag):
    url = f"https://api.brawlstars.com/v1/players/{urllib.parse.quote(player_tag)}"
    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
    if response.status_code != 200:
        print(f"Failed to retrieve data for {player_tag}: {response.status_code}")
        return []
    df = response.json()
    df = pd.json_normalize(df)
    
    return df

# print(player_log("#2Q0U9PJLP").info())

def club_log(player_tag):
    club_tag = player_log(player_tag)["club.tag"].loc[0]
    url = f"https://api.brawlstars.com/v1/clubs/{urllib.parse.quote(club_tag)}"
    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
    if response.status_code != 200:
        print(f"Failed to retrieve data for {club_tag}: {response.status_code}")
        return []
    df = response.json()
    return df

def brawles():
    url = f"https://api.brawlstars.com/v1/brawlers"
    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
    df = response.json()
    try:
        df = pd.json_normalize(df["items"])
    except: df = pd.DataFrame({
    "name": [
    "CLANCY", "BERRY", "LILY", "DRACO", "ANGELO", "MELODIE", "LARRY & LAWRIE", 
    "KIT", "MICO", "CHARLIE", "CHUCK", "PEARL", "DOUG", "CORDELIUS", "HANK", 
    "MAISIE", "WILLOW", "R-T", "MANDY", "GRAY", "CHESTER", "BUSTER", "GUS", 
    "SAM", "OTIS", "BONNIE", "JANET", "EVE", "FANG", "LOLA", "MEG", "ASH", 
    "GRIFF", "BUZZ", "GROM", "SQUEAK", "BELLE", "STU", "RUFFS", "EDGAR", 
    "BYRON", "LOU", "AMBER", "COLETTE", "SURGE", "SPROUT", "NANI", "GALE", 
    "JACKY", "MAX", "MR. P", "EMZ", "BEA", "SANDY", "8-BIT", "BIBI", "CARL", 
    "ROSA", "LEON", "TICK", "GENE", "FRANK", "PENNY", "DARRYL", "TARA", "PAM", 
    "PIPER", "BO", "POCO", "CROW", "MORTIS", "EL PRIMO", "DYNAMIKE", "NITA", 
    "JESSIE", "BARLEY", "SPIKE", "RICO", "BROCK", "BULL", "COLT", "SHELLY"]})
    return df

def API_tester(player_tag):
    url = f"https://api.brawlstars.com/v1/players/{urllib.parse.quote(player_tag)}/battlelog"
    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
    if response.status_code == 404:
        return ["invalid","Wrong tag try again"]
    elif response.status_code == 400:
        return ["invalid","Error: Bad request:400"]
    elif response.status_code == 403:
        return ["invalid","Error: Forbidden API:403"]
    elif response.status_code == 500:
        # print("invalid")
        return ["invalid","Error: Supercells_problem:500"]
    elif response.status_code == 504:
        return ["invalid","Error: API is down:504"]
    if response.status_code == 200:
        if not Brawl_Tags.objects.filter(tag=player_tag).exists():
            Brawl_Tags(tag=player_tag).save()
        return ["valid", ""]
        
    else:
        return ["invalid",f"Failed to retrieve data for {player_tag}: {response.status_code}"]
        






