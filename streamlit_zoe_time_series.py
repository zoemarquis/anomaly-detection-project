from streamlit_defaults import *
import numpy as np

from plotly.subplots import make_subplots


# je veux une visualisation d'une série temporelle avec la couleur qui change en fonction du label : un barcode chart

df_phy_1["Time"] = pd.to_datetime(df_phy_1["Time"])
df_phy_2["Time"] = pd.to_datetime(df_phy_2["Time"])
df_phy_3["Time"] = pd.to_datetime(df_phy_3["Time"])
df_phy_4["Time"] = pd.to_datetime(df_phy_4["Time"])
df_phy_norm["Time"] = pd.to_datetime(df_phy_norm["Time"])

# ---------------------------------------------------------------------
# Créer le Barcode Chart
fig = px.scatter(
    df_phy_1,
    x="Time",
    y="Label",
    color="Label",
    color_discrete_map=label_color_map,
    symbol="Label",
    title="Distribution des événements dans le temps",
    labels={"Time": "Date"},
    size=[1] * len(df_phy_1),
    opacity=0.8,
    template="simple_white",
    height=400,
)

st.plotly_chart(fig)


# ---------------------------------------------------------------------

# bump chart sur att_phy_1

# Création de l'application Streamlit
st.title("Bump Chart des Labels pour df_phy_1")

# Création du bump chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_phy_1['Time'],
    y=df_phy_1['Label'],
    mode='lines+markers',
))

# Mise à jour de la mise en page
fig.update_layout(title="Bump Chart des Labels au Fil du Temps",
                  xaxis_title="Time",
                  yaxis_title="Label",
                  )

fig.update_yaxes(categoryorder='array', categoryarray=all_labels)

# Affichage du graphique dans Streamlit
st.plotly_chart(fig)

# ---------------------------------------------------------------------

st.title("Barcode Chart pour 5 Séries Temporelles")

datasets = {
    "phy_att_1": df_phy_1,
    "phy_att_2": df_phy_2,
    "phy_att_3": df_phy_3,
    "phy_att_4": df_phy_4,
    "phy_norm": df_phy_norm,
}

max_len = max(len(df) for df in datasets.values())

fig = make_subplots(
    rows=5,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.05,
)

# Ajout de chaque dataset en tant que scatter plot, étiré sur la largeur maximale
for i, (key, df) in enumerate(datasets.items(), start=1):
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
    title_text="Barcode Chart Aligné pour 5 Séries Temporelles",
    template="simple_white"
)


# Afficher les ticks de l'axe x seulement pour le dernier sous-graphe
fig.update_xaxes(title_text="Time", showticklabels=True, row=5, col=1)


# Mise à jour de l'axe y pour chaque sous-graphe pour afficher le nom du dataset
for i, key in enumerate(datasets.keys(), start=1):
    fig.update_yaxes(title_text=key, row=i, col=1, showticklabels=False) #, orientation="horizontal")



st.plotly_chart(fig)



# TODO : légende


# ---------------------------------------------------------------------

fig = px.scatter(
    df_phy_1,
    x="Time",
    y="Label",
    color="Label",
    color_discrete_map=label_color_map,
    # symbol="Label",
    title="Distribution des événements dans le temps",
    labels={"Time": "Time"},
    opacity=0.8,
    # template="simple_white",
    height=400,
    marginal_x= "rug", # vraiment pas mal !
)

st.plotly_chart(fig)



# ---------------------------------------------------------------------

# Création de l'application Streamlit
st.title("Bump Chart des Labels pour les séries temporelles alignées à Temps 0")


datasets = {
    "phy_att_1": (df_phy_1, 'purple'),
    "phy_att_2": (df_phy_2, 'blue_green'),
    "phy_att_3": (df_phy_3, 'yellow'),
    "phy_att_4": (df_phy_4, 'pink'),
}

# Création de la figure
fig = go.Figure()

# Ajout de chaque dataset au graphique avec temps normalisé
for name, (df, color) in datasets.items():
    df = df.copy()  # Créer une copie pour éviter de modifier l'original
    df['Time'] = (df['Time'] - df['Time'].min()).dt.total_seconds() / (60*60*24)  # Normaliser à temps 0 (en jours)

    fig.add_trace(go.Scatter(
        x=df['Time'],
        y=df['Label'],
        mode='lines+markers',
        name=name,
        marker=dict(color=default_colors[color], size=2),  # Taille réduite pour rendre les points très discrets
        line=dict(color=default_colors[color], width=1),   # Épaisseur de ligne fine
    ))

# Mise à jour de la mise en page
fig.update_layout(
    title="Bump Chart des Labels Aligné à Temps 0",
    xaxis_title="Temps (jours depuis le début de chaque série)",
    yaxis_title="Label",
)

# Ordre des catégories pour l'axe y
fig.update_yaxes(categoryorder='array', categoryarray=all_labels)

# Affichage du graphique dans Streamlit
st.plotly_chart(fig)