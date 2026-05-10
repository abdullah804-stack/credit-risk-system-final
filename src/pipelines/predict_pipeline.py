import joblib
import pandas as pd
from src.models.train_model import load_model
from src.features.build_features import preprocess_data


def predict(data_dict):

    # Load model
    model = load_model()

    # Load feature schema
    feature_columns = joblib.load("features.pkl")

    # Convert input to DataFrame
    df = pd.DataFrame([data_dict])

    # Preprocess
    df = preprocess_data(df)

    # 🔥 Align features (MOST IMPORTANT LINE)
    df = df.reindex(columns=feature_columns, fill_value=0)

    # Predict
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return prediction, probability