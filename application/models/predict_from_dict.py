import pickle
import pandas as pd
# Charger ton modèle
import joblib

model = joblib.load("my_model.pkl")



def predict_from_dict(stats_dict):
    """
    stats_dict: dictionnaire des stats du match (shots, corners, saves…)
    """
    X = pd.DataFrame([stats_dict])
    pred = model.predict(X)
    return pred[0]
