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
        
        df_matrix_clean = [df_net_1_clean, df_net_2_clean, df_net_3_clean, df_net_4_clean]
        df_matrix_clean = pd.concat(df_matrix_clean, axis=0, ignore_index=True)
        df_matrix_clean = df_matrix_clean.groupby('label', group_keys=False).apply(
            lambda x: x.sample(frac=0.25, random_state=42)
        )
        
        df_net_1 = db["net_attack_1"]
        df_net_2 = db["net_attack_2"]
        df_net_3 = db["net_attack_3"]
        df_net_4 = db["net_attack_4"]
        df_net_norm = db["net_norm"]
        
        pca_table = db["pca_variance_table_df_net"]
        
        dataframes = {
            "Attaque 1": df_net_1,
            "Attaque 2": df_net_2,
            "Attaque 3": df_net_3,
            "Attaque 4": df_net_4,
            "Normal": df_net_norm,
        }
        dataframes_clean = {
            "Attaque 1": df_net_1_clean,
            "Attaque 2": df_net_2_clean,
            "Attaque 3": df_net_3_clean,
            "Attaque 4": df_net_4_clean,
            "Normal": df_net_norm_clean,
        }

        return dataframes, dataframes_clean, pca_table, df_matrix_clean


    except KeyError as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return {}


dataframes, dataframes_clean, pca_table, df_matrix = chargement_des_donnees()

for key, df in dataframes.items():
    dataframes[key].columns = df.columns.str.strip()

st.write(f"# Exploration des jeux de données réseau")
st.write(f"## Répartition des labels")
col1, col2 = st.columns(2)

with col1:
    fig_label = go.Figure()
    for name, df in dataframes_clean.items():
        label_counts = df["label"].value_counts()
        fig_label.add_trace(go.Bar(x=label_counts.index, y=label_counts.values, name=name))

    fig_label.update_layout(title="Répartition des labels (données nettoyées)", xaxis_title="Label", yaxis_title="Nombre", barmode="stack")
    st.plotly_chart(fig_label)
    
with col2:
    fig_label_by_file = go.Figure()

    unique_labels = set()
    for df in dataframes_clean.values():
        unique_labels.update(df["label"].unique())

    for label in unique_labels:
        label_counts = [df[df["label"] == label].shape[0] for df in dataframes_clean.values()]
        fig_label_by_file.add_trace(go.Bar(x=list(dataframes_clean.keys()), y=label_counts, name=str(label)))

    fig_label_by_file.update_layout(title="Répartition des labels dans les fichiers (données nettoyées)", xaxis_title="Fichier", yaxis_title="Nombre", barmode="stack")

    st.plotly_chart(fig_label_by_file)

dataset_name = st.selectbox("Sélectionnez un dataset :", options=list(dataframes_clean.keys()))

st.write(f"Un échantillon représentatif de 500 000 lignes du fichier sélectionné est utilisé.")

