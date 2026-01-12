from fastapi import FastAPI
from pydantic import BaseModel
import joblib, json
import numpy as np
import pandas as pd

app = FastAPI(title="Fraud Detection API")

#load
model = joblib.load("fraud_best_model.pkl")
scaler = joblib.load("fraud_scaler.pkl")
feature_names = json.load(open("feature_names.json"))

THRESHOLD = 0.230   #optimal threshold

class Transaction(BaseModel):
    features: dict   # key = feature name, value = numeric value


@app.get("/")
def health():
    return {"status": "online", "model": "fraud_best_model"}


@app.post("/predict")
def predict(tx: Transaction):

    raw = tx.features

    # RAW FIELDS 
    amount = float(raw.get("amount", 0))
    old_org = float(raw.get("oldbalanceOrg", 0))
    new_org = float(raw.get("newbalanceOrig", 0))
    old_dest = float(raw.get("oldbalanceDest", 0))
    new_dest = float(raw.get("newbalanceDest", 0))
    step = int(raw.get("step", 1))

    tx_type = raw.get("type", "TRANSFER")

    # FEATURE ENGINEERING

    balance_change_orig = new_org - old_org
    balance_change_dest = new_dest - old_dest

    transaction_hour = step % 24

    balance_zeroed = int((new_org == 0) and (old_org != 0))

    amount_balance_ratio = amount / (old_org + 1)

    
    if amount < 1000:
        amount_category = 0
    elif amount < 5000:
        amount_category = 1
    elif amount < 20000:
        amount_category = 2
    else:
        amount_category = 3

    # RISK TAGS
    is_high_risk_type = int(tx_type in ["TRANSFER", "CASH_OUT"])

    # Load 95th-percentile amount threshold (computed during training)
    try:
        with open("amount_q95.json") as f:
            AMOUNT_Q95 = float(json.load(f))
    except:
        # fallback — avoids breaking inference
        AMOUNT_Q95 = 100000.0

    is_large_transaction = int(amount > AMOUNT_Q95)

    # TYPE ENCODING (consistent with training) 
    type_map = {
        "TRANSFER": 1,
        "CASH_OUT": 2,
        "PAYMENT": 3,
        "DEBIT": 4
    }
    type_encoded = type_map.get(tx_type, 0)

    # BUILD FEATURE ROW 
    row = {
        "step": step,
        "amount": amount,
        "oldbalanceOrg": old_org,
        "newbalanceOrig": new_org,
        "oldbalanceDest": old_dest,
        "newbalanceDest": new_dest,
        "type_encoded": type_encoded,
        "balance_change_orig": balance_change_orig,
        "balance_change_dest": balance_change_dest,
        "transaction_hour": transaction_hour,
        "balance_zeroed": balance_zeroed,
        "amount_balance_ratio": amount_balance_ratio,
        "amount_category": amount_category,
        "is_high_risk_type": is_high_risk_type,
        "is_large_transaction": is_large_transaction,
    }

    # ORDER COLUMNS EXACTLY LIKE TRAINING
    df = pd.DataFrame([row]).reindex(columns=feature_names).astype(float)

    # SCALE + PREDICT 
    X_scaled = scaler.transform(df)
    prob = float(model.predict_proba(X_scaled)[0][1])
    label = int(prob >= THRESHOLD)

    return {
        "fraud_probability": prob,
        "is_fraud": label,
        "threshold": THRESHOLD,
        "engineered_features_used": True
    }
