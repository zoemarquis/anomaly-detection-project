from streamlit_config.streamlit_defaults import *
from streamlit_config.utils import *
from streamlit_config.article_data import *
import plotly.graph_objects as go

import matplotlib.pyplot as plt

st.title("Comparaison des modèles pour la détection d'attaques")

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
# if selec_dataset[dataset_choice] == "PHY":
#     model_names = model_names_phy
# else:
#     model_names = model_names_netw
# model_choice = st.selectbox("Sélectionnez le modèle :", list(model_names.keys()))

st.divider()

df_attack = df_results[(df_results["attack_type"] == attack_types[attack_choice])]
df_attack = df_attack[df_attack["data"] == selec_dataset[dataset_choice]]

# si labeln sélectionné ajouter les données de l'article
if attack_types[attack_choice] == "labeln":
    if dataset_choice == "données physiques":
        article_data = article_data_phy
    else:
        article_data = article_data_netw
    df_attack = pd.concat([df_attack, pd.DataFrame(article_data)], ignore_index=True)

# st.table(df_attack)

df_attack_without_article = df_attack[
    (df_attack["model_type"] != "KNN article")
    & (df_attack["model_type"] != "RF article")
    & (df_attack["model_type"] != "SVM article")
    & (df_attack["model_type"] != "NB article")
]




# df_selected = df_results[(df_results["filename"] == dataset_name)]
df_selected = df_attack[
    [
        "model_type",
        "precision",
        "recall",
        "tnr",
        "accuracy",
        "f1",
        "balanced_accuracy",
        "mcc",
    ]
]

df_selected = df_selected.rename(
    columns={
        "model_type": "Modèle",
        "precision": "Precision",
        "recall": "Rappel / TPR",
        "tnr": "TNR",
        "accuracy": "Accuracy",
        "f1": "F1 score",
        "balanced_accuracy": "Balanced Accuracy",
        "mcc": "Matthews Correlation Coefficient",
    }
)

df_selected = df_selected.set_index("Modèle")

styled_df = (
    df_selected.style.format(precision=3, na_rep="(pas de valeur)")
    .apply(
        lambda col: (
            [""] * len(col)  # Pas de style si toutes les valeurs sont identiques
            if col.nunique() <= 1
            else [
                "background-color: rgba(150, 212, 0, 0.5); color: white;"
                if v == col.max()
                else "background-color: rgba(41, 212, 157, 0.5); color: black;"
                if v == col.nlargest(2).iloc[-1]
                else "background-color: rgba(255, 70, 0, 0.5); color: black;"
                if v == col.nsmallest(2).iloc[-1]
                else "background-color: rgba(250, 24, 110, 0.5); color: black;"
                if v == col.min()
                else ""
                for v in col
            ]
        ),
        subset=df_selected.columns,
    )
    .set_table_styles(
        [
            {"selector": "td, th", "props": [("text-align", "left")]}
        ]  # Aligner à gauche tous les éléments (td et th)
    )
)


# Diviser l'espace en 2 colonnes
col1, col2 = st.columns(
    [8, 2]
)  # La première colonne (pour le tableau) occupe 2/3 de l'espace, la seconde (pour la légende) 1/3

with col1:
    # Affichage du tableau avec le style
    st.write("### Résultats pour l'attaque sélectionnée")
    st.table(styled_df)

