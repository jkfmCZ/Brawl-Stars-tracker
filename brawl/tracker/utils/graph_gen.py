from .get_data import battles_df, teams_df ,pl_brawlers ,teamates_df ,results ,brawler_trophy
import plotly.express as px
import pandas as pd
from plotly.offline import plot



def lossxwins():
    w_counter = battles_df["result"].apply(lambda x:1 if x == "victory" else 0).sum()
    l_counter = len(battles_df["result"]) - w_counter
    fig = px.pie(values=[w_counter,l_counter], names=["wins","losses"], title="winsxlosses ratio")
    responce = plot(fig,output_type="div")
    return responce

def bar_ratio():
    battles_df['victory'] = battles_df['result'].apply(lambda x: 1 if x == "victory" else 0)
    battles_df['defeat'] = battles_df['result'].apply(lambda x: 1 if x != "victory" else 0)
    # Agregace 
    agg_df = battles_df.groupby('mode').sum()[['victory', 'defeat']].reset_index()
    melted_df = agg_df.melt(id_vars='mode', value_vars=['victory', 'defeat'], var_name='result_type', value_name='count')

    fig = px.bar(melted_df, x='mode', y='count', color='result_type', barmode='group',
                labels={'mode': 'Mode', 'count': 'Count', 'result_type': 'Result'},
                title='Wins and Losses by Mode')
    return plot(fig, output_type="div")