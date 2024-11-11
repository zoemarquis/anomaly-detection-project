from streamlit_config.streamlit_defaults import *

# # TODO : 1 avant nettoyer
#
# Expliquer les étapes de nettoyage (si disponibles) et inclure des résumés de ce qui a changé après chaque étape.
#
# # TODO : 2 après nettoyer
#
# Histogrammes, distributions, diagrammes de dispersion pour les principales caractéristiques.
#
# Représentation des valeurs manquantes (si applicable), pour identifier les éventuelles lacunes dans les données brutes.
#
# Distribution des classes de sortie, pour visualiser le déséquilibre des classes.


st.title("Données physiques")
st.success("Avant nettoyage")
st.sidebar.header("Avant nettoyage")

st.sidebar.subheader("Répartition des labels par dataset")

datasets = [
    ("Attack 1", df_phy_1),
    ("Attack 2", df_phy_2),
    ("Attack 3", df_phy_3),
    ("Attack 4", df_phy_4),
    ("Normal", df_phy_norm),
]

data = []
unique_labels = set()
for name, df in dict_dfs.items():
    label_counts = df["Label"].value_counts()
    unique_labels.update(label_counts.index)
    for label, count in label_counts.items():
        data.append({"Dataset": name, "Label": label, "Count": count})
data_df = pd.DataFrame(data)
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


st.sidebar.header("Après nettoyage")

st.sidebar.subheader("Répartition des labels par dataset")


# sélection du dataset et regarder distribution de colonnes sélec tionnées au cours du temps
