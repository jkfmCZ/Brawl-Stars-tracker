from .get_data import club_log, player_log, battle_log, brawles
from .loader import updater
import plotly.express as px
import pandas as pd
from plotly.offline import plot
from datetime import datetime, date



def lossxwins(player_tag):
    battles_df = updater(player_tag, "battle")
    w_counter = battles_df["result"].apply(lambda x:1 if x == "victory" else 0).sum()
    l_counter = len(battles_df["result"]) - w_counter
    fig = px.pie(values=[w_counter,l_counter], names=["wins","losses"])
    responce = plot(fig,output_type="div")
    return responce
def bar_ratio(player_tag):
    battles_df = updater(player_tag, "battle")
    battles_df['victory'] = battles_df['result'].apply(lambda x: 1 if x == "victory" else 0)
    battles_df['defeat'] = battles_df['result'].apply(lambda x: 1 if x != "victory" else 0)
    # Agregace 
    battles_df = battles_df.drop("time", axis='columns')
    agg_df = battles_df.groupby('mode').sum()[['victory', 'defeat']].reset_index()
    melted_df = agg_df.melt(id_vars='mode', value_vars=['victory', 'defeat'], var_name='result_type', value_name='count')

    fig = px.bar(melted_df, x='mode', y='count', color='result_type', barmode='group',
                labels={'mode': 'Mode', 'count': 'Count', 'result_type': 'Result'})
    return plot(fig, output_type="div"),

def team_braw(player_tag):
    battles_df = updater(player_tag, "battle")
    try:
        teams_df = (battles_df["teams"]).dropna().to_list()
    except:
        teams_df = (battles_df["players"]).dropna().to_list()
    flat_teams_list = [item for sublist in teams_df for team in sublist for item in team]
    try:
        for sub in battles_df.iloc[:,14].dropna():
            for team in sub:
                flat_teams_list.append(team)
    except: 
        try:
            for sub in battles_df.loc[battles_df['teams'].isnull()]["players"]:
                for team in sub:
                    flat_teams_list.append(team)
        except: print("upsik")
    teams_df = pd.json_normalize(flat_teams_list)
    teamates_df = teams_df[teams_df["tag"] != player_tag]
    fig = px.treemap(path=[teamates_df["brawler.name"].dropna(),teamates_df["brawler.power"].dropna(),teamates_df["name"].dropna()])
    return plot(fig, output_type="div")

def team_braw_trophy(player_tag):
    battles_df = updater(player_tag, "battle")
    try:
        teams_df = (battles_df["teams"]).dropna().to_list()
    except:
        teams_df = (battles_df["players"]).dropna().to_list()
    flat_teams_list = [item for sublist in teams_df for team in sublist for item in team]
    try:
        for sub in battles_df.iloc[:,14].dropna():
            for team in sub:
                flat_teams_list.append(team)
    except: 
        try:
            for sub in battles_df.loc[battles_df['teams'].isnull()]["players"]:
                for team in sub:
                    flat_teams_list.append(team)
        except: print("upsik")
    teams_df = pd.json_normalize(flat_teams_list)  
    teamates_df = teams_df[teams_df["tag"] != player_tag]
    brawler_trophy = teamates_df.groupby("brawler.name")
    fig = px.line(x=brawler_trophy["brawler.name"].first(),y=brawler_trophy["brawler.trophies"].mean())
    return plot(fig, output_type="div")



def p_braw_wl(player_tag):
    battles_df = updater(player_tag, "battle")
    try:
        teams_df = (battles_df["teams"]).dropna().to_list()
    except:
        teams_df = (battles_df["players"]).dropna().to_list()
    flat_teams_list = [item for sublist in teams_df for team in sublist for item in team]
    try:
        for sub in battles_df.iloc[:,14].dropna():
            for team in sub:
                flat_teams_list.append(team)
    except: 
        try:
            for sub in battles_df.loc[battles_df['teams'].isnull()]["players"]:
                for team in sub:
                    flat_teams_list.append(team)
        except: print("upsik")
    teams_df = pd.json_normalize(flat_teams_list)
    pl_brawlers = teams_df[teams_df["tag"] == player_tag]
    try:results = battles_df["result"].combine_first(battles_df["rank"])
    except:
        try:results = battles_df["rank"].combine_first(battles_df["result"])
        except:
            try:results = battles_df["rank"]
            except: results = battles_df["result"]

    fig = px.treemap(path=[battles_df["mode"],pl_brawlers["brawler.name"],results])
    return plot(fig, output_type="div")
