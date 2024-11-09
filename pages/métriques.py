from streamlit_config.streamlit_defaults import *
from streamlit_config.utils import *    
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.title("Comparaison des modèles pour la détection d'attaques")

dataset_choice = st.selectbox("Sélectionnez le type de données :", list(selec_dataset.keys()))
attack_choice = st.selectbox("Sélectionnez le type d'attaque :", list(attack_types.keys()))
if selec_dataset[dataset_choice] == "PHY":
    model_names = model_names_phy
else:
    model_names = model_names_netw
model_choice = st.selectbox("Sélectionnez le modèle :", list(model_names.keys()))

st.write("**Type de données sélectionné :**", dataset_choice)
st.write("**Type d'attaque sélectionné :**", attack_choice)
st.write("**Modèle sélectionné :**", model_choice)

dataset_name = f"{selec_dataset[dataset_choice]}_results_{model_names[model_choice]}_{attack_types[attack_choice]}"
st.write(f"Nom du dataset généré : {dataset_name}")

# afficher chaque valeur de chaque métrique pour le modèle et l'attaque sélectionnés
# TODO : afficher ça "pretty"
df_selected = df_results[(df_results["filename"] == dataset_name)]
st.table(df_selected)

df_attack = df_results[(df_results["attack_type"] == attack_types[attack_choice])]

# TODO : associer une couleur à un modèle et afficher la légende
# default_colors -> créer map pour couleur

### Radar Chart ###
balanced_measures = ['model_type', 'precision', 'recall', 'tnr','accuracy']
unbalanced_measures = ['model_type', 'f1', 'balanced_accuracy', 'mcc']

col1, col2 = st.columns(2)

with col1:
    df_radar_balanced = df_attack[balanced_measures]

    fig_radar_balanced = go.Figure()

    for model in df_radar_balanced['model_type']:
        model_data = df_radar_balanced[df_radar_balanced['model_type'] == model]
        fig_radar_balanced.add_trace(go.Scatterpolar(
            r=model_data.iloc[0, 1:].values,
            theta=df_radar_balanced.columns[1:],
            fill='toself',
            name=model,
            line_color=default_colors[colors_model_names.get(model, 'blue')],  # Utiliser la couleur du modèle
            showlegend=True
        ))
    
    fig_radar_balanced.update_layout(
        title="Radar Chart des métriques équilibrées pour chaque modèle",
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1]),
        ),
        showlegend=True,
        autosize=True
    )
    
    fig_radar_balanced.update_layout(width=800, height=600)
    st.plotly_chart(fig_radar_balanced, use_container_width=True)

with col2:
    df_radar_unbalanced = df_attack[unbalanced_measures]
    
    fig_radar_unbalanced = go.Figure()

    for model in df_radar_unbalanced['model_type']:
        model_data = df_radar_unbalanced[df_radar_unbalanced['model_type'] == model]
        fig_radar_unbalanced.add_trace(go.Scatterpolar(
            r=model_data.iloc[0, 1:].values,
            theta=df_radar_unbalanced.columns[1:],
            fill='toself',
            name=model,
            line_color=default_colors[colors_model_names.get(model, 'blue')],  # Utiliser la couleur du modèle
            showlegend=True
        ))

    fig_radar_unbalanced.update_layout(
        title="Radar Chart des métriques déséquilibrées pour chaque modèle",
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1]),
        ),
        showlegend=True,
        autosize=True
    )
    
    fig_radar_unbalanced.update_layout(width=800, height=600)
    st.plotly_chart(fig_radar_unbalanced, use_container_width=True)

# ### Précision-Rappel Plot ###
# # Tracer la Précision et le Rappel pour chaque modèle sélectionné
# fig, ax = plt.subplots()
# for model in model_names.keys():
#     subset = df_attack[df_attack['model_type'] == model]
#     precision = subset['precision']
#     recall = subset['recall']
#     ax.scatter(recall, precision, label=model)
#     ax.annotate(model, (recall, precision), textcoords="offset points", xytext=(5,5), ha='center')
# 
# # Configurer les axes et le titre
# ax.set_xlabel("Recall")
# ax.set_ylabel("Precision")
# ax.set_title(f"Comparaison Précision-Rappel pour l'attaque {attack_types[attack_choice]}")
# ax.legend()
# st.pyplot(fig)

# TODO : matrice de confusion pour chaque attaque.
# TODO : Comparaison avec les résultats publiés : Tableau comparatif des performances de chaque modèle par rapport aux résultats du papier associé.

## Matrices de confusion ##

# # Visualisation des matrices de confusion pour chaque modèle et attaque
# vérif bon ordre et meme ordre partout 
# pourattaque sélectionnée : autre coouleur 
