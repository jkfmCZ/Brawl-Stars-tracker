from .get_data import club_log, player_log, battle_log, brawles
import plotly.express as px
import pandas as pd
from plotly.offline import plot



def lossxwins(player_tag):
    battles_df = battle_log(player_tag)
    w_counter = battles_df["result"].apply(lambda x:1 if x == "victory" else 0).sum()
    l_counter = len(battles_df["result"]) - w_counter
    fig = px.pie(values=[w_counter,l_counter], names=["wins","losses"], title="winsxlosses ratio")
    responce = plot(fig,output_type="div")
    return responce

def bar_ratio(player_tag):
    battles_df = battle_log(player_tag)
    battles_df['victory'] = battles_df['result'].apply(lambda x: 1 if x == "victory" else 0)
    battles_df['defeat'] = battles_df['result'].apply(lambda x: 1 if x != "victory" else 0)
    # Agregace 
    agg_df = battles_df.groupby('mode').sum()[['victory', 'defeat']].reset_index()
    melted_df = agg_df.melt(id_vars='mode', value_vars=['victory', 'defeat'], var_name='result_type', value_name='count')

    fig = px.bar(melted_df, x='mode', y='count', color='result_type', barmode='group',
                labels={'mode': 'Mode', 'count': 'Count', 'result_type': 'Result'},
                title='Wins and Losses by Mode')
    return plot(fig, output_type="div")

def team_braw(player_tag):
    battles_df = battle_log(player_tag)
    teams_df = (battles_df["teams"].combine_first(battles_df.iloc[:,14])).to_list()
    flat_teams_list = [item for sublist in teams_df for team in sublist for item in team]
    for sub in battles_df.iloc[:,14].dropna():
        for team in sub:
            flat_teams_list.append(team)
    teams_df = pd.json_normalize(flat_teams_list)
    teamates_df = teams_df[teams_df["tag"] != player_tag]
    fig = px.treemap(path=[teamates_df["brawler.name"].dropna(),teamates_df["brawler.power"].dropna(),teamates_df["name"].dropna()],title="most used brawlers")
    return plot(fig, output_type="div")

def team_braw_trophy(player_tag):
    battles_df = battle_log(player_tag)
    teams_df = (battles_df["teams"].combine_first(battles_df.iloc[:,14])).to_list()
    flat_teams_list = [item for sublist in teams_df for team in sublist for item in team]
    for sub in battles_df.iloc[:,14].dropna():
        for team in sub:
            flat_teams_list.append(team)
    teams_df = pd.json_normalize(flat_teams_list)
    teamates_df = teams_df[teams_df["tag"] != player_tag]
    brawler_trophy = teamates_df.groupby("brawler.name")
    fig = px.line(x=brawler_trophy["brawler.name"].first(),y=brawler_trophy["brawler.trophies"].mean(),title="mean trophies on teamates brawlers")
    return plot(fig, output_type="div")

def p_braw_wl(player_tag):
    battles_df = battle_log(player_tag)
    teams_df = (battles_df["teams"].combine_first(battles_df.iloc[:,14])).to_list()
    flat_teams_list = [item for sublist in teams_df for team in sublist for item in team]
    for sub in battles_df.iloc[:,14].dropna():
        for team in sub:
            flat_teams_list.append(team)
    teams_df = pd.json_normalize(flat_teams_list)
    pl_brawlers = teams_df[teams_df["tag"] == player_tag]
    results = battles_df["result"].combine_first(battles_df["rank"])
    fig = px.treemap(path=[battles_df["mode"],pl_brawlers["brawler.name"],results],title="Used brawler by player vs wins/looses")
    return plot(fig, output_type="div")
#player logs
def player_info(player_tag):
    df_player = player_log(player_tag)
    name = df_player["name"].values.item()
    trophies = df_player["trophies"].values.item()
    highestTrophies = df_player["highestTrophies"].values.item()
    vs3Victories  = df_player["3vs3Victories"].values.item()
    solowin = df_player["soloVictories"].values.item()
    duowin = df_player["duoVictories"].values.item()
    club = df_player["club.name"].values.item()
    return {"pname": name,"trophies":trophies,"solowin":solowin,
            "highestTrophies":highestTrophies,"vs3Victories":vs3Victories,
            "duowin":duowin, "club":club}

def p_brawl_lvl(player_tag):
    df_player = player_log(player_tag)
    df_pbrawl = pd.json_normalize(df_player["brawlers"])
    brawler_list = []
    for col in df_pbrawl.columns:
        brawler_list.append(pd.json_normalize(df_pbrawl[col][0]))
    df_brawlers = pd.concat(brawler_list, ignore_index=True)
    fig = px.treemap(df_brawlers, path=["power", "name"], title="Your Brawlers power")
    return plot(fig, output_type="div")

def p_brawl_trophy(player_tag):  
    df_player = player_log(player_tag)
    df_pbrawl = pd.json_normalize(df_player["brawlers"])
    brawler_list = []
    for col in df_pbrawl.columns:
        brawler_list.append(pd.json_normalize(df_pbrawl[col][0]))
    df_brawlers = pd.concat(brawler_list, ignore_index=True)
    df_brawlers_long = df_brawlers.melt(id_vars=['name'], value_vars=['trophies', 'highestTrophies'],var_name='Trophy Type', value_name='Trophies')
    fig = px.bar(df_brawlers_long, x='name', y='Trophies', color='Trophy Type', barmode='group',title='Current vs Maximum Trophies on Brawlers')
    return plot(fig, output_type="div")

def own_ornot(player_tag):
    df_player = player_log(player_tag)
    df_pbrawl = pd.json_normalize(df_player["brawlers"])
    brawler_list = []
    for col in df_pbrawl.columns:
        brawler_list.append(pd.json_normalize(df_pbrawl[col][0]))
    df_brawlers = pd.concat(brawler_list, ignore_index=True)
    allb = brawles()
    allb['players'] = allb['name'].apply(lambda x: 'OWN' if x in df_brawlers["name"].tolist() else 'DOESNT HAVE YET')
    fig = px.treemap(allb, path=["players","name"], title="Your brawlers")
    return plot(fig, output_type= "div")
#club_logs
def club_members(player_tag):
    df_club = club_log(player_tag)
    df_members = pd.json_normalize(df_club["members"])
    fig = px.treemap(df_members,path=["trophies","name", "tag" ],title="Club members")
    return plot(fig, output_type="div")
                
def club_roles(player_tag):
    df_club = club_log(player_tag)
    df_members = pd.json_normalize(df_club["members"])
    fig=px.sunburst(df_members,path=["role","name"],title="Club roles")
    return plot(fig, output_type="div")

def clubm_trophies(player_tag):               
    df_club = club_log(player_tag)
    df_members = pd.json_normalize(df_club["members"])
    df_members['color'] = df_members['tag'].apply(lambda x: 'red' if x == player_tag else 'blue')
    df_members.sort_values(by=["trophies"])
    fig = px.bar(df_members, color="color", x="name",y="trophies",
                 category_orders={"name": df_members.sort_values(by='trophies',ascending=False)['name'].tolist()}
                ,title="Club members trophies")
    return plot(fig, output_type="div")

def club_info(player_tag):
    df_club = pd.json_normalize(club_log(player_tag))
    tag = df_club["tag"].values.item()
    name = df_club["name"].values.item()
    description = df_club["description"].values.item()
    type = df_club["type"].values.item()
    reg_trophy = df_club["requiredTrophies"].values.item
    trophies = df_club["trophies"].values.item
    return {'name': name, 'description': description, 'type': type, 
            "tag": tag, 'reg_trophy': reg_trophy, "trophies":trophies}