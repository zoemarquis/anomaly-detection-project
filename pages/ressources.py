import streamlit as st


# [PHY_ ou NETW_] + [models_phy] + [one_attack]
# sélection de données physique ou network
# sélection du modèle
# sélection de quelle attaque

model_names_phy = ['cnn1d', ]
model_names_netw = []
one_attack = ['label_n', 'label_DoS', 'label_MITM', 'label_physical_fault', 'label_scan']


# Interface utilisateur
st.title("Sélection des données et des attaques")

# Sélectionner le type de données (physiques ou réseau)
data_type = st.radio("Choisissez le type de données", ('Physique', 'Réseau'))

# Sélectionner le modèle en fonction du type de données choisi
if data_type == 'Physique':
    model_choice = st.selectbox("Sélectionnez le modèle", model_names_phy)
elif data_type == 'Réseau':
    model_choice = st.selectbox("Sélectionnez le modèle", model_names_netw)

# Sélectionner l'attaque
attack_choice = st.selectbox("Sélectionnez l'attaque", one_attack)

# Afficher les choix de l'utilisateur
st.write(f"Type de données choisi : {data_type}")
st.write(f"Modèle choisi : {model_choice}")
st.write(f"Attaque choisie : {attack_choice}")

# Créer le nom du fichier selon la sélection
if data_type == 'Physique':
    dataset_prefix = 'PHY_'
elif data_type == 'Réseau':
    dataset_prefix = 'NETW_'

# Générer le nom final du dataset
dataset_name = f"{dataset_prefix}{model_choice}_{attack_choice}"

# Afficher le nom du dataset généré
st.write(f"Nom du dataset généré : {dataset_name}")



Temps d’entraînement (fit time) et temps de prédiction (prediction time) sous forme de graphiques.
Utilisation de la mémoire RAM pour chaque modèle, illustrée par des diagrammes ou des barres pour une comparaison rapide.

Comparaison entre les modèles : Tableau comparatif montrant les différences de consommation de ressources pour chaque algorithme.


# 
graphisque de lignes pour le temps et la mémoire 