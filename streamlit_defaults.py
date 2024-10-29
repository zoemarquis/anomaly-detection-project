import streamlit as st

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

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

st.set_page_config(layout="wide")


# load data
df_phy_1 = pd.read_csv(
    "dataset/Physical dataset/phy_att_1.csv", encoding="utf-16", sep="\t"
)
df_phy_2 = pd.read_csv(
    "dataset/Physical dataset/phy_att_2.csv", encoding="utf-16", sep="\t"
)
df_phy_3 = pd.read_csv(
    "dataset/Physical dataset/phy_att_3.csv", encoding="utf-16", sep="\t"
)
df_phy_4 = pd.read_csv(
    "dataset/Physical dataset/phy_att_4.csv", encoding="utf-8", sep=","
)
df_phy_norm = pd.read_csv(
    "dataset/Physical dataset/phy_norm.csv", encoding="utf-16", sep="\t"
)

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
