import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pickleshare import PickleShareDB
import networkx as nx

# Chargement des données 1 fois au démarrage puis en cache
@st.cache_resource
def load_data():
    db = PickleShareDB("./prep_data/kity/")
    dataframes = {}
    try:
        df_net_1 = db["net_attack_1_clean"]
        df_net_2 = db["net_attack_2_clean"]
        df_net_3 = db["net_attack_3_clean"]
        df_net_4 = db["net_attack_4_clean"]
        df_net_norm = db["net_norm_clean"]
        dataframes = {
            "Attaque 1": df_net_1,
            "Attaque 2": df_net_2,
            "Attaque 3": df_net_3,
            "Attaque 4": df_net_4,
            "Normal": df_net_norm,
        }
        return dataframes
    except KeyError as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return {}


@st.cache_resource
def combine_data(dataframes):
    combined_df = pd.concat(
        [df.assign(source=name) for name, df in dataframes.items()], ignore_index=True
    )
    return combined_df


dataframes = load_data()

# Titre
st.title("Analyse exploratoire des données réseau")
st.write(
    "Cette page explore et compare les caractéristiques des différents fichiers de données réseau."
)

# Partie 1
st.header("Aperçu des Données")

file_sizes = {name: df.shape for name, df in dataframes.items()}
df_sizes = pd.DataFrame(file_sizes, index=["Lignes", "Colonnes"]).T
st.write("Taille des fichiers de données :")
st.write(df_sizes)

st.write("Premières lignes d'un des fichiers")
st.write(dataframes["Normal"].head())

unique_values_df = pd.DataFrame(
    {
        "Normal": dataframes["Normal"].nunique(),
        "Attaque 1": dataframes["Attaque 1"].nunique(),
        "Attaque 2": dataframes["Attaque 2"].nunique(),
        "Attaque 3": dataframes["Attaque 3"].nunique(),
        "Attaque 4": dataframes["Attaque 4"].nunique(),
    }
).T
st.write("Comparaison du Nombre de Valeurs Uniques par Colonne")
st.dataframe(unique_values_df)

# Partie 2
st.header("Comparaison des distributions entre les fichiers")

# A
st.subheader("Répartition des labels")
fig_label = go.Figure()
for name, df in dataframes.items():
    label_counts = df["label"].value_counts()
    fig_label.add_trace(go.Bar(x=label_counts.index, y=label_counts.values, name=name))

fig_label.update_layout(
    title="Répartition des labels",
    xaxis_title="Label",
    yaxis_title="Nombre",
    barmode="stack",
)
st.plotly_chart(fig_label)

# B
st.subheader("Répartition des ports sources et destination")
fig_sport = go.Figure()
for name, df in dataframes.items():
    fig_sport.add_trace(
        go.Bar(
            x=df["sport"].value_counts().index,
            y=df["sport"].value_counts(),
            name=name,
            opacity=0.6,
        )
    )
fig_sport.update_layout(
    title="Distribution des ports source",
    xaxis_title="Port source",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_sport)

fig_dport = go.Figure()
for name, df in dataframes.items():
    fig_dport.add_trace(
        go.Bar(
            x=df["dport"].value_counts().index,
            y=df["dport"].value_counts(),
            name=name,
            opacity=0.6,
        )
    )
fig_dport.update_layout(
    title="Distribution des ports destination",
    xaxis_title="Port destination",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_dport)

# C
# TODO : Essayer d'afficher les ports en discret
st.subheader("Répartition des flags TCP")
fig_flags = go.Figure()
for name, df in dataframes.items():
    fig_flags.add_trace(
        go.Bar(
            x=df["flags"].value_counts().index, y=df["flags"].value_counts(), name=name
        )
    )
fig_flags.update_layout(
    title="Distribution des flags TCP",
    xaxis_title="Flags TCP",
    yaxis_title="Fréquence",
    barmode="group",
)
st.plotly_chart(fig_flags)


# D
st.subheader("Taille des paquets")
fig_size = go.Figure()
for name, df in dataframes.items():
    size_counts = df["size"].value_counts()
    fig_size.add_trace(go.Bar(x=size_counts.index, y=size_counts.values, name=name))
fig_size.update_layout(
    title="Distribution de la taille des paquets",
    xaxis_title="Taille des paquets",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_size)

