import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import OrdinalEncoder
from pickleshare import PickleShareDB
import plotly.graph_objects as go
import concurrent.futures

# Chargement des données
@st.cache_resource
def chargement_des_donnees():
    db = PickleShareDB("./prep_data/kity/")

    dataset_keys = {
        "net_attack_1": ("dataframes", "Attaque 1"),
        "net_attack_2": ("dataframes", "Attaque 2"),
        "net_attack_3": ("dataframes", "Attaque 3"),
        "net_attack_4": ("dataframes", "Attaque 4"),
        "net_norm": ("dataframes", "Normal"),
        "net_attack_1_clean": ("dataframes_clean", "Attaque 1"),
        "net_attack_2_clean": ("dataframes_clean", "Attaque 2"),
        "net_attack_3_clean": ("dataframes_clean", "Attaque 3"),
        "net_attack_4_clean": ("dataframes_clean", "Attaque 4"),
        "net_norm_clean": ("dataframes_clean", "Normal"),
        "pca_variance_table_net_1": ("pca_tables", "Attaque 1"),
        "pca_variance_table_net_2": ("pca_tables", "Attaque 2"),
        "pca_variance_table_net_3": ("pca_tables", "Attaque 3"),
        "pca_variance_table_net_4": ("pca_tables", "Attaque 4"),
        "pca_variance_table_net_norm": ("pca_tables", "Normal"),
    }

    def charger_cle(key, category, name):
        try:
            return category, name, db[key]
        except KeyError as e:
            st.error(f"Erreur lors du chargement de {key}: {e}")
            return category, name, None

    # Limitation du nombre de threads
    max_threads = 4
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(charger_cle, key, category, name)
            for key, (category, name) in dataset_keys.items()
        ]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    dataframes = {}
    dataframes_clean = {}
    pca_tables = {}

    for category, name, data in results:
        if data is not None:
            if category == "dataframes":
                dataframes[name] = data
            elif category == "dataframes_clean":
                dataframes_clean[name] = data
            elif category == "pca_tables":
                pca_tables[name] = data

    return dataframes, dataframes_clean, pca_tables


dataframes, dataframes_clean, pca_tables = chargement_des_donnees()

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

    fig_label.update_layout(title="Répartition des labels", xaxis_title="Label", yaxis_title="Nombre", barmode="stack")
    st.plotly_chart(fig_label)
    
with col2:
    fig_label_by_file = go.Figure()

    unique_labels = set()
    for df in dataframes_clean.values():
        unique_labels.update(df["label"].unique())

    for label in unique_labels:
        label_counts = [df[df["label"] == label].shape[0] for df in dataframes_clean.values()]
        fig_label_by_file.add_trace(go.Bar(x=list(dataframes_clean.keys()), y=label_counts, name=str(label)))

    fig_label_by_file.update_layout(title="Répartition des labels dans les fichiers", xaxis_title="Fichier", yaxis_title="Nombre", barmode="stack")

    st.plotly_chart(fig_label_by_file)

dataset_name = st.selectbox("Sélectionnez un dataset :", options=list(dataframes_clean.keys()))



