from streamlit_config.streamlit_defaults import *
import numpy as np
from sklearn.decomposition import PCA

from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

from plotly.subplots import make_subplots
from sklearn.preprocessing import LabelEncoder

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

for df in [df_phy_1, df_phy_2, df_phy_3, df_phy_4, df_phy_norm]:
    df["Flow_sensor_1"] = pd.to_numeric(df["Flow_sensor_1"], errors='coerce')
    df['Flow_sensor_2'] = df['Flow_sensor_2'].apply(lambda x: 4000 if x else 0).astype(int)

print()



# a : numériques
df_phy_1_num = df_phy_1.select_dtypes(include=[np.number])
df_phy_2_num = df_phy_2.select_dtypes(include=[np.number])
df_phy_3_num = df_phy_3.select_dtypes(include=[np.number])
df_phy_4_num = df_phy_4.select_dtypes(include=[np.number])
df_phy_norm_num = df_phy_norm.select_dtypes(include=[np.number])


scaler = StandardScaler()
df_phy_1_num_scaled = pd.DataFrame(
    scaler.fit_transform(df_phy_1_num), columns=df_phy_1_num.columns
)
df_phy_2_num_scaled = pd.DataFrame(
    scaler.fit_transform(df_phy_2_num), columns=df_phy_2_num.columns
)
df_phy_3_num_scaled = pd.DataFrame(
    scaler.fit_transform(df_phy_3_num), columns=df_phy_3_num.columns
)
df_phy_4_num_scaled = pd.DataFrame(
    scaler.fit_transform(df_phy_4_num), columns=df_phy_4_num.columns
)
df_phy_norm_num_scaled = pd.DataFrame(
    scaler.fit_transform(df_phy_norm_num), columns=df_phy_norm_num.columns
)

# 1a
df_phy_att_num_scaled = pd.concat(
    [
        df_phy_1_num_scaled,
        df_phy_2_num_scaled,
        df_phy_3_num_scaled,
        df_phy_4_num_scaled,
    ]
)

df_phy_norm_num_scaled = df_phy_norm_num_scaled

# 2a
df_phy_all_num_scaled = pd.concat(
    [
        df_phy_1_num_scaled,
        df_phy_2_num_scaled,
        df_phy_3_num_scaled,
        df_phy_4_num_scaled,
        df_phy_norm_num_scaled,
    ]
)

# Visualisation

corr_att_num = df_phy_att_num_scaled.corr()
corr_norm_num = df_phy_norm_num_scaled.corr()
corr_all_num = df_phy_all_num_scaled.corr()

# Création des heatmaps
fig_att = px.imshow(
    corr_att_num,
    title="Matrice de corrélations des 4 datasets d'attaque",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
)
fig_norm = px.imshow(
    corr_norm_num,
    title="Matrice de corrélations du dataset normal",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
)
fig_all = px.imshow(
    corr_all_num,
    title="Matrice de corrélations avec tous les datasets",
    color_continuous_scale="RdBu",
    zmin=-1,
    zmax=1,
)

# Affichage des heatmaps dans Streamlit sur la même ligne
st.title("Corrélations entre les Labels")

# Utilisation de st.columns pour afficher les matrices sur la même ligne
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(fig_att)

with col2:
    st.plotly_chart(fig_norm)

with col3:
    st.plotly_chart(fig_all)


# 1 b et 2 b : trop lourd l'encodage: trop de colonnes