if dataset_name:
    df = dataframes[dataset_name]
    df_clean = dataframes_clean[dataset_name]
    
    sample_size = 500000
    df_sampled = df.sample(n=sample_size, random_state=42)
    df_clean_sampled = df_clean.sample(n=sample_size, random_state=42)

    df = df_sampled
    df_clean = df_clean_sampled


    # Statistiques sur les valeurs numériques
    st.write(f"## Distribution des valeurs numériques continues")

    columns_to_plot = ["size", "n_pkt_src", "n_pkt_dst"]

    cols = st.columns(3)
    for col, column_name in zip(cols, columns_to_plot):
        with col:
            fig = px.box(df, x="label", y=column_name, color="label", title=f"Distribution pour {column_name} (données initiales)", labels={column_name: f"Valeurs de {column_name}", "label": "Label"})
            st.plotly_chart(fig)


    # Nombre de valeurs uniques pour les colonnes discrètes
    st.write(f"## Distribution des valeurs discrètes")

    discrete_columns = ['mac_s', 'mac_d', 'ip_s', 'ip_d', 'sport', 'dport', 'proto', 'flags', 'modbus_fn', 'modbus_response']

    unique_counts = {col: df[col].nunique() for col in discrete_columns}

    unique_counts_df = pd.DataFrame(list(unique_counts.items()), columns=['Column', 'Unique Values'])
    unique_counts_df = unique_counts_df.sort_values(by='Unique Values')

    fig = px.bar(unique_counts_df, x='Unique Values', y='Column', orientation='h', title="Nombre de valeurs uniques par colonne discrète (données initiales)", labels={'Unique Values': "Nombre de valeurs uniques", 'Column': "Colonnes"})


    st.plotly_chart(fig)

    # Statistiques sur les valeurs discrètes (peu de valeurs uniques)
    st.write(f"### Distribution des valeurs discrètes avec peu de valeurs uniques")

    columns_to_plot = ['mac_s', 'mac_d', 'ip_s', 'ip_d', 'proto', 'flags', 'modbus_fn']

    columns_row1 = columns_to_plot[:4]
    columns_row2 = columns_to_plot[4:]

    cols1 = st.columns(len(columns_row1))
    for col, column in zip(cols1, columns_row1):
        with col:
            fig = px.histogram(df, x=column, color="label", barmode="stack", title=f"Distribution {column} (données initiales)", labels={column: "Valeurs", "label": "Label"}, nbins=50)
            st.plotly_chart(fig, use_container_width=True)

    cols2 = st.columns(len(columns_row2))
    for col, column in zip(cols2, columns_row2):
        with col:
            fig = px.histogram(df, x=column, color="label", barmode="stack", title=f"Distribution {column} (données initiales)", labels={column: "Valeurs", "label": "Label"}, nbins=50)
            st.plotly_chart(fig, use_container_width=True)
        
    # Statistiques sur les valeurs discrètes (beaucoup de valeurs uniques)
    st.write(f"### Distribution des valeurs discrètes avec beaucoup de valeurs uniques")

    columns_to_plot = ['sport', 'dport', 'modbus_response']

    cols = st.columns(len(columns_to_plot))

    for col, column in zip(cols, columns_to_plot):
        with col:
            fig = px.histogram(df_clean, x=column, color="label", barmode="stack", title=f"Distribution {column} (données nettoyées)", labels={column: "Valeurs", "label": "Label"}, nbins=50)
            st.plotly_chart(fig, use_container_width=True)

    

    # Matrice de corrélation
    df_matrix = df_matrix.astype({col: 'str' for col in df_matrix.select_dtypes(include=['category']).columns})
        
    object_cols = df_matrix.select_dtypes(include=["object"]).columns
    ordinal_encoder = OrdinalEncoder()
    df_matrix[object_cols] = ordinal_encoder.fit_transform(df_matrix[object_cols].astype(str))

    correlation_matrix = df_matrix.corr()

    st.write(f"## Matrice de corrélation (échantillon des 4 fichiers d'attaques)")
    fig = px.imshow(correlation_matrix, color_continuous_scale="RdBu", zmin=-1, zmax=1, height=600, width=600)
    st.plotly_chart(fig, use_container_width=True)



    # Affichage des résultats PCA
    st.write(f"## Réduction de  dimension - PCA")
    st.write(f"### Variance expliquée (échantillon des 4 fichiers d'attaques)")

    variance_table = pca_table

    #st.dataframe(variance_table)

    fig_pca = go.Figure()
    fig_pca.add_trace(go.Bar(x=variance_table["Composante"], y=variance_table["Pourcentage de Variance Expliquée"], name="Variance Expliquée (%)"))

    fig_pca.add_trace(go.Scatter( x=variance_table["Composante"], y=variance_table["Total"], mode="lines+markers", name="Cumul de la Variance (%)"))

    fig_pca.update_layout(xaxis_title="Composantes principales", yaxis_title="Pourcentage de Variance", barmode="group")

    st.plotly_chart(fig_pca, use_container_width=True)

