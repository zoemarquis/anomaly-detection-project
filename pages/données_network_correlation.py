import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import OrdinalEncoder
from pickleshare import PickleShareDB

# Chargement des données
@st.cache_resource
def chargement_des_donnees():
    db = PickleShareDB("./prep_data/kity/")
    dataframes = {}
    try:
        df_net_1 = db["net_attack_1_clean"]
        df_net_2 = db["net_attack_2_clean"]
        df_net_3 = db["net_attack_3_clean"]
        df_net_4 = db["net_attack_4_clean"]
        df_net_norm = db["net_norm_clean"]
        dataframes = {
            "Attaque 1": df_net_1,
            "Attaque 2": df_net_2,
            "Attaque 3": df_net_3,
            "Attaque 4": df_net_4,
            "Normal": df_net_norm,
        }
        return dataframes
    except KeyError as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return {}


dataframes = chargement_des_donnees()

# Sélection du dataset
st.title("Visualisation des données")
dataset_name = st.selectbox("Sélectionnez un dataset :", options=list(dataframes.keys()))

if dataset_name:
    df = dataframes[dataset_name]

    # Changement du type pour être mieux géré par Streamlit
    df = df.astype({col: 'str' for col in df.select_dtypes(include=['category']).columns})

    # Infos sur le dataset
    st.write(f"### Aperçu du dataset : {dataset_name}")
    st.dataframe(df.head())

    
    # Distribution des colonnes numériques
    label_col = 'label' if 'label' in df.columns else 'label_n'
    st.write(f"### Distribution des colonnes numériques pour : {dataset_name}")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        fig = px.histogram(
            df, x=col, color=label_col, title=f"Distribution de {col} par {label_col}", nbins=50
        )
        st.plotly_chart(fig, use_container_width=True)

    # Encodage des objets
    object_cols = df.select_dtypes(include=["object"]).columns
    ordinal_encoder = OrdinalEncoder()
    df[object_cols] = ordinal_encoder.fit_transform(df[object_cols].astype(str))

    # Suppression des colonnes inutiles 
    #df = df.drop(columns=['label', 'label_n'])
    
    # Matrice de corrélation
    correlation_matrix = df.corr()

    st.write(f"### Matrice de corrélation pour : {dataset_name}")
    fig = px.imshow(
        correlation_matrix,
        #title=f"Matrice de corrélation du dataset {dataset_name}",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        height=600,
        width=600,
    )
    st.plotly_chart(fig, use_container_width=True)