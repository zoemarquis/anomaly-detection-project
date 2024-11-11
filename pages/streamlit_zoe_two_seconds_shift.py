from streamlit_config.streamlit_defaults import *  # Assure-toi que cette bibliothèque est bien configurée pour charger les DataFrames

# Sidebar pour la sélection du dataframe
st.sidebar.header("Sélection du DataFrame")
selected_df_name = st.sidebar.selectbox(
    "Choisissez un DataFrame :", list(dict_dfs.keys())
)
selected_df = dict_dfs[selected_df_name]

# Sélection de l'heure de référence
st.title("Visualisation des données avant et après un événement")
reference_time = st.select_slider(
    "Sélectionne l'heure de référence :",
    options=selected_df["Time"].sort_values().unique(),
    value=selected_df["Time"].iloc[50],
)

# Filtrer les données 3 secondes avant et après la référence
time_window = pd.Timedelta(seconds=3)
filtered_df = selected_df.loc[
    (selected_df["Time"] >= reference_time - time_window)
    & (selected_df["Time"] <= reference_time + time_window)
]

# Vérifier si on a des données dans la plage
if not filtered_df.empty:
    st.write("Données 3 secondes avant et après l'heure de référence :")
    st.write(filtered_df)

    # Tracer toutes les colonnes
    for column in filtered_df.columns:
        if column != "Time":  # Exclure la colonne Time elle-même
            fig = px.line(
                filtered_df,
                x="Time",
                y=column,
                title=f"{column} - 3s avant et après {reference_time}",
            )
            st.plotly_chart(fig)
else:
    st.write("Aucune donnée disponible dans la plage sélectionnée.")
