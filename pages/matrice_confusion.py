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

st.table(df_selected)

conf_matrix_str = df_selected["confusion_matrix"].iloc[0]
conf_matrix_str_cleaned = re.sub(r"\s+", ",", conf_matrix_str)
conf_matrix_str_cleaned = conf_matrix_str_cleaned.replace("][", "],[")
conf_matrix_str_cleaned = conf_matrix_str_cleaned.replace("[,", "[")
conf_matrix = ast.literal_eval(conf_matrix_str_cleaned)

if attack_types[attack_choice] == "labeln":
    labels = [0, 1]

else:
    label_mapping = db["label_mapping"]
    labels = list(label_mapping.keys())
    labels = list(map(str, labels))


fig = go.Figure(
    data=go.Heatmap(
        z=conf_matrix,
        x=labels,
        y=labels,
        colorscale="viridis",
        colorbar=dict(title="Nombre de prédictions"),
        hoverongaps=False,
        text=conf_matrix,
        texttemplate="%{text}",
        showscale=True,
    )
)

fig.update_layout(
    title="Matrice de confusion interactive",
    xaxis_title="Valeurs prédites",
    yaxis_title="Valeurs réelles",
    xaxis=dict(tickmode="array", tickvals=np.arange(len(labels))),
    yaxis=dict(tickmode="array", tickvals=np.arange(len(labels))),
    autosize=True,
)

st.plotly_chart(fig)


if attack_types[attack_choice] != "labeln":

    tp = df_selected["TP"].iloc[0]
    tn = df_selected["TN"].iloc[0]
    fp = df_selected["FP"].iloc[0]
    fn = df_selected["FN"].iloc[0]

    conf_matrix_01 = np.array([[tn, fp], [fn, tp]])

    print(conf_matrix_01)

    fig = go.Figure(
        data=go.Heatmap(
            z=conf_matrix_01,
            x=[0, 1],
            y=[0, 1],
            colorscale="viridis",
            colorbar=dict(title="Nombre de prédictions"),
            hoverongaps=False,
            text=conf_matrix_01,
            texttemplate="%{text}",
            showscale=True,
        )
    )

    fig.update_layout(
        title="Matrice de confusion 0/1",
        xaxis_title="Valeurs prédites",
        yaxis_title="Valeurs réelles",
        xaxis=dict(tickmode="array", tickvals=np.arange(2)),
        yaxis=dict(tickmode="array", tickvals=np.arange(2)),
        autosize=True,
    )

    st.plotly_chart(fig)
