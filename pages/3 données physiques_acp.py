import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pickleshare import PickleShareDB
import os

# Chargement des données
data_dir = "prep_data"
db = PickleShareDB(os.path.join(data_dir, "kity"))

# Récupérer les résultats PCA
pca_results = db['pca_results_phy']

# Configuration de la page
st.set_page_config(page_title="Analyse en Composantes Principales", layout="wide")

# Titre principal
st.title("🔍 Analyse en Composantes Principales des Données Physiques")

# Introduction explicative
st.markdown("""
Cette page présente les résultats de l'Analyse en Composantes Principales (ACP) appliquée aux données physiques.
L'ACP permet de réduire la dimensionnalité des données tout en conservant l'information pertinente et 
de visualiser les relations entre les différentes caractéristiques.
""")

# Division en colonnes pour la variance expliquée
col1, col2 = st.columns(2)

with col1:
    st.subheader("Variance expliquée par composante")
    
    # Graphique de la variance expliquée
    fig_variance = go.Figure()
    
    # Graphique en barres pour la variance individuelle
    fig_variance.add_trace(
        go.Bar(
            x=pca_results['explained_variance']['Component'],
            y=pca_results['explained_variance']['Explained_Variance'],
            name='Individuelle',
            text=pca_results['explained_variance']['Explained_Variance'].round(3),
            textposition='auto',
        )
    )
    
    # Courbe pour la variance cumulée
    fig_variance.add_trace(
        go.Scatter(
            x=pca_results['explained_variance']['Component'],
            y=pca_results['explained_variance']['Cumulative_Variance'],
            name='Cumulée',
            line=dict(color='red'),
            mode='lines+markers'
        )
    )
    
    fig_variance.update_layout(
        title='Ratio de variance expliquée par composante principale',
        xaxis_title='Composante Principale',
        yaxis_title='Ratio de variance expliquée',
        showlegend=True
    )
    
    st.plotly_chart(fig_variance, use_container_width=True)

with col2:
    st.subheader("Matrice des composantes")
    
    # Heatmap des composantes
    fig_components = px.imshow(
        pca_results['components_matrix'],
        title='Matrice des composantes principales',
        aspect='auto',
        color_continuous_scale='RdBu'
    )
    
    st.plotly_chart(fig_components, use_container_width=True)

# Visualisations interactives
st.header("Visualisations des données projetées")

# Sélection du type de visualisation
viz_type = st.radio(
    "Choisissez le type de visualisation :",
    ["Classification par type d'attaque", "Classification binaire (Normal vs Attaque)"]
)

# Colonne pour les options de visualisation
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Options")
    dim_viz = st.radio(
        "Dimensions :",
        ["2D", "3D"]
    )

with col2:
    if viz_type == "Classification par type d'attaque":
        if dim_viz == "2D":
            fig = px.scatter(
                pca_results['transformed_data'],
                x='PC1',
                y='PC2',
                color='Label',
                title='Projection ACP - Deux premières composantes',
                hover_data=['source']
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = px.scatter_3d(
                pca_results['transformed_data'],
                x='PC1',
                y='PC2',
                z='PC3',
                color='Label',
                title='Projection ACP - Trois premières composantes',
                hover_data=['source']
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        if dim_viz == "2D":
            fig = px.scatter(
                pca_results['transformed_data'],
                x='PC1',
                y='PC2',
                color='Label_n',
                title='Projection ACP - Classification binaire',
                hover_data=['source'],
                color_discrete_map={True: 'red', False: 'blue'},
                labels={'Label_n': 'Attaque'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = px.scatter_3d(
                pca_results['transformed_data'],
                x='PC1',
                y='PC2',
                z='PC3',
                color='Label_n',
                title='Projection ACP - Classification binaire',
                hover_data=['source'],
                color_discrete_map={True: 'red', False: 'blue'},
                labels={'Label_n': 'Attaque'}
            )
            st.plotly_chart(fig, use_container_width=True)

# Analyse des caractéristiques principales
st.header("Analyse des caractéristiques principales")

# Sélection de la composante à analyser
selected_pc = st.selectbox(
    "Sélectionnez une composante principale :",
    [f"PC{i+1}" for i in range(len(pca_results['components_matrix']))]
)

pc_index = int(selected_pc[2]) - 1
feature_importance = pd.DataFrame({
    'Feature': pca_results['feature_names'],
    'Importance': np.abs(pca_results['pca_model'].components_[pc_index])
}).sort_values('Importance', ascending=False)

# Affichage des caractéristiques les plus importantes
fig_features = px.bar(
    feature_importance.head(10),
    x='Feature',
    y='Importance',
    title=f'Top 10 des caractéristiques contribuant à {selected_pc}'
)
st.plotly_chart(fig_features, use_container_width=True)

# Informations supplémentaires
st.sidebar.header("ℹ️ Informations")
st.sidebar.markdown("""
### À propos de l'ACP
L'Analyse en Composantes Principales est une technique de réduction de dimensionnalité qui :
- Trouve les directions de variance maximale dans les données
- Crée de nouvelles caractéristiques non corrélées
- Permet de visualiser les données en 2D ou 3D

### Interprétation
- Les points proches dans la visualisation ont des caractéristiques similaires
- La séparation des points par couleur indique la qualité de la discrimination entre les classes
- Les composantes principales sont ordonnées par importance décroissante
""")