import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Projet Protection Dashboard",
    page_icon="🛡️",
    layout="wide",
)

# Titre principal
st.title("🛡️ Projet Protection des données")
st.markdown(
    """
    Bienvenue dans le tableau de bord du projet **Protection des données**.
    Ce projet vise à analyser et visualiser des données issues de simulations de réseaux et de systèmes physiques, 
    avec pour objectif d'étudier les performances des modèles de détection des attaques.
    """
)

# Sous-titre
st.header("🔍 Aperçu du projet")

# Contenu de la section Aperçu
st.markdown(
    """
L'objectif de ce projet est d'appliquer une chaîne d'analyse de données sur un jeu de données cyber-physique. L'analyse se divise en deux volets :  
1. Utilisation des **données réseau** uniquement.  
2. Utilisation des **données physiques** uniquement.  

Nous comparons les performances de plusieurs algorithmes de machine learning, parmi lesquels :  
- **K-Nearest Neighbors (KNN)**  
- **CART (Classification and Regression Trees)**  
- **Random Forest**  
- **XGBoost**  
- **Multi-Layer Perceptron (MLP)**  
"""
)

# Section Guide d'utilisation
st.header("📖 Guide d'utilisation")
st.markdown(
    """
    1. **Sélectionnez un jeu de données et un type d'attaque :**  
       Utilisez les menus déroulants pour choisir le dataset et l'attaque à analyser.
    2. **Explorez les graphiques :**  
       Visualisez les temps d'entraînement et de prédiction, ainsi que la mémoire consommée.  
    3. **Comparez les modèles :**  
       Analysez les différences de performances entre les modèles entraînés.
    """
)

# Divider pour une meilleure séparation visuelle
st.divider()

# Ajout d'une note sur l'équipe et les contributeurs
st.sidebar.title("💡 À propos")
st.sidebar.markdown(
    """
    **Contributeurs :**  
    - Zoé Marquis  
    - Charlotte Kruzic
    - Daniil Kudriashov
    - Ekaterina Zaitceva
    """
)


st.sidebar.divider()

# Ajout d'un lien vers l'énoncé ou la documentation
st.sidebar.title("📂 Ressources")
st.sidebar.markdown(
    """
    - [Énoncé du projet](enonce.pdf)  
    - [Rapport final](rapport.pdf)  
    - [Code source](https://github.com/zoemarquis/projet_protection)
    """
)

# Section des points d'analyse
st.subheader("📊 Points d'analyse principaux")

st.markdown(
    """
- **Évaluation des performances des modèles** :  
  - Mesures pour données équilibrées : *précision, rappel, TPR (True Positive Rate), TNR (True Negative Rate), accuracy*.  
  - Mesures pour données déséquilibrées : *F1-score, balanced accuracy, coefficient de corrélation de Matthews (MCC)*.  
  - Analyse des matrices de confusion pour chaque algorithme et chaque classe d'attaque.  

- **Évaluation des ressources consommées** :  
  - Temps d'entraînement (fit time).  
  - Temps de prédiction (predict time).  
  - Mémoire utilisée (RAM).  

- **Comparaison avec les performances publiées** dans l'article scientifique associé au dataset.  
"""
)
