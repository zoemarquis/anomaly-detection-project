from streamlit_config.streamlit_defaults import *

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler

# Titre principal
st.title("Analyse exploratoire des données physiques")


# Sidebar pour la sélection du dataframe
st.sidebar.header("Sélection du DataFrame")
selected_df_name = st.sidebar.selectbox(
    "Choisissez un DataFrame :", list(dict_dfs_load.keys())
)
selected_df = dict_dfs_load[selected_df_name]

# Affichage de la structure des données
st.subheader("1. Structure des données")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Nombre de lignes", value=f"{selected_df.shape[0]}")
with col2:
    st.metric(label="Nombre de colonnes", value=f"{selected_df.shape[1]}")


st.subheader("2. Types de colonnes")

# Identifier les colonnes numériques et catégorielles
numeric_columns = selected_df.select_dtypes(include=["number"]).columns.tolist()
categorical_columns = selected_df.select_dtypes(include=["object", "category"]).columns.tolist()
datetime_columns = selected_df.select_dtypes(include=["datetime"]).columns.tolist()

# Affichage sous forme de colonnes pour plus de lisibilité
col1, col2 , col3= st.columns(3)

with col1:
    st.write("### Colonnes numériques")
    st.write(f"**{len(numeric_columns)} colonnes**")
    st.write(numeric_columns if numeric_columns else "Aucune")

with col3:
    st.write("### Colonnes catégorielles")
    st.write(f"**{len(categorical_columns)} colonnes**")
    st.write(categorical_columns if categorical_columns else "Aucune")

with col2:  
    boolean_columns = selected_df.select_dtypes(include=["bool"]).columns.tolist()
    st.write("### Colonnes booléennes")
    st.write(f"**{len(boolean_columns)} colonnes**")
    st.write(boolean_columns if boolean_columns else "Aucune")

# Statistiques descriptives
st.subheader("3. Statistiques descriptives")
st.write(selected_df.describe(include="all"))

st.subheader("Nombre de valeurs différentes par colonne")
unique_values_df = selected_df.nunique().reset_index()
unique_values_df.columns = ["Colonne", "Nombre de valeurs uniques"]
st.write(unique_values_df)

# Valeurs manquantes
st.subheader("4. Valeurs manquantes")
missing_values = selected_df.isnull().sum()
st.write(missing_values[missing_values > 0])

st.subheader("5. Analyse des labels")

# # Analyse des labels
# if "Label" in selected_df.columns:
#     st.bar_chart(selected_df["Label"].value_counts())
#     st.write("Crosstabulation des labels et des autres colonnes :")
#     selected_col = st.selectbox("Choisissez une colonne pour crosstab :", selected_df.columns)
#     st.write(pd.crosstab(selected_df["Label"], selected_df[selected_col]))


dict_dfs_sans_all = {k: v for k, v in dict_dfs.items() if k != "all"}

# --------------------------------------------------------------------

data_ = []
unique_labels_ = set()

for name, df in dict_dfs_sans_all.items():
    label_counts = df["Label"].value_counts()
    unique_labels_.update(label_counts.index)
    for label, count in label_counts.items():
        data_.append({"Dataset": name, "Label": label, "Count": count})
data_df = pd.DataFrame(data_)
fig = px.bar(
    data_df,
    x="Dataset",
    y="Count",
    color="Label",
    color_discrete_map=label_color_map,
    title="Répartition des labels par dataset",
    labels={"Count": "Nombre d'étiquettes"},
)
st.plotly_chart(fig)


# --------------------------------------------------------------------

max_len = max(len(df) for df in dict_dfs_sans_all.values())
fig = make_subplots(
    rows=5,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.05,
)
# Ajout de chaque dataset en tant que scatter plot, étiré sur la largeur maximale
for i, (key, df) in enumerate(dict_dfs_sans_all.items(), start=1):
    x_values = list(range(max_len))  # Plage d'index pour alignement maximal
    y_values = i * np.ones(max_len)
    # Ajout de points existants et espaces vides pour remplir la longueur
    fig.add_trace(
        go.Scatter(
            x=x_values[
                : len(df)
            ],  # Seule la partie de x correspondant à la longueur du dataset
            y=y_values[: len(df)],
            mode="markers",
            marker=dict(
                color=df["Label"].map(label_color_map),
                size=10,  # Taille ajustée pour des formes rectangulaires
                symbol="square",
                # symbol=df["Label"].map(label_symbols)
            ),
            text=df["Label"],
        ),
        row=i,
        col=1,
    )
