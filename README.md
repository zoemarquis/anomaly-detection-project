# Projet protection

Ce projet vise à mettre en œuvre des traitements de données et une application web interactive pour visualiser les résultats. L'énoncé du projet est disponible ![ici](enonce.pdf).

--- 

## 📂 Structure du projet 

Le dépôt contient :

- Le code et les fichiers nécessaires pour exécuter la WebApp
- Les notebooks utilisés pour les traitements de données
- Un fichier ```requirements.txt``` listant les ackages nécessaires
- Un rapport détaillant l'approche, les résultats et les analyses
# TODO : link rapport

---

## 🚀 Instructions pour exécuter le projet

### 1. Télécharger et préparer les données
1. Téléchargez les données via le lien fourni dans l'énoncé
2. Décompresssez les fichiers dans un répertoire ```datasets```

vous devez obtenir la structure suivante   
datasets/  
│  
├── Network dataset/  
│   ├── csv/  
│   │   ├── attack_1.csv  
│   │   ├── attack_2.csv  
│   │   ├── attack_3.csv  
│   │   ├── attack_4.csv  
│   │   └── normal.csv  
│   │  
│   ├── pcap/  
│       ├── attack_1.pcap  
│       ├── attack_2.pcap  
│       ├── attack_3.pcap  
│       ├── attack_4.pcap  
│       └── normal.pcap  
│  
├── Physical dataset/  
│   ├── phy_att_1.csv  
│   ├── phy_att_2.csv  
│   ├── phy_att_3.csv  
│   ├── phy_att_4.csv  
│   └── phy_norm.csv  
│  
└── README.xlsx  

Assurez-vous que les fichiers sont organisés comme indiqué avant de passer à l'étape suivante.

### 2. Installer les dépendances 

Assurez-vous d'avoir Python installé. Ensuite, exécutez :
```pip install -r requirements.txt```

### 3. Exécuter les notebooks
Les notebooks doivent être exécutés dans l'ordre suivant :
    a_preparation_phy.ipynb
    b_phy_CNN1D.ipynb
    c_pca_phy.ipynb
    d_KNN_phy.ipynb
    e_CART_phy.ipynb
    g_RandomForest_phy.ipynb
    h_XGBoost_phy.ipynb
    i_MLP_phy.ipynb

    N_a_enregistrements_donnees_initiales.ipynb
    N_a2_nettoyage_network.ipynb
    N_a3_EAD_network.ipynb
    N_b_pca_network.ipynb
    N_b2_pca_table_variance.ipynb
    N_d_preparation_pour_modeles_network.ipynb
    N_e_KNN_network.ipynb
    N_f_CART_network.ipynb
    N_g_RF_network.ipynb
    N_h_XGBoost_network.ipynb
    N_i_MLP_network.ipynb






### 4. Lancer l'application Streamlit 
Pour démarrer la WebApp: 
```streamlit run homepage.py```

---

## 👷 Contributeurs

- Zoé Marquis
- Charlotte Kruzic
- Daniil Kudriashov
- Ekaterina Zaitceva