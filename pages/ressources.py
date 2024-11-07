import streamlit as st
import json

# Charger les résultats
with open("model_resource_metrics.json", "r") as f:
    all_results = json.load(f)

# Afficher les métriques et les ressources pour chaque modèle
for model_name, result in all_results.items():
    st.header(f"Modèle : {model_name}")
    st.subheader("Temps et mémoire")
    st.write("Temps d'entraînement (fit):", result['fit_time'], "secondes")
    st.write("Utilisation mémoire pour fit:", result['fit_memory_usage_MB'], "MB")
    st.write("Temps de prédiction:", result['predict_time'], "secondes")
    st.write("Utilisation mémoire pour prédiction:", result['predict_memory_usage_MB'], "MB")
    
    st.subheader("Métriques de performance")
    for metric, value in result['metrics'].items():
        st.write(metric, ":", value)