# Mise à jour de la mise en page pour afficher les noms et les légendes
fig.update_layout(
    height=500,
    title_text="Barcode Chart alignés pour 5 séries temporelles (après nettoyage des données)",
    template="simple_white",
    showlegend=False  # Désactiver l'affichage de la légende
)
# Afficher les ticks de l'axe x seulement pour le dernier sous-graphe
fig.update_xaxes(title_text="Time", showticklabels=True, row=5, col=1)
# Mise à jour de l'axe y pour chaque sous-graphe pour afficher le nom du dataset
for i, key in enumerate(dict_dfs_sans_all.keys(), start=1):
    fig.update_yaxes(
        title_text=key, row=i, col=1, showticklabels=False
    )  # , orientation="horizontal")
st.plotly_chart(fig)
#--------------------------------------------------------------------

# 6. Distribution des données
st.subheader("6. Distribution des données")
col_choice = st.selectbox("Choisissez une colonne pour visualiser la distribution :", selected_df.columns)

col1, col2 = st.columns(2)

fig_width = 6  # largeur en pouces
fig_height = 4  # hauteur en pouces

with col1:
    # Histogramme
    st.write(f"Histogramme de {col_choice}")
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    sns.histplot(selected_df[col_choice], kde=True, ax=ax)
    st.pyplot(fig)

with col2:
    # Boxplot
    st.write(f"Boxplot de {col_choice}")
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    sns.boxplot(x=selected_df[col_choice], ax=ax)
    st.pyplot(fig)

st.divider()


def get_df_encoded(
    df,
):  # ici one hot, d'autres sont possibles (genre le label encoder ?)
    cat_cols = df.select_dtypes(exclude=[np.number]).columns
    df_encoded = pd.get_dummies(df, columns=cat_cols)
    return df_encoded


for df in [df_phy_1, df_phy_2, df_phy_3, df_phy_4, df_phy_norm]:
    df["Flow_sensor_1"] = pd.to_numeric(df["Flow_sensor_1"], errors="coerce")
    df["Flow_sensor_2"] = (
        df["Flow_sensor_2"].apply(lambda x: 4000 if x else 0).astype(int)
    )

# a : numériques
df_phy_1_num = df_phy_1.select_dtypes(include=[np.number])
df_phy_2_num = df_phy_2.select_dtypes(include=[np.number])
df_phy_3_num = df_phy_3.select_dtypes(include=[np.number])
df_phy_4_num = df_phy_4.select_dtypes(include=[np.number])
df_phy_norm_num = df_phy_norm.select_dtypes(include=[np.number])


scaler = StandardScaler()
df_phy_1_num_scaled = pd.DataFrame(
    scaler.fit_transform(df_phy_1_num), columns=df_phy_1_num.columns
)
df_phy_2_num_scaled = pd.DataFrame(
    scaler.fit_transform(df_phy_2_num), columns=df_phy_2_num.columns
)
df_phy_3_num_scaled = pd.DataFrame(
    scaler.fit_transform(df_phy_3_num), columns=df_phy_3_num.columns
)
df_phy_4_num_scaled = pd.DataFrame(
    scaler.fit_transform(df_phy_4_num), columns=df_phy_4_num.columns
)
df_phy_norm_num_scaled = pd.DataFrame(
    scaler.fit_transform(df_phy_norm_num), columns=df_phy_norm_num.columns
)

# 1a
df_phy_att_num_scaled = pd.concat(
    [
        df_phy_1_num_scaled,
        df_phy_2_num_scaled,
        df_phy_3_num_scaled,
        df_phy_4_num_scaled,
    ]
)

df_phy_norm_num_scaled = df_phy_norm_num_scaled

# 2a
df_phy_all_num_scaled = pd.concat(
    [
        df_phy_1_num_scaled,
        df_phy_2_num_scaled,
        df_phy_3_num_scaled,
        df_phy_4_num_scaled,
        df_phy_norm_num_scaled,
    ]
)

# Visualisation

corr_att_num = df_phy_att_num_scaled.corr()
corr_norm_num = df_phy_norm_num_scaled.corr()
corr_all_num = df_phy_all_num_scaled.corr()

# Création des heatmaps
fig_att = px.imshow(
    corr_att_num,
    title="Matrice de corrélations des 4 datasets d'attaque",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
)
fig_norm = px.imshow(
    corr_norm_num,
    title="Matrice de corrélations du dataset normal",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
)
fig_all = px.imshow(
    corr_all_num,
    title="Matrice de corrélations avec tous les datasets",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
)

# Affichage des heatmaps dans Streamlit sur la même ligne
st.subheader("7. Corrélations entre les colonnes numériques (pour tous les datasets)")


# Utilisation de st.columns pour afficher les matrices sur la même ligne
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(fig_att)

with col2:
    st.plotly_chart(fig_norm)

with col3:
    st.plotly_chart(fig_all)


# 1 b et 2 b : trop lourd l'encodage: trop de colonnes
