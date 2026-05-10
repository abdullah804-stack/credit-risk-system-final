from src.pipelines.pipeline import run_training_pipeline
if __name__ == "__main__":
    data_path = "data/raw/loan_data.csv"
    model = run_training_pipeline(data_path)