# E
st.subheader("Distribution des adresses IP")
fig_ip_s = go.Figure()
for name, df in dataframes.items():
    top_ip_s = df["ip_s"].value_counts()
    fig_ip_s.add_trace(go.Bar(x=top_ip_s.index, y=top_ip_s.values, name=name))

fig_ip_s.update_layout(
    title="Distribution des adresses IP source",
    xaxis_title="Adresse IP source",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_ip_s)

fig_ip_d = go.Figure()
for name, df in dataframes.items():
    top_ip_d = df["ip_d"].value_counts()
    fig_ip_d.add_trace(go.Bar(x=top_ip_d.index, y=top_ip_d.values, name=name))

fig_ip_d.update_layout(
    title="Distribution des adresses IP destination",
    xaxis_title="Adresse IP destination",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_ip_d)

# F
st.subheader("Distribution des adresses MAC")
fig_mac_s = go.Figure()
for name, df in dataframes.items():
    top_mac_s = df["mac_s"].value_counts().nlargest(10)
    fig_mac_s.add_trace(go.Bar(x=top_mac_s.index, y=top_mac_s.values, name=name))
fig_mac_s.update_layout(
    title="Distribution des adresses MAC source (Top 10)",
    xaxis_title="Adresse MAC Source",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_mac_s)

fig_mac_d = go.Figure()
for name, df in dataframes.items():
    top_mac_d = df["mac_d"].value_counts().nlargest(10)
    fig_mac_d.add_trace(go.Bar(x=top_mac_d.index, y=top_mac_d.values, name=name))
fig_mac_d.update_layout(
    title="Distribution des adresses MAC destination (Top 10)",
    xaxis_title="Adresse MAC Destination",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_mac_d)

# G
st.subheader("Distribution des fonctions Modbus")
fig_modbus_fn = go.Figure()
for name, df in dataframes.items():
    top_modbus_fn = df["modbus_fn"].value_counts().nlargest(10)
    fig_modbus_fn.add_trace(
        go.Bar(x=top_modbus_fn.index, y=top_modbus_fn.values, name=name)
    )
fig_modbus_fn.update_layout(
    title="Distribution des fonctions Modbus",
    xaxis_title="Fonction Modbus",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_modbus_fn)

# H
st.subheader("Distribution des réponses Modbus")
fig_modbus_response = go.Figure()
for name, df in dataframes.items():
    top_modbus_response = df["modbus_response"].value_counts()
    fig_modbus_response.add_trace(
        go.Bar(x=top_modbus_response.index, y=top_modbus_response.values, name=name)
    )
fig_modbus_response.update_layout(
    title="Distribution des réponses Modbus",
    xaxis_title="Réponse Modbus",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_modbus_response)

# I
st.subheader("Distribution du nombre de paquets")
fig_n_pkt_src = go.Figure()
for name, df in dataframes.items():
    top_n_pkt_src = df["n_pkt_src"].value_counts()
    fig_n_pkt_src.add_trace(
        go.Bar(x=top_n_pkt_src.index, y=top_n_pkt_src.values, name=name)
    )
fig_n_pkt_src.update_layout(
    title="Distribution du nombre de paquets source",
    xaxis_title="Nombre de paquets source",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_n_pkt_src)

st.subheader("Distribution du Nombre de Paquets Destination")
fig_n_pkt_dst = go.Figure()
for name, df in dataframes.items():
    top_n_pkt_dst = df["n_pkt_dst"].value_counts()
    fig_n_pkt_dst.add_trace(
        go.Bar(x=top_n_pkt_dst.index, y=top_n_pkt_dst.values, name=name)
    )
fig_n_pkt_dst.update_layout(
    title="Distribution du nombre de paquets destination",
    xaxis_title="Nombre de paquets destination",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_n_pkt_dst)


# Partie 3
combined_df = combine_data(dataframes)

st.header("Comparaison des distributions entre les labels")

# A
st.subheader("Distribution des ports par label")
fig_sport = go.Figure()
for label in combined_df["label"].unique():
    label_df = combined_df[combined_df["label"] == label]
    top_sport = label_df["sport"].value_counts()
    fig_sport.add_trace(go.Bar(x=top_sport.index, y=top_sport.values, name=label))

fig_sport.update_layout(
    title="Distribution des ports source par label",
    xaxis_title="Port source",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_sport)

fig_dport = go.Figure()
for label in combined_df["label"].unique():
    label_df = combined_df[combined_df["label"] == label]
    top_dport = label_df["dport"].value_counts()
    fig_dport.add_trace(go.Bar(x=top_dport.index, y=top_dport.values, name=label))

