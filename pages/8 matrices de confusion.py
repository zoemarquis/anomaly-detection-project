import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from streamlit_config.streamlit_defaults import *
from streamlit_config.utils import *
from streamlit_config.article_data import *
import plotly.graph_objects as go
import ast
import re

dataset_choice = st.sidebar.selectbox(
    "Sélectionnez le type de données :", list(selec_dataset.keys())
)


if selec_dataset[dataset_choice] == "PHY":
    attack_types = attack_types_phy
else:
    attack_types = attack_types_net

attack_choice = st.sidebar.selectbox(
    "Sélectionnez le type d'attaque :", list(attack_types.keys())
)

if selec_dataset[dataset_choice] == "PHY":
    model_names = model_names_phy
else:
    model_names = model_names_netw
model_choice = st.sidebar.selectbox(
    "Sélectionnez le modèle :", list(model_names.keys())
)

dataset_name = f"{selec_dataset[dataset_choice]}_results_{model_names[model_choice]}_{attack_types[attack_choice]}"
df_selected = df_results[(df_results["filename"] == dataset_name)]

conf_matrix_str = df_selected["confusion_matrix"].iloc[0]
conf_matrix_str_cleaned = re.sub(r"\s+", ",", conf_matrix_str)
conf_matrix_str_cleaned = conf_matrix_str_cleaned.replace("][", "],[")
conf_matrix_str_cleaned = conf_matrix_str_cleaned.replace("[,", "[")
conf_matrix = ast.literal_eval(conf_matrix_str_cleaned)

if attack_types[attack_choice] == "labeln" or (selec_dataset[dataset_choice] == "PHY" and model_names[model_choice] != "cnn1d"):
    labels = [0, 1]

else:
    if selec_dataset[dataset_choice] == "PHY":
        label_mapping = db["label_mapping"]
    else:
        label_mapping = db["label_mapping_network"]
    labels = list(label_mapping.keys())
    labels = list(map(str, labels))


fig1 = go.Figure(
    data=go.Heatmap(
        z=conf_matrix,
        x=labels,
        y=labels,
        colorscale="Blues",
        colorbar=dict(title="Nombre de prédictions"),
        hoverongaps=False,
        text=conf_matrix,
        texttemplate="%{text}",
        showscale=True,
    )
)

fig1.update_layout(
    title="Matrice de confusion binaire"
    if attack_types[attack_choice] == "labeln"
    else "Matrice de confusion multiclasse",
    xaxis_title="Valeurs prédites",
    yaxis_title="Valeurs réelles",
    xaxis=dict(tickmode="array", tickvals=np.arange(len(labels))),
    yaxis=dict(tickmode="array", tickvals=np.arange(len(labels))),
    height=600,
    width=700,
    # autosize=True,
)


col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1)

if (selec_dataset[dataset_choice] == "NETW" and attack_types [attack_choice]!="labeln") or (selec_dataset[dataset_choice] == "PHY" and model_names[model_choice] == "cnn1d" and attack_types[attack_choice] != "labeln"):
    tp = df_selected["TP"].iloc[0]
    tn = df_selected["TN"].iloc[0]
    fp = df_selected["FP"].iloc[0]
    fn = df_selected["FN"].iloc[0]

    conf_matrix_01 = np.array([[tn, fp], [fn, tp]])

    fig2 = go.Figure(
        data=go.Heatmap(
            z=conf_matrix_01,
            x=[0, 1],
            y=[0, 1],
            colorscale="Blues",
            colorbar=dict(title="Nombre de prédictions"),
            hoverongaps=False,
            text=conf_matrix_01,
            texttemplate="%{text}",
            showscale=True,
        )
    )

    fig2.update_layout(
        title="Matrice de confusion binaire résumée pour l'attaque spécifiée",
        xaxis_title="Valeurs prédites",
        yaxis_title="Valeurs réelles",
        xaxis=dict(tickmode="array", tickvals=np.arange(2)),
        yaxis=dict(tickmode="array", tickvals=np.arange(2)),
        height=600,
        width=700,
        # autosize=True,
    )

    # st.plotly_chart(fig2)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
