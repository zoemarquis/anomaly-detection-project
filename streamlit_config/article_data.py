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


article_data = [
    knn_phy,
    rf_phy,
    svm_phy,
    nb_phy,
]
