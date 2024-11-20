from streamlit_config.streamlit_defaults import *
from streamlit_config.utils import *
import plotly.graph_objects as go
import plotly.subplots as sp

st.title(
    "Évaluation de la consommation de ressources pour l'apprentissage et la détection"
)

dataset_choice = st.sidebar.selectbox(
    "Sélectionnez le type de données :", list(selec_dataset.keys())
)

if selec_dataset[dataset_choice] == "PHY":
    attack_types = attack_types_phy
else:
    attack_types = attack_types_net

attack_choice = st.sidebar.selectbox(
    "Sélectionnez le type d'attaque :", list(attack_types.keys())
)

df_attack = df_results[(df_results["data"] == selec_dataset[dataset_choice] )]
df_attack = df_attack[(df_results["attack_type"] == attack_types[attack_choice])]

time_measures = df_attack[["model_type", "fit_time", "predict_time"]]
memory_measures = df_attack[["model_type", "fit_memory_usage", "predict_memory_usage"]]

# Créer une figure avec deux sous-graphiques (1 ligne, 2 colonnes) sans partager l'axe Y
fig = sp.make_subplots(
    rows=2,
    cols=2,
    subplot_titles=[
        "Temps d'Entraînement",
        "Temps de Prédiction",
        "Mémoire pour l'Entraînement",
        "Mémoire pour la Prédiction",
    ],
    shared_yaxes=False,  # Désactiver le partage de l'axe Y pour des échelles différentes
    vertical_spacing=0.15,  # Augmenter l'espacement entre les sous-graphiques
)

# temps d'entraînement
for i, row in time_measures.iterrows():
    fig.add_trace(
        go.Bar(
            y=[row["model_type"]],  # Chaque modèle est sur l'axe Y
            x=[row["fit_time"]],
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

# temps de prédiction
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

# Mémoire pour l'entraînement
for i, row in memory_measures.iterrows():
    fig.add_trace(
        go.Bar(
            y=[row["model_type"]],
            x=[row["fit_memory_usage"]],
            name=f"Mémoire pour l'Entraînement ({row['model_type']}) en Mo",
            orientation="h",
            marker=dict(
                color=default_colors[colors_model_names.get(row["model_type"], "green")]
            ),
            width=0.8,
        ),
        row=2,
        col=1,
    )

# Mémoire pour la prédiction
for i, row in memory_measures.iterrows():
    fig.add_trace(
        go.Bar(
            y=[row["model_type"]],
            x=[row["predict_memory_usage"]],
            name=f"Mémoire pour la Prédiction ({row['model_type']} en Mo)",
            orientation="h",
            marker=dict(
                color=default_colors[
                    colors_model_names.get(row["model_type"], "orange")
                ]
            ),
            width=0.8,
        ),
        row=2,
        col=2,
    )

# Configurer le titre et l'affichage des axes pour les temps
fig.update_layout(
    title="Comparaison des Temps d'Entraînement et de Prédiction",
    # xaxis_title="Temps (secondes)",
    # yaxis_title="Modèles",
    template="plotly_white",
    bargap=0.1,  # Laisser un espace entre les barres pour plus de clarté
    showlegend=False,
)

fig.update_layout(
    title="Évaluation des temps et ressources (apprentissage et détection)",
    template="plotly_white",
    bargap=0.1,  # Laisser un espace entre les barres pour plus de clarté
    showlegend=False,
    height=800,  # Ajustez la hauteur (plus grand pour mieux visualiser)
)

# Limiter l'axe X de 0 à 60 pour les deux sous-graphiques
fig.update_xaxes(range=[0, 60], row=1, col=1)  # Temps d'Entraînement
fig.update_xaxes(range=[0, 2], row=1, col=2)  # Temps de Prédiction
fig.update_xaxes(range=[0, 60], row=2, col=1)  # Mémoire pour l'Entraînement (en Mo)
fig.update_xaxes(range=[0, 60], row=2, col=2)  # Mémoire pour la Prédiction (en Mo)


# Afficher le graphique dans Streamlit
st.plotly_chart(fig)

st.divider()
