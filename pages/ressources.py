from streamlit_config.streamlit_defaults import *
from streamlit_config.utils import *
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go


st.sidebar.title("TODO")

# TODO : pourquoi valeur négative pour memory ??
# TODO : problème pour valeurs des modèles de label
# TODO : mémoire

# Utilisation de la mémoire RAM pour chaque modèle, illustrée par des diagrammes ou des barres pour une comparaison rapide.


st.title("TODO")

dataset_choice = st.selectbox(
    "Sélectionnez le type de données :", list(selec_dataset.keys())
)
attack_choice = st.selectbox(
    "Sélectionnez le type d'attaque :", list(attack_types.keys())
)
if selec_dataset[dataset_choice] == "PHY":
    model_names = model_names_phy
else:
    model_names = model_names_netw
model_choice = st.selectbox("Sélectionnez le modèle :", list(model_names.keys()))

st.divider()

dataset_name = f"{selec_dataset[dataset_choice]}_results_{model_names[model_choice]}_{attack_types[attack_choice]}"
st.write(f"Nom du dataset généré : {dataset_name}")

# afficher chaque valeur de chaque métrique pour le modèle et l'attaque sélectionnés
# TODO : afficher ça "pretty"
df_selected = df_results[(df_results["filename"] == dataset_name)]
st.table(df_selected)

df_attack = df_results[(df_results["attack_type"] == attack_types[attack_choice])]

st.divider()

time_measures = df_attack[["model_type", "fit_time", "predict_time"]]
memory_measures = df_attack[["model_type", "fit_memory_usage", "predict_memory_usage"]]

# Créer une figure avec deux sous-graphiques (1 ligne, 2 colonnes) sans partager l'axe Y
fig = sp.make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["Temps d'Entraînement", "Temps de Prédiction"],
    shared_yaxes=False,  # Désactiver le partage de l'axe Y pour des échelles différentes
)

# Ajouter les barres horizontales pour le temps d'entraînement dans le premier sous-graphe
for i, row in time_measures.iterrows():
    fig.add_trace(
        go.Bar(
            y=[row["model_type"]],  # Chaque modèle est sur l'axe Y
            x=[
                row["fit_time"]
            ],  # Chaque barre a une longueur qui est la valeur du temps d'entraînement
            name=f"Temps d'Entraînement ({row['model_type']})",
            orientation="h",  # Spécifier que les barres sont horizontales
            marker=dict(
                color=default_colors[colors_model_names.get(row["model_type"], "blue")]
            ),
            width=0.8,  # Ajuster la largeur des barres
        ),
        row=1,
        col=1,
    )

# Ajouter les barres horizontales pour le temps de prédiction dans le second sous-graphe
for i, row in time_measures.iterrows():
    fig.add_trace(
        go.Bar(
            y=[row["model_type"]],  # Chaque modèle est sur l'axe Y
            x=[
                row["predict_time"]
            ],  # Chaque barre a une longueur qui est la valeur du temps de prédiction
            name=f"Temps de Prédiction ({row['model_type']})",
            orientation="h",  # Spécifier que les barres sont horizontales
            marker=dict(
                color=default_colors[colors_model_names.get(row["model_type"], "blue")]
            ),
            width=0.8,  # Ajuster la largeur des barres
        ),
        row=1,
        col=2,
    )

# Configurer le titre et l'affichage des axes pour les temps
fig.update_layout(
    title="Comparaison des Temps d'Entraînement et de Prédiction",
    xaxis_title="Temps (secondes)",
    yaxis_title="Modèles",
    template="plotly_white",
    bargap=0.1,  # Laisser un espace entre les barres pour plus de clarté
    showlegend=False,
)

# Limiter l'axe X de 0 à 60 pour les deux sous-graphiques
fig.update_xaxes(range=[0, 60], row=1, col=1)  # Temps d'Entraînement
fig.update_xaxes(range=[0, 10], row=1, col=2)  # Temps de Prédiction

# Afficher le graphique dans Streamlit
st.plotly_chart(fig)

st.divider()
