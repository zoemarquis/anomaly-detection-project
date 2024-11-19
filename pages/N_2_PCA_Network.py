import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import OrdinalEncoder
from pickleshare import PickleShareDB
import plotly.graph_objects as go

# Chargement des données
@st.cache_resource
def chargement_des_donnees():
    db = PickleShareDB("./prep_data/kity/")
    dataframes = {}
    try:
        df_net_1_clean = db["net_attack_1_clean"]
        df_net_2_clean = db["net_attack_2_clean"]
        df_net_3_clean = db["net_attack_3_clean"]
        df_net_4_clean = db["net_attack_4_clean"]
        df_net_norm_clean = db["net_norm_clean"]

        pca_table_1 = db["pca_variance_table_net_1"]
        pca_table_2 = db["pca_variance_table_net_2"]
        pca_table_3 = db["pca_variance_table_net_3"]
        pca_table_4 = db["pca_variance_table_net_4"]
        pca_table_norm = db["pca_variance_table_net_norm"]

        #df_net_1 = db["net_attack_1"]
        #df_net_2 = db["net_attack_2"]
        #df_net_3 = db["net_attack_3"]
        #df_net_4 = db["net_attack_4"]
        #df_net_norm = db["net_norm"]
        
        #dataframes = {
        #    "Attaque 1": df_net_1,
        #    "Attaque 2": df_net_2,
        #    "Attaque 3": df_net_3,
        #    "Attaque 4": df_net_4,
        #    "Normal": df_net_norm,
        #}

        dataframes_clean = {
            "Attaque 1": df_net_1_clean,
            "Attaque 2": df_net_2_clean,
            "Attaque 3": df_net_3_clean,
            "Attaque 4": df_net_4_clean,
            "Normal": df_net_norm_clean,
        }

        pca_tables = {
            "Attaque 1": pca_table_1,
            "Attaque 2": pca_table_2,
            "Attaque 3": pca_table_3,
            "Attaque 4": pca_table_4,
            "Normal": pca_table_norm,
        }

        return pca_tables, dataframes_clean
    except KeyError as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return {}


pca_tables, dataframes_clean = chargement_des_donnees()


dataset_name = st.selectbox("Sélectionnez un dataset :", options=list(dataframes_clean.keys()))

if dataset_name:
    df = dataframes_clean[dataset_name]

    # Changement du type pour être mieux géré par Streamlit
    df = df.astype({col: 'str' for col in df.select_dtypes(include=['category']).columns})

    object_cols = df.select_dtypes(include=["object"]).columns
    ordinal_encoder = OrdinalEncoder()
    df[object_cols] = ordinal_encoder.fit_transform(df[object_cols].astype(str))

    #df = df.drop(columns=['label', 'label_n'])
    
    # Matrice de corrélation
    correlation_matrix = df.corr()

    st.write(f"### Matrice de corrélation")
    fig = px.imshow(correlation_matrix, color_continuous_scale="RdBu", zmin=-1, zmax=1, height=600, width=600)
    st.plotly_chart(fig, use_container_width=True)

    # Affichage des résultats PCA
    st.write(f"### Réduction de  dimension - PCA")
    st.subheader(f"#### Variance expliquée")

    variance_table = pca_tables[dataset_name]

    #st.dataframe(variance_table)

    fig_pca = go.Figure()
    fig_pca.add_trace(go.Bar(x=variance_table["Composante"], y=variance_table["Pourcentage de Variance Expliquée"], name="Variance Expliquée (%)"))

    fig_pca.add_trace(go.Scatter( x=variance_table["Composante"], y=variance_table["Total"], mode="lines+markers", name="Cumul de la Variance (%)"))

    fig_pca.update_layout(title=f"Variance expliquée pour PCA - {dataset_name}", xaxis_title="Composantes principales", yaxis_title="Pourcentage de Variance", barmode="group")

    st.plotly_chart(fig_pca, use_container_width=True)