with col2:
    # Ajouter une légende avec des carrés colorés
    # st.write("### Légende des couleurs")
    st.markdown(
        "<h5 style='font-size: 25px;'>Légende des couleurs</h5>", unsafe_allow_html=True
    )
    # margin vertical
    st.markdown(
        "<div style='margin-top: 10px; margin-bottom: 10px;'></div>",
        unsafe_allow_html=True,
    )

    # Création de l'affichage avec des carrés de couleur
    fig, ax = plt.subplots(
        figsize=(2, 5)
    )  # Taille de la légende plus haute pour mieux afficher tous les carrés
    # Ajouter les carrés et les textes, en ajustant les positions y pour éviter qu'ils ne se chevauchent
    ax.add_patch(plt.Rectangle((0, 0), 1, 1.5, color="#96D400"))  # Carré vert foncé
    ax.text(
        1.1,
        0.5,
        "Valeur maximale",
        verticalalignment="center",
        fontsize=20,
        color="white",
    )
    ax.add_patch(plt.Rectangle((0, -1.5), 1, 1, color="#29D49D"))  # Carré vert clair
    ax.text(
        1.1,
        -1,
        "Deuxième valeur la plus élevée",
        verticalalignment="center",
        fontsize=20,
        color="white",
    )
    ax.add_patch(plt.Rectangle((0, -3), 1, 1, color="#FF4600"))  # Carré orange
    ax.text(
        1.1,
        -2.5,
        "Deuxième valeur la plus basse",
        verticalalignment="center",
        fontsize=20,
        color="white",
    )
    ax.add_patch(plt.Rectangle((0, -4.5), 1, 1, color="#FA186E"))  # Carré rose
    ax.text(
        1.1,
        -4,
        "Valeur minimale",
        verticalalignment="center",
        fontsize=20,
        color="white",
    )

    # Retirer les axes
    ax.set_axis_off()

    # Ajuster les limites de l'axe pour s'assurer que tout soit visible
    ax.set_xlim(0, 1.5)
    ax.set_ylim(-5.5, 1)

    fig.patch.set_alpha(0.0)  # Rendre l'arrière-plan de la figure transparent
    ax.set_facecolor("none")  # Rendre l'arrière-plan des axes transparent

    # Afficher la légende dans streamlit
    st.pyplot(fig, transparent=True)

st.divider()

### Radar Chart ###
balanced_measures = ["model_type", "precision", "recall", "accuracy", "tnr"]
unbalanced_measures = ["model_type", "f1", "balanced_accuracy", "mcc"]

col1, col2 = st.columns(2)

with col1:
    df_radar_balanced = df_attack[balanced_measures]

    fig_radar_balanced = go.Figure()

    for model in df_radar_balanced["model_type"]:
        model_data = df_radar_balanced[df_radar_balanced["model_type"] == model]
        fig_radar_balanced.add_trace(
            go.Scatterpolar(
                r=model_data.iloc[0, 1:].values,
                theta=df_radar_balanced.columns[1:],
                fill="toself",
                name=model,
                line_color=default_colors[colors_model_names.get(model, "blue")],
                showlegend=True,
            )
        )

    fig_radar_balanced.update_layout(
        title="Radar Chart des métriques équilibrées pour chaque modèle",
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1]),
        ),
        showlegend=True,
        autosize=True,
    )

    fig_radar_balanced.update_layout(width=800, height=600)
    st.plotly_chart(fig_radar_balanced, use_container_width=True)

with col2:
    df_radar_unbalanced = df_attack[unbalanced_measures]

    fig_radar_unbalanced = go.Figure()

    for model in df_radar_unbalanced["model_type"]:
        model_data = df_radar_unbalanced[df_radar_unbalanced["model_type"] == model]
        fig_radar_unbalanced.add_trace(
            go.Scatterpolar(
                r=model_data.iloc[0, 1:].values,
                theta=df_radar_unbalanced.columns[1:],
                fill="toself",
                name=model,
                line_color=default_colors[colors_model_names.get(model, "blue")],
                showlegend=True,
            )
        )

    fig_radar_unbalanced.update_layout(
        title="Radar Chart des métriques déséquilibrées pour chaque modèle",
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1]),
        ),
        showlegend=True,
        autosize=True,
    )

    fig_radar_unbalanced.update_layout(width=800, height=600)
    st.plotly_chart(fig_radar_unbalanced, use_container_width=True)

st.divider()

## Précision-Rappel, TPR-TNR, TPR-FPR ##

