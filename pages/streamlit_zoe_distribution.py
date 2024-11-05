from streamlit_config.streamlit_defaults import *

# Sidebar pour la sélection du dataframe
st.sidebar.header("Sélection du DataFrame")
selected_df_name = st.sidebar.selectbox("Choisissez un DataFrame :", list(dict_dfs.keys()))
selected_df = dict_dfs[selected_df_name]

# Sidebar pour la sélection de la colonne
st.sidebar.header("Options de Visualisation")
selected_column = st.sidebar.selectbox("Choisissez une colonne :", selected_df.columns)

# Type de graphique
plot_type = st.sidebar.radio("Choisissez le type de graphique :", ["Histogramme", "Boîte à moustaches"])

# Afficher le titre du dataframe sélectionné
st.header(f"Visualisation pour le DataFrame : {selected_df_name}")

# Histogramme
if plot_type == "Histogramme":
    st.subheader(f"Distribution de '{selected_column}' - Histogramme")
    fig = px.histogram(selected_df, x=selected_column, nbins=30, title=f"Histogramme de {selected_column}")
    fig.update_layout(bargap=0.1, xaxis_title=selected_column, yaxis_title="Fréquence")
    st.plotly_chart(fig)

# Boîte à moustaches
elif plot_type == "Boîte à moustaches":
    st.subheader(f"Distribution de '{selected_column}' - Boîte à moustaches")
    fig = px.box(selected_df, y=selected_column, title=f"Boîte à moustaches de {selected_column}")
    fig.update_layout(yaxis_title=selected_column)
    st.plotly_chart(fig)

# Afficher le dataframe sélectionné
st.subheader("Aperçu du DataFrame sélectionné")
st.write(selected_df.head())


# améliorer pour pouvoir sélectoinner 1 / plusieurs df
# plot plusieurs vizs en même temps : histogramme, boîte à moustaches, scatter plot, etc.