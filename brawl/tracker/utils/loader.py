from .get_data import player_log, brawles, club_log ,battle_log

def club_checker(player_tag):
    df = player_log(player_tag)
    try:
        df["club.name"].values.item()
    except:
        return False
    return club_log_load(player_tag)

def player_log_load(player_tag):
    global player_df
    player_df = player_log(player_tag)
    return player_df

def club_log_load(player_tag):
    global club_df
    club_df = club_log(player_tag)
    return club_df

def battle_log_load(player_tag):
    global battle_df
    battle_df = battle_log(player_tag)
    return battle_log

def brawles():
    global brawles_df
    brawles_df = brawles()
    return brawles_df
def restarter():
    global log_list
    log_list = [""]

def updater(log, status):
    if log in log_list:
        if status == "player":
            return player_df
        elif status == "club":
            return club_df
        elif status == "battle":
            return battle_df

    else:
        player_log_load(log),club_checker(log),battle_log_load(log)
        log_list[0] = log
        if status == "player":
            return player_df
        elif status == "club":
            return club_df
        elif status == "battle":
            return battle_df

 