fig_precision_recall = go.Figure()
fig_precision_recall.add_trace(
    go.Scatter(
        x=[1, 1],
        y=[0, 1],
        mode="lines",
        line=dict(color="white", dash="dot"),
        showlegend=False,
    )
)
fig_precision_recall.add_trace(
    go.Scatter(
        x=[0, 1],
        y=[1, 1],
        mode="lines",
        line=dict(color="white", dash="dot"),
        showlegend=False,
    )
)
for model in df_attack["model_type"].unique():
    subset = df_attack[df_attack["model_type"] == model]
    precision = subset["precision"].values[0]
    recall = subset["recall"].values[0]
    color = default_colors[colors_model_names.get(model, "blue")]
    fig_precision_recall.add_trace(
        go.Scatter(
            x=[recall],
            y=[precision],
            mode="markers",
            name=model,
            text=[model],
            textposition="top center",
            marker=dict(color=color, size=10),
        )
    )
fig_precision_recall.update_layout(
    title="Comparaison Précision-Rappel pour chaque modèle",
    xaxis_title="Recall",
    yaxis_title="Precision",
    xaxis=dict(range=[0, 1.1]),
    yaxis=dict(range=[0, 1.1]),
    showlegend=True,
    template="plotly_white",
)

fig_tpr_tnr = go.Figure()
fig_tpr_tnr.add_trace(
    go.Scatter(
        x=[1, 1],
        y=[0, 1],
        mode="lines",
        line=dict(color="white", dash="dot"),
        showlegend=False,
    )
)
fig_tpr_tnr.add_trace(
    go.Scatter(
        x=[0, 1],
        y=[1, 1],
        mode="lines",
        line=dict(color="white", dash="dot"),
        showlegend=False,
    )
)
for model in df_attack_without_article["model_type"].unique():
    subset = df_attack[df_attack["model_type"] == model]
    tpr = subset["recall"].values[0]
    tnr = subset["tnr"].values[0]
    color = default_colors[colors_model_names.get(model, "blue")]
    fig_tpr_tnr.add_trace(
        go.Scatter(
            x=[tnr],
            y=[tpr],
            mode="markers",
            name=model,
            text=[model],
            textposition="top center",
            marker=dict(color=color, size=10),
        )
    )
fig_tpr_tnr.update_layout(
    title="Comparaison TPR vs TNR pour chaque modèle",
    xaxis_title="True Negative Rate",
    yaxis_title="True Positive Rate",
    xaxis=dict(range=[0, 1.1]),
    yaxis=dict(range=[0, 1.1]),
    showlegend=True,
    template="plotly_white",
)

fig_tpr_fpr = go.Figure()
fig_tpr_fpr.add_trace(
    go.Scatter(
        x=[1, 1],
        y=[0, 1],
        mode="lines",
        line=dict(color="white", dash="dot"),
        showlegend=False,
    )
)
fig_tpr_fpr.add_trace(
    go.Scatter(
        x=[0, 1],
        y=[1, 1],
        mode="lines",
        line=dict(color="white", dash="dot"),
        showlegend=False,
    )
)
for model in df_attack_without_article["model_type"].unique():
    subset = df_attack[df_attack["model_type"] == model]
    tpr = subset["recall"].values[0]
    fpr = subset["fpr"].values[0]
    color = default_colors[colors_model_names.get(model, "blue")]
    fig_tpr_fpr.add_trace(
        go.Scatter(
            x=[fpr],
            y=[tpr],
            mode="markers",
            name=model,
            text=[model],
            textposition="top center",
            marker=dict(color=color, size=10),
        )
    )
fig_tpr_fpr.update_layout(
    title="Comparaison TPR vs FPR pour chaque modèle",
    xaxis_title="False Positive Rate",
    yaxis_title="True Positive Rate",
    xaxis=dict(range=[0, 1.1]),
    yaxis=dict(range=[0, 1.1]),
    showlegend=True,
    template="plotly_white",
)

# Créer des colonnes dans Streamlit
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(fig_precision_recall)
with col2:
    st.plotly_chart(fig_tpr_tnr)
with col3:
    st.plotly_chart(fig_tpr_fpr)
