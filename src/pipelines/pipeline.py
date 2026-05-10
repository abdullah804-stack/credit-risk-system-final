from src.data.load_data import load_data
from src.features.build_features import preprocess_data
from src.models.train_model import train_model, save_model
from sklearn.model_selection import train_test_split


def run_training_pipeline(data_path):
    # Load data
    df = load_data(data_path)

    # Preprocess data
    df = preprocess_data(df)

    # Split features and target
    X = df.drop("loan_status", axis=1)
    y = df["loan_status"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    import joblib

    # Save feature columns
    joblib.dump(X.columns, "features.pkl")

    # Train model
    model = train_model(X_train, y_train)

    # Save model
    save_model(model, path="model.pkl")


    print("Training pipeline completed successfully.")
    return model  