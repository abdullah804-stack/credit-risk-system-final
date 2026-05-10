import pandas as pd
import numpy as np


def preprocess_data(df):

    # -------------------------------
    # 1. TARGET (only for training)
    # -------------------------------
    if "loan_status" in df.columns:
        df["loan_status"] = df["loan_status"].apply(
            lambda x: 1 if x == "Charged Off" else 0
        )

    # -------------------------------
    # 2. DROP UNNECESSARY COLUMNS
    # -------------------------------
    drop_cols = ["emp_title", "title", "address", "grade", "sub_grade"]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])

    # -------------------------------
    # 3. HANDLE MISSING VALUES (SAFE)
    # -------------------------------
    df["emp_length"] = df.get("emp_length", "Unknown")
    df["emp_length"] = df["emp_length"].fillna("Unknown")

    if "mort_acc" in df.columns:
        df["mort_acc"] = df["mort_acc"].fillna(df["mort_acc"].median())

    if "pub_rec_bankruptcies" in df.columns:
        df["pub_rec_bankruptcies"] = df["pub_rec_bankruptcies"].fillna(0)

    if "revol_util" in df.columns:
        df["revol_util"] = df["revol_util"].fillna(df["revol_util"].median())

    # -------------------------------
    # 4. DATE FEATURES (SAFE)
    # -------------------------------
    if "issue_d" in df.columns:
        df["issue_year"] = pd.to_datetime(
            df["issue_d"], format="%b-%Y", errors="coerce"
        ).dt.year

    if "earliest_cr_line" in df.columns:
        df["credit_history_year"] = pd.to_datetime(
            df["earliest_cr_line"], format="%b-%Y", errors="coerce"
        ).dt.year

    if "issue_year" in df.columns and "credit_history_year" in df.columns:
        df["credit_age"] = df["issue_year"] - df["credit_history_year"]

    # Drop date columns safely
    df = df.drop(
        columns=[col for col in ["issue_d", "earliest_cr_line"] if col in df.columns]
    )

    # -------------------------------
    # 5. FEATURE ENGINEERING (SAFE)
    # -------------------------------
    if all(col in df.columns for col in ["loan_amnt", "annual_inc", "installment"]):

        df["annual_inc"] = df["annual_inc"].replace(0, np.nan)

        df["loan_income_ratio"] = df["loan_amnt"] / df["annual_inc"]
        df["installment_income_ratio"] = df["installment"] / df["annual_inc"]

        # Handle inf and NaN
        df.replace([np.inf, -np.inf], np.nan, inplace=True)

        df["loan_income_ratio"] = df["loan_income_ratio"].fillna(0)
        df["installment_income_ratio"] = df["installment_income_ratio"].fillna(0)

    # -------------------------------
    # 6. ENCODING
    # -------------------------------
    df = pd.get_dummies(df, drop_first=True)

    # -------------------------------
    # 7. CLEAN COLUMN NAMES (CRITICAL)
    # -------------------------------
    df.columns = df.columns.str.replace(r"[^\w]", "_", regex=True)
    df.columns = df.columns.astype(str)

    return df