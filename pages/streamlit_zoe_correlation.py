from streamlit_config.streamlit_defaults import *
import numpy as np
from sklearn.decomposition import PCA

from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

from plotly.subplots import make_subplots

# ATTENTION  : kes données ici ne sont pas nettoyées !!
# c'est pour se donner des idées de viz, pas pour faire des analyses sérieuses
# drop flow_sensor_3
# et renommer lable_n en label_n

df_phy_1.drop(columns=["Flow_sensor_3"], inplace=True)
df_phy_2.drop(columns=["Flow_sensor_3"], inplace=True)
df_phy_3.drop(columns=["Flow_sensor_3"], inplace=True)
df_phy_4.drop(columns=["Flow_sensor_3"], inplace=True)
df_phy_norm.drop(columns=["Flow_sensor_3"], inplace=True)

df_phy_2.rename(columns={"Lable_n": "Label_n"}, inplace=True)

df_phy_1["Label_n"] = df_phy_1["Label_n"].astype("category")
df_phy_2["Label_n"] = df_phy_2["Label_n"].astype("category")
df_phy_3["Label_n"] = df_phy_3["Label_n"].astype("category")
df_phy_4["Label_n"] = df_phy_4["Label_n"].astype("category")
df_phy_norm["Label_n"] = df_phy_norm["Label_n"].astype("category")

# supprimer label_n car pas nuémrique mais catégorielle !

# 1. on sépare un gros dataset attaque (1234) et un dataset normal
# a. on ne prend que les valeurs numériques
# b. on fait un one hot encoding de toutes les colonnes non numériques

# 2. on regroupe tous les dataframe ensemble
# a. que les valeurs numériques
# b. on fait un one hot encoding de toutes les colonnes non numériques


def get_df_encoded(
    df,
):  # ici one hot, d'autres sont possibles (genre le label encoder ?)
    cat_cols = df.select_dtypes(exclude=[np.number]).columns
    df_encoded = pd.get_dummies(df, columns=cat_cols)
    return df_encoded


# a : numériques
df_phy_1_num = df_phy_1.select_dtypes(include=[np.number])
df_phy_2_num = df_phy_2.select_dtypes(include=[np.number])
df_phy_3_num = df_phy_3.select_dtypes(include=[np.number])
df_phy_4_num = df_phy_4.select_dtypes(include=[np.number])
df_phy_norm_num = df_phy_norm.select_dtypes(include=[np.number])

# b : encoded
df_phy_1_encoded = get_df_encoded(df_phy_1)
df_phy_2_encoded = get_df_encoded(df_phy_2)
df_phy_3_encoded = get_df_encoded(df_phy_3)
df_phy_4_encoded = get_df_encoded(df_phy_4)
df_phy_norm_encoded = get_df_encoded(df_phy_norm)

# 1a
df_phy_att_num = pd.concat([df_phy_1_num, df_phy_2_num, df_phy_3_num, df_phy_4_num])
df_phy_norm_num = df_phy_norm_num

# 1b
df_phy_att_encoded = pd.concat(
    [df_phy_1_encoded, df_phy_2_encoded, df_phy_3_encoded, df_phy_4_encoded]
)
df_phy_norm_encoded = df_phy_norm_encoded

# 2a
df_phy_all_num = pd.concat(
    [df_phy_1_num, df_phy_2_num, df_phy_3_num, df_phy_4_num, df_phy_norm_num]
)

# 2b
df_phy_all_encoded = pd.concat(
    [
        df_phy_1_encoded,
        df_phy_2_encoded,
        df_phy_3_encoded,
        df_phy_4_encoded,
        df_phy_norm_encoded,
    ]
)


# Visualisation

corr_att_num = df_phy_att_num.corr()
corr_norm_num = df_phy_norm_num.corr()
corr_all_num = df_phy_all_num.corr()

# Création des heatmaps
fig_att = px.imshow(
    corr_att_num,
    title="Matrice de Corrélations - Attaque",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
)
fig_norm = px.imshow(
    corr_norm_num,
    title="Matrice de Corrélations - Benign",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
)
fig_all = px.imshow(
    corr_all_num,
    title="Matrice de Corrélations - Tous les Datasets",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
)

# Affichage des heatmaps dans Streamlit sur la même ligne
st.title("Corrélations entre les Labels")

# Utilisation de st.columns pour afficher les matrices sur la même ligne
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Matrice de Corrélations - Attaque")
    st.plotly_chart(fig_att)

with col2:
    st.subheader("Matrice de Corrélations - Benign")
    st.plotly_chart(fig_norm)

with col3:
    st.subheader("Matrice de Corrélations - Tous les Datasets")
    st.plotly_chart(fig_all)


