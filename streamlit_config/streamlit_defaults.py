import streamlit as st
import pandas as pd
import plotly.express as px
from pickleshare import PickleShareDB
import plotly.graph_objects as go
import os

data_dir = 'prep_data' 
db = PickleShareDB(os.path.join(data_dir, 'kity'))


df_phy_1 = db['df_phy_1']

if 'df_phy_1' in db:
    df_phy_1 = db['df_phy_1']
else:
    print("df_phy_1 n'est pas trouvé dans la base de données.")
if 'df_phy_2' in db:
    df_phy_2 = db['df_phy_2']
else:
    print("df_phy_2 n'est pas trouvé dans la base de données.")
if 'df_phy_3' in db:
    df_phy_3 = db['df_phy_3']
else:
    print("df_phy_3 n'est pas trouvé dans la base de données.")
if 'df_phy_4' in db:
    df_phy_4 = db['df_phy_4']
else:
    print("df_phy_4 n'est pas trouvé dans la base de données.")
if 'df_phy_norm' in db:
    df_phy_norm = db['df_phy_norm']
else:
    print("df_phy_norm n'est pas trouvé dans la base de données.")
if 'df_phy_attack' in db:
    df_phy_attack = db['df_phy_attack']
if 'df_phy_all' in db:
    df_phy_all = db['df_phy_all']
else:
    print("df_phy_all n'est pas trouvé dans la base de données.")
if 'dict_dfs' in db:
    dict_dfs = db['dict_dfs']
else:
    print("dict_dfs n'est pas trouvé dans la base de données.")
if 'df_load_phy_1' in db:
    df_load_phy_1 = db['df_load_phy_1']
else:
    print("df_load_phy_1 n'est pas trouvé dans la base de données.")
if 'df_load_phy_2' in db:
    df_load_phy_2 = db['df_load_phy_2'] 
else:
    print("df_load_phy_2 n'est pas trouvé dans la base de données.")
if 'df_load_phy_3' in db:
    df_load_phy_3 = db['df_load_phy_3']
else:
    print("df_load_phy_3 n'est pas trouvé dans la base de données.")
if 'df_load_phy_4' in db:
    df_load_phy_4 = db['df_load_phy_4']
else:
    print("df_load_phy_4 n'est pas trouvé dans la base de données.")
if 'df_load_phy_norm' in db:
    df_load_phy_norm = db['df_load_phy_norm']
else:
    print("df_load_phy_norm n'est pas trouvé dans la base de données.")
if 'dict_dfs_load' in db:
    dict_dfs_load = db['dict_dfs_load']
else:
    print("dict_dfs_load n'est pas trouvé dans la base de données.")

st.set_page_config(layout="wide")

default_colors = {
    "purple": "#4C2ED6",
    "blue": "#0095FF",
    "blue_green": "#29D49D",
    "green": "#96D400",
    "yellow": "#FFF028",
    "orange": "#FF4600",
    "pink": "#FA186E",
    "brown": "#BD6244",
    "grey": "#696260",
}

attack_color_map = {
    "phy_att_1": default_colors["purple"],
    "phy_att_2": default_colors["blue_green"],
    "phy_att_3": default_colors["yellow"],
    "phy_att_4": default_colors["pink"],
    "phy_norm": default_colors["grey"],
}

attacks_colors = [
    "purple",
    "blue",
    "pink",
    "yellow",
    "orange",
    "brown",
]

normal_colors = [
    "grey",
    "blue_green",
    "green",
]

# create label color map
all_labels = set(df_phy_1["Label"].unique())
all_labels.update(set(df_phy_2["Label"].unique()))
all_labels.update(set(df_phy_3["Label"].unique()))
all_labels.update(set(df_phy_4["Label"].unique()))
all_labels.update(set(df_phy_norm["Label"].unique()))
all_labels = sorted(all_labels)

all_symbols = ["square", "diamond", "cross", "x", "triangle-up", "triangle-down"]

label_color_map = {}
label_symbol_map = {}
i = 0
for label in all_labels:
    if label == "normal":
        label_color_map[label] = default_colors[normal_colors[0]]
        label_symbol_map[label] = "circle"
    else:
        label_color_map[label] = default_colors[attacks_colors[i]]
        label_symbol_map[label] = all_symbols[i]
        i += 1
        if i >= len(attacks_colors):
            raise ValueError("Not enough colors in attacks_colors to map all labels.")
        if i >= len(all_symbols):
            raise ValueError("Not enough symbols to map all labels.")
        