#player logs
def player_info(player_tag):
    df_player = updater(player_tag, "player")
    df = updater(player_tag, "battle")
    games_today = df["time"][df["time"] == date.today()].count()
    name = df_player["name"].values.item()
    trophies = df_player["trophies"].values.item()
    highestTrophies = df_player["highestTrophies"].values.item()
    vs3Victories  = df_player["3vs3Victories"].values.item()
    solowin = df_player["soloVictories"].values.item()
    duowin = df_player["duoVictories"].values.item()
    try:
        club = df_player["club.name"].values.item()
    except:
        club = "Unknown"
    return {"pname": name,"trophies":trophies,"solowin":solowin,
            "highestTrophies":highestTrophies,"vs3Victories":vs3Victories,
            "duowin":duowin, "club":club, "games_today":games_today}

def p_brawl_lvl(player_tag):
    df_player = updater(player_tag, "player")
    df_pbrawl = pd.json_normalize(df_player["brawlers"])
    brawler_list = []
    for col in df_pbrawl.columns:
        brawler_list.append(pd.json_normalize(df_pbrawl[col][0]))
    df_brawlers = pd.concat(brawler_list, ignore_index=True)
    fig = px.treemap(df_brawlers, path=["power", "name"])
    return plot(fig, output_type="div")

def p_brawl_trophy(player_tag):  
    df_player = updater(player_tag, "player")
    df_pbrawl = pd.json_normalize(df_player["brawlers"])
    brawler_list = []
    for col in df_pbrawl.columns:
        brawler_list.append(pd.json_normalize(df_pbrawl[col][0]))
    df_brawlers = pd.concat(brawler_list, ignore_index=True)
    df_brawlers_long = df_brawlers.melt(id_vars=['name'], value_vars=['trophies', 'highestTrophies'],var_name='Trophy Type', value_name='Trophies')
    fig = px.bar(df_brawlers_long, x='name', y='Trophies', color='Trophy Type', barmode='group')
    return plot(fig, output_type="div")


def own_ornot(player_tag):
    df_player = updater(player_tag, "player")
    df_pbrawl = pd.json_normalize(df_player["brawlers"])
    brawler_list = []
    for col in df_pbrawl.columns:
        brawler_list.append(pd.json_normalize(df_pbrawl[col][0]))
    df_brawlers = pd.concat(brawler_list, ignore_index=True)
    allb = brawles()
    allb['players'] = allb['name'].apply(lambda x: 'OWN' if x in df_brawlers["name"].tolist() else 'DOESNT HAVE YET')
    allb["rank"] = [df_brawlers["rank"][df_brawlers["name"] == x].values.item() if x in df_brawlers["name"].tolist() else 0 for x in allb['name']]
    fig = px.treemap(allb, path=["players","name","rank"])
    return plot(fig, output_type= "div")
   
#club_logs
def club_members(player_tag):
    df_club = updater(player_tag, "club")
    df_members = pd.json_normalize(df_club["members"])
    fig = px.treemap(df_members,path=["trophies","name", "tag" ])
    return plot(fig, output_type="div")
   
                
def club_roles(player_tag):
    df_club = updater(player_tag, "club")
    df_members = pd.json_normalize(df_club["members"])
    fig=px.sunburst(df_members,path=["role","name"])
    return plot(fig, output_type="div")

def clubm_trophies(player_tag):               
    df_club = updater(player_tag, "club")
    df_members = pd.json_normalize(df_club["members"])
    df_members['color'] = df_members['tag'].apply(lambda x: 'red' if x == player_tag else 'blue')
    df_members.sort_values(by=["trophies"])
    fig = px.bar(df_members, color="color", x="name",y="trophies",
                 category_orders={"name": df_members.sort_values(by='trophies',ascending=False)['name'].tolist()})
    return plot(fig, output_type="div")
  

def club_info(player_tag):
    df_club = pd.json_normalize(updater(player_tag, "club"))
    clubtag = df_club["tag"].values.item()
    name = df_club["name"].values.item()
    description = df_club["description"].values.item()
    type = df_club["type"].values.item()
    reg_trophy = df_club["requiredTrophies"].values.item
    trophies = df_club["trophies"].values.item
    return {'name': name, 'description': description, 'type': type, 
            "clubtag": clubtag, 'reg_trophy': reg_trophy, "trophies":trophies}
def player_name(player_tag):
    df_player = updater(player_tag, "player")
    df = df_player["name"].values.item()
    return df


