from src.pipelines.predict_pipeline import predict

sample = {
    "loan_amnt": 10000,
    "term": "36 months",
    "int_rate": 12.5,
    "installment": 300,
    "annual_inc": 50000,
    "dti": 15,
    "open_acc": 10,
    "revol_bal": 5000,
    "revol_util": 40,
    "total_acc": 25,
    "application_type": "INDIVIDUAL",
    "home_ownership": "RENT",
    "verification_status": "Verified",
    "purpose": "credit_card",
    "issue_d": "Jan-2015",
    "earliest_cr_line": "Jan-2010"
}

prediction, probability = predict(sample)

print("Prediction:", prediction)
print("Probability:", probability)