if dataset_name:
    df = dataframes[dataset_name]
    df_clean = dataframes_clean[dataset_name]

    # Sample pour éviter que ce soit trop long
    sample_size = 500000
    df_sampled = df.sample(n=sample_size, random_state=42)
    df_clean_sampled = df_clean.sample(n=sample_size, random_state=42)

    df = df_sampled
    df_clean = df_clean_sampled


    # Statistiques sur les valeurs numériques
    st.write("## Distribution des valeurs numériques continues")

    columns_to_plot = ["size", "n_pkt_src", "n_pkt_dst"]

    cols = st.columns(3)
    for col, column_name in zip(cols, columns_to_plot):
        with col:
            fig = px.box(df, x="label", y=column_name, color="label", title=f"Distribution pour {column_name}", labels={column_name: f"Valeurs de {column_name}", "label": "Label"})
            st.plotly_chart(fig)


    # Nombre de valeurs uniques pour les colonnes discrètes
    st.write(f"## Distribution des valeurs dicrètes")

    discrete_columns = ['mac_s', 'mac_d', 'ip_s', 'ip_d', 'sport', 'dport', 'proto', 'flags', 'modbus_fn', 'modbus_response']

    unique_counts = {col: df[col].nunique() for col in discrete_columns}

    unique_counts_df = pd.DataFrame(list(unique_counts.items()), columns=['Column', 'Unique Values'])
    unique_counts_df = unique_counts_df.sort_values(by='Unique Values')

    fig = px.bar(unique_counts_df, x='Unique Values', y='Column', orientation='h', title="Nombre de valeurs uniques par colonne discrète", labels={'Unique Values': "Nombre de valeurs uniques", 'Column': "Colonnes"})


    st.plotly_chart(fig)

    # Statistiques sur les valeurs discrètes (peu de valeurs uniques)
    st.write(f"### Ditribution des valeurs discrètes avec peu de valeurs uniques")

    columns_to_plot = ['mac_s', 'mac_d', 'ip_s', 'ip_d', 'proto', 'flags', 'modbus_fn']

    columns_row1 = columns_to_plot[:4]
    columns_row2 = columns_to_plot[4:]

    cols1 = st.columns(len(columns_row1))
    for col, column in zip(cols1, columns_row1):
        with col:
            fig = px.histogram(df, x=column, color="label", barmode="stack", title=f"Distribution de {column}", labels={column: "Valeurs", "label": "Label"}, nbins=50)
            st.plotly_chart(fig, use_container_width=True)

    cols2 = st.columns(len(columns_row2))
    for col, column in zip(cols2, columns_row2):
        with col:
            fig = px.histogram(df, x=column, color="label", barmode="stack", title=f"Distribution de {column}", labels={column: "Valeurs", "label": "Label"}, nbins=50)
            st.plotly_chart(fig, use_container_width=True)
        
    # Statistiques sur les valeurs discrètes (beaucoup de valeurs uniques)
    st.write(f"### Ditribution des valeurs discrètes avec beaucoup de valeurs uniques")

    columns_to_plot = ['sport', 'dport', 'modbus_response']

    cols = st.columns(len(columns_to_plot))

    for col, column in zip(cols, columns_to_plot):
        with col:
            fig = px.histogram(df_clean, x=column, color="label", barmode="stack", title=f"Distribution de {column}", labels={column: "Valeurs", "label": "Label"}, nbins=50)
            st.plotly_chart(fig, use_container_width=True)

    # Changement du type pour être mieux géré par Streamlit
    df = df.astype({col: 'str' for col in df.select_dtypes(include=['category']).columns})

    object_cols = df.select_dtypes(include=["object"]).columns
    ordinal_encoder = OrdinalEncoder()
    df[object_cols] = ordinal_encoder.fit_transform(df[object_cols].astype(str))
    

    # Matrice de corrélation
    correlation_matrix = df.corr()

    st.write(f"### Matrice de corrélation")
    fig = px.imshow(correlation_matrix, color_continuous_scale="RdBu", zmin=-1, zmax=1, height=600, width=600)
    st.plotly_chart(fig, use_container_width=True)


    # Affichage des résultats PCA
    st.write(f"## Réduction de  dimension - PCA")
    st.write(f"### Variance expliquée")

    variance_table = pca_tables[dataset_name]

    #st.dataframe(variance_table)

    fig_pca = go.Figure()
    fig_pca.add_trace(go.Bar(x=variance_table["Composante"], y=variance_table["Pourcentage de Variance Expliquée"], name="Variance Expliquée (%)"))

    fig_pca.add_trace(go.Scatter( x=variance_table["Composante"], y=variance_table["Total"], mode="lines+markers", name="Cumul de la Variance (%)"))

    fig_pca.update_layout(xaxis_title="Composantes principales", yaxis_title="Pourcentage de Variance", barmode="group")

    st.plotly_chart(fig_pca, use_container_width=True)