# # 1 b : trop lourd l'encodage: trop de colonnes
# st.subheader("Matrice de Corrélations - Datasets Attaques - données encodées")
# corr_att_encoded = df_phy_att_encoded.corr()
# fig_att_encoded = px.imshow(corr_att_encoded, title="Matrice de Corrélations - Attaque", color_continuous_scale='Viridis', zmin=-1, zmax=1)
# st.plotly_chart(fig_att_encoded)
#
# st.subheader("Matrice de Corrélations - Datasets Normal - données encodées")
# corr_att_encoded = df_phy_norm_encoded.corr()
# fig_att_encoded = px.imshow(corr_att_encoded, title="Matrice de Corrélations - Normal", color_continuous_scale='Viridis', zmin=-1, zmax=1)
# st.plotly_chart(fig_att_encoded)

# # 2 b
# st.subheader("Matrice de Corrélations - Tous les Datasets - données encodées")
# corr_all_encoded = df_phy_all_encoded.corr()
# fig_all_encoded = px.imshow(corr_all_encoded, title="Matrice de Corrélations - Tous les Datasets", color_continuous_scale='Viridis', zmin=-1, zmax=1)
# st.plotly_chart(fig_all_encoded)


# Réduction de dimension avec PCA

# Exemple: df_phy_all_encoded est le DataFrame combiné avec un encodage one-hot
# Assurez-vous d'utiliser uniquement les colonnes numériques
numeric_cols = df_phy_all_encoded.select_dtypes(include=[np.number]).columns
X = df_phy_all_encoded[numeric_cols]

# 1. Normalisation des données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 2. PCA
pca = PCA(n_components=2)  # Vous pouvez ajuster le nombre de composantes
X_pca = pca.fit_transform(X_scaled)

# 3. Création d'un DataFrame pour les résultats PCA
pca_df = pd.DataFrame(data=X_pca, columns=["PC1", "PC2"])

# Ajout d'une colonne pour les étiquettes si nécessaire
# pca_df['Label'] = ...  # Ajoutez une colonne si vous souhaitez colorer par labels

# 4. Visualisation avec Plotly
fig = px.scatter(
    pca_df,
    x="PC1",
    y="PC2",
    title="PCA - Projection des Données",
    # color='Label',  # Décommentez si vous ajoutez des labels
    labels={"PC1": "Composante Principale 1", "PC2": "Composante Principale 2"},
)

# Affichage dans Streamlit
st.title("Analyse en Composantes Principales (PCA)")
st.plotly_chart(fig)


# Exemple: df_phy_all_encoded est le DataFrame combiné avec un encodage one-hot
# Assurez-vous d'utiliser uniquement les colonnes numériques
numeric_cols = df_phy_all_encoded.select_dtypes(include=[np.number]).columns
X = df_phy_all_encoded[numeric_cols]

# 1. Normalisation des données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 2. PCA
pca = PCA(
    n_components=len(numeric_cols)
)  # Ajuster le nombre de composantes selon le besoin
X_pca = pca.fit_transform(X_scaled)

# 3. Création d'un DataFrame pour les résultats PCA
pca_df = pd.DataFrame(data=X_pca, columns=[f"PC{i+1}" for i in range(X_pca.shape[1])])

# 4. Variance expliquée
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)

# 5. Affichage des informations PCA
st.title("Analyse en Composantes Principales (PCA)")

# Affichage des valeurs de variance expliquée
st.subheader("Variance Expliquée par Composante")
variance_df = pd.DataFrame(
    {
        "Composante": [f"PC{i+1}" for i in range(len(explained_variance))],
        "Variance Expliquée": explained_variance,
        "Variance Cumulée": cumulative_variance,
    }
)

st.write(variance_df)

# Graphique de dispersion pour les deux premières composantes
fig = px.scatter(
    pca_df,
    x="PC1",
    y="PC2",
    title="PCA - Projection des Données",
    labels={"PC1": "Composante Principale 1", "PC2": "Composante Principale 2"},
)

st.plotly_chart(fig)

# Graphique des valeurs propres
fig_eigen = go.Figure()
fig_eigen.add_trace(
    go.Scatter(
        x=[f"PC{i+1}" for i in range(len(explained_variance))],
        y=explained_variance,
        mode="lines+markers",
        name="Variance Expliquée",
        marker=dict(color="blue"),
    )
)

fig_eigen.update_layout(
    title="Valeurs Propres des Composantes",
    xaxis_title="Composantes",
    yaxis_title="Variance Expliquée",
    yaxis=dict(range=[0, 1]),
)
st.plotly_chart(fig_eigen)

# Heatmap des composantes
components_df = pd.DataFrame(data=pca.components_, columns=numeric_cols)
fig_heatmap = px.imshow(
    components_df,
    title="Heatmap des Composantes Principales",
    labels=dict(x="Variables", y="Composantes"),
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
)
st.plotly_chart(fig_heatmap)


# autres réductions de dimensions
