from streamlit_config.streamlit_defaults import *  # Assure-toi que cette bibliothèque est bien configurée pour charger les DataFrames

st.title("Page 1 - Analyse des Données")

# Sidebar pour la sélection du dataframe
st.sidebar.header("Sélection du DataFrame")
selected_df_name = st.sidebar.selectbox("Choisissez un DataFrame :", list(dict_dfs.keys()))
selected_df = dict_dfs[selected_df_name]

# Convertir la colonne 'Time' en datetime si ce n'est pas déjà fait
selected_df['Time'] = pd.to_datetime(selected_df['Time'], errors='coerce')

# Supprimer les valeurs NaT résultant d'erreurs de conversion
selected_df = selected_df.dropna(subset=['Time'])

# Calculer la différence de temps entre chaque ligne
selected_df['Time_Diff'] = selected_df['Time'].diff().dt.total_seconds()

# Filtrer pour trouver les lignes avec une différence de 2 secondes
two_second_diff = selected_df[selected_df['Time_Diff'] == 2]

# Affichage
st.title("Visualisation des différences de 2 secondes")
if not two_second_diff.empty:
    st.write("Lignes avec une différence de temps de 2 secondes :")
    
    # Préparer les données pour le tableau
    comparison_data = []

    for index in two_second_diff.index:
        if index > 0:  # S'assurer qu'il y a une ligne précédente à comparer
            before_values = selected_df.iloc[index - 1].drop('Time').to_dict()
            after_values = selected_df.iloc[index].drop('Time').to_dict()
            
            # Créer une ligne de comparaison
            comparison_row = {'Variable': 'Avant'}
            comparison_row.update(before_values)
            comparison_data.append(comparison_row)
            
            comparison_row = {'Variable': 'Après'}
            comparison_row.update(after_values)
            comparison_data.append(comparison_row)

    # Convertir en DataFrame pour affichage
    comparison_df = pd.DataFrame(comparison_data)

    # Réorganiser le DataFrame pour avoir une colonne par variable
    comparison_df.set_index('Variable', inplace=True)

    # Afficher le tableau
    st.write("Comparaison des valeurs avant et après :", comparison_df)

else:
    st.write("Aucune différence de 2 secondes trouvée.")