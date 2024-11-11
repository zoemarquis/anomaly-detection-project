from streamlit_config.streamlit_defaults import *  # Assure-toi que cette bibliothèque est bien configurée pour charger les DataFrames
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# Sidebar pour la sélection du dataframe
st.sidebar.header("Sélection du DataFrame")
selected_df_name = st.sidebar.selectbox(
    "Choisissez un DataFrame :", list(dict_dfs_load.keys())
)
selected_df = dict_dfs_load[selected_df_name]


selected_df["Time"] = pd.to_datetime(selected_df["Time"])
tick_vals = selected_df["Time"][::60]  # Prendre un échantillon toutes les 10 lignes
tick_text = tick_vals.dt.strftime("%H:%M")


# Titre principal de la page
st.title("Sélection de l'intervalle de temps pour la visualisation")

# Récupérer les valeurs uniques de la colonne 'Time'
time_values = selected_df["Time"].sort_values().unique()

# Sélection de l'intervalle de temps (début et fin)
start_time, end_time = st.select_slider(
    "Sélectionnez l'intervalle de temps:",
    options=time_values,
    value=(time_values[0], time_values[-1]),
)

# Filtrer les données en fonction de l'intervalle de temps
filtered_df = selected_df[
    (selected_df["Time"] >= start_time) & (selected_df["Time"] <= end_time)
]

# Afficher les données filtrées
st.write(f"Données filtrées entre {start_time} et {end_time}:")

### Visualisation des données Label ###
fig = go.Figure()
x_values = filtered_df["Time"]  # Utiliser les valeurs de la colonne 'Time' pour l'axe X
y_values = [1] * len(
    filtered_df
)  # Les y-values sont toutes égales ici, mais tu peux les ajuster
fig.add_trace(
    go.Scatter(
        x=x_values,
        y=y_values,
        mode="markers",
        marker=dict(
            color=filtered_df["Label"].map(
                label_color_map
            ),  # Appliquer les couleurs en fonction du label
            size=10,  # Taille des marqueurs
            symbol="square",  # Utiliser un symbole carré pour les marqueurs
        ),
        text=filtered_df["Label"],  # Afficher l'info des Labels en hover
    ),
)
fig.update_layout(
    height=200,
    width=1400,
    title_text=f"Visualisation des données - Labels en fonction du type d'attaque",
    template="simple_white",
    xaxis=dict(title="Temps", showgrid=True),  # Intitulé de l'axe X : "Temps"
    yaxis=dict(
        title="Valeurs",  # Intitulé de l'axe Y
        showgrid=False,
        showticklabels=False,  # Masquer les ticks (valeurs) de l'axe Y
    ),
)
st.plotly_chart(fig)

### Visualisation des données Valv ###
st.sidebar.subheader("Visualisation combinée des colonnes Valv")
valv_columns = [f"Valv_{i}" for i in range(1, 23)]
valv_df = filtered_df[["Time"] + valv_columns]
fig = px.line(
    valv_df,
    x="Time",
    y=valv_columns,
    title=f"Visualisation des colonnes Valv - Entre {start_time} et {end_time}",
)
fig.update_layout(
    height=300,
    width=1400,
    template="simple_white",
    xaxis=dict(title="Temps"),
    yaxis=dict(title="Valeurs"),
)
st.plotly_chart(fig)


### Visualisation des données Pump ###
st.sidebar.subheader("Visualisation combinée des colonnes Pump")
valv_columns = [f"Pump_{i}" for i in range(1, 7)]
valv_df = filtered_df[["Time"] + valv_columns]
fig = px.line(
    valv_df,
    x="Time",
    y=valv_columns,
    title=f"Visualisation des colonnes Valv - Entre {start_time} et {end_time}",
)
fig.update_layout(
    height=300,
    width=1400,
    template="simple_white",
    xaxis=dict(title="Temps"),
    yaxis=dict(title="Valeurs"),
)
st.plotly_chart(fig)

### Visualisation des données Tank ###
st.sidebar.subheader("Visualisation combinée des colonnes Tank")
valv_columns = [f"Tank_{i}" for i in range(1, 5)]
valv_df = filtered_df[["Time"] + valv_columns]
fig = px.line(
    valv_df,
    x="Time",
    y=valv_columns,
    title=f"Visualisation des colonnes Valv - Entre {start_time} et {end_time}",
)
fig.update_layout(
    height=300,
    width=1400,
    template="simple_white",
    xaxis=dict(title="Temps"),
    yaxis=dict(title="Valeurs"),
)
st.plotly_chart(fig)


### Visualisation des données Flow_sensor ###
st.sidebar.subheader("Visualisation combinée des colonnes Flow_sensor")
valv_columns = [f"Flow_sensor_{i}" for i in range(1, 5)]
valv_df = filtered_df[["Time"] + valv_columns]
fig = px.line(
    valv_df,
    x="Time",
    y=valv_columns,
    title=f"Visualisation des colonnes Valv - Entre {start_time} et {end_time}",
)
fig.update_layout(
    height=300,
    width=1400,
    template="simple_white",
    xaxis=dict(title="Temps"),
    yaxis=dict(title="Valeurs"),
)

st.plotly_chart(fig)