fig_dport.update_layout(
    title="Distribution des ports destination par label",
    xaxis_title="Port destination",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_dport)

# B
st.subheader("Distribution des flags TCP par label")
fig_flags = go.Figure()
for label in combined_df["label"].unique():
    label_df = combined_df[combined_df["label"] == label]
    top_flags = label_df["flags"].value_counts()
    fig_flags.add_trace(go.Bar(x=top_flags.index, y=top_flags.values, name=label))

fig_flags.update_layout(
    title="Distribution des flags TCP par label",
    xaxis_title="Flags TCP",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_flags)

# C
st.subheader("Distribution de la taille des paquets par label")
fig_size = go.Figure()
for label in combined_df["label"].unique():
    label_df = combined_df[combined_df["label"] == label]
    top_size = label_df["size"].value_counts()
    fig_size.add_trace(go.Bar(x=top_size.index, y=top_size.values, name=label))

fig_size.update_layout(
    title="Distribution de la taille des paquets par label",
    xaxis_title="Taille des paquets",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_size)

# D
st.subheader("Distribution des adresses IP par label")
fig_ip_s = go.Figure()
for label in combined_df["label"].unique():
    label_df = combined_df[combined_df["label"] == label]
    top_ip_s = label_df["ip_s"].value_counts()
    fig_ip_s.add_trace(go.Bar(x=top_ip_s.index, y=top_ip_s.values, name=label))

fig_ip_s.update_layout(
    title="Distribution des adresses IP source par label",
    xaxis_title="Adresse IP source",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_ip_s)

fig_ip_d = go.Figure()
for label in combined_df["label"].unique():
    label_df = combined_df[combined_df["label"] == label]
    top_ip_d = label_df["ip_d"].value_counts()
    fig_ip_d.add_trace(go.Bar(x=top_ip_d.index, y=top_ip_d.values, name=label))

fig_ip_d.update_layout(
    title="Distribution des adresses IP destination par label",
    xaxis_title="Adresse IP destination",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_ip_d)

# E
st.subheader("Distribution des fonctions Modbus par label")
fig_modbus_fn = go.Figure()
for label in combined_df["label"].unique():
    label_df = combined_df[combined_df["label"] == label]
    top_modbus_fn = label_df["modbus_fn"].value_counts()
    fig_modbus_fn.add_trace(
        go.Bar(x=top_modbus_fn.index, y=top_modbus_fn.values, name=label)
    )

fig_modbus_fn.update_layout(
    title="Distribution des fonctions Modbus par label",
    xaxis_title="Fonction Modbus",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_modbus_fn)

# F
st.subheader("Distribution des réponses Modbus par label")
fig_modbus_response = go.Figure()
for label in combined_df["label"].unique():
    label_df = combined_df[combined_df["label"] == label]
    top_modbus_response = label_df["modbus_response"].value_counts()
    fig_modbus_response.add_trace(
        go.Bar(x=top_modbus_response.index, y=top_modbus_response.values, name=label)
    )

fig_modbus_response.update_layout(
    title="Distribution des réponses Modbus par label",
    xaxis_title="Réponse Modbus",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_modbus_response)

# G
st.subheader("Distribution du nombre de paquets par label")
fig_n_pkt_src = go.Figure()
for label in combined_df["label"].unique():
    label_df = combined_df[combined_df["label"] == label]
    top_n_pkt_src = label_df["n_pkt_src"].value_counts()
    fig_n_pkt_src.add_trace(
        go.Bar(x=top_n_pkt_src.index, y=top_n_pkt_src.values, name=label)
    )

fig_n_pkt_src.update_layout(
    title="Distribution du nombre de paquets source par label",
    xaxis_title="Nombre de paquets source",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_n_pkt_src)

fig_n_pkt_dst = go.Figure()
for label in combined_df["label"].unique():
    label_df = combined_df[combined_df["label"] == label]
    top_n_pkt_dst = label_df["n_pkt_dst"].value_counts()
    fig_n_pkt_dst.add_trace(
        go.Bar(x=top_n_pkt_dst.index, y=top_n_pkt_dst.values, name=label)
    )

fig_n_pkt_dst.update_layout(
    title="Distribution du nombre de paquets destination par label",
    xaxis_title="Nombre de paquets destination",
    yaxis_title="Fréquence",
    barmode="stack",
)
st.plotly_chart(fig_n_pkt_dst)
