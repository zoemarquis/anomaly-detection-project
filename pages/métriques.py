import streamlit as st
import json

# Charger les métriques du fichier JSON
with open("model_metrics.json", "r") as f:
    results = json.load(f)

# Afficher les métriques de chaque modèle
for model_name, metrics in results.items():
    st.header(f"Évaluation du modèle: {model_name}")
    st.write("Précision:", metrics['precision'])
    st.write("Rappel:", metrics['recall'])
    st.write("Exactitude:", metrics['accuracy'])
    st.write("F1-Score:", metrics['f1_score'])
    st.write("Balanced Accuracy:", metrics['balanced_accuracy'])
    st.write("Matthews Corr. Coef.:", metrics['mcc'])
    st.write("Matrice de Confusion:", metrics['confusion_matrix'])
