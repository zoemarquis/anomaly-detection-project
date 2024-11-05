from streamlit_config.streamlit_defaults import *


# --- Visualisation ---

# -----------------------------------------------------------------------------------------
# Bar chart : nb labels per dataset

st.title("Physical dataset")
st.header("Number of labels per dataset")


# Créer une liste de tous les DataFrames et noms pour les identifier
datasets = [
    ("Attack 1", df_phy_1),
    ("Attack 2", df_phy_2),
    ("Attack 3", df_phy_3),
    ("Attack 4", df_phy_4),
    ("Normal", df_phy_norm),
]

# Préparation des données pour l'histogramme empilé
data = []
unique_labels = set()

# Extraction des informations de chaque dataset
for name, df in datasets:
    label_counts = df["Label"].value_counts()
    unique_labels.update(label_counts.index)  # Recueillir tous les labels uniques
    for label, count in label_counts.items():
        data.append({"Dataset": name, "Label": label, "Count": count})

# Convertir en DataFrame et associer des couleurs aux labels uniques
data_df = pd.DataFrame(data)

# Créer l'histogramme empilé
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
