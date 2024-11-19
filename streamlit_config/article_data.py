knn_phy = {
    "data": "PHY",
    "model_type": "KNN article",
    "attack_type": "labeln",
    "accuracy": 0.98,
    "recall": 0.95,
    "precision": 0.95,
    "f1": 0.95,
    "article": True,
}

knn_netw = {
    "data": "NETW",
    "model_type": "KNN article",
    "attack_type": "labeln",
    "accuracy": 0.77,
    "recall": 0.44,
    "precision": 0.68,
    "f1": 0.53,
    "article": True,
}

rf_phy = {
    "data": "PHY",
    "model_type": "RF article",
    "attack_type": "labeln",
    "accuracy": 0.99,
    "recall": 0.98,
    "precision": 0.95,
    "f1": 0.97,
    "article": True,
}

rf_netw = {
    "data": "NETW",
    "model_type": "RF article",
    "attack_type": "labeln",
    "accuracy": 0.75,
    "recall": 0.53,
    "precision": 0.56,
    "f1": 0.54,
}

svm_phy = {
    "data": "PHY",
    "model_type": "SVM article",
    "attack_type": "labeln",
    "accuracy": 0.93,
    "recall": 0.92,
    "precision": 0.64,
    "f1": 0.75,
    "article": True,
}

svm_netw = {
    "data": "NETW",
    "model_type": "SVM article",
    "attack_type": "labeln",
    "accuracy": 0.69,
    "recall": 0.99,
    "precision": 0.10,
    "f1": 0.20,
}

nb_phy = {
    "data": "PHY",
    "model_type": "NB article",
    "attack_type": "labeln",
    "accuracy": 0.93,
    "recall": 0.92,
    "precision": 0.66,
    "f1": 0.77,
    "article": True,
}

nb_netw = {
    "data": "NETW",
    "model_type": "NB article",
    "attack_type": "labeln",
    "accuracy": 0.75,
    "recall": 0.15,
    "precision": 0.90,
    "f1": 0.27,
}


article_data_phy = [
    knn_phy,
    rf_phy,
    svm_phy,
    nb_phy,
]

article_data_netw = [
    knn_netw,
    rf_netw,
    svm_netw,
    nb_netw,
]
