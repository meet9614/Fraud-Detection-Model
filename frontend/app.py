import os
print("Streamlit app starting...")
print("Secrets available:", os.environ.keys())

import streamlit as st
import requests

st.set_page_config(page_title="Fraud Detection UI")

API_URL = os.environ.get("API_URL")

print("API_URL =", API_URL)

st.title("Fraud Detection — Transaction Risk Scoring by MEET")
st.caption(f"Backend API: {API_URL}")

st.subheader("Enter Transaction Details")

# -------- RAW INPUT FIELDS (only these are required) --------

step = st.number_input("Step (Time Step)", min_value=1, step=1)

amount = st.number_input("Transaction Amount", min_value=0.0, step=10.0)

old_balance = st.number_input("Old Balance (Origin)", min_value=0.0, step=10.0)
new_balance = st.number_input("New Balance (Origin)", min_value=0.0, step=10.0)

old_dest = st.number_input("Old Balance (Destination)", min_value=0.0, step=10.0)
new_dest = st.number_input("New Balance (Destination)", min_value=0.0, step=10.0)

tx_type = st.selectbox(
    "Transaction Type",
    ["TRANSFER", "CASH_OUT", "PAYMENT", "DEBIT"]
)

# -------- PAYLOAD SENT TO FASTAPI --------
payload = {
    "features": {
        "step": int(step),
        "amount": float(amount),
        "oldbalanceOrg": float(old_balance),
        "newbalanceOrig": float(new_balance),
        "oldbalanceDest": float(old_dest),
        "newbalanceDest": float(new_dest),
        "type": tx_type
    }
}

st.write("Payload sent to API:")
st.json(payload)


# -------- SEND REQUEST --------
if st.button("Predict Fraud Risk"):

    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=payload,
            timeout=20
        )

        result = response.json()

        st.subheader("API Response")
        st.json(result)

        # graceful error handling
        if "fraud_probability" not in result:
            st.error("API returned an error instead of prediction.")
            st.stop()

        prob = result["fraud_probability"]
        label = result["is_fraud"]
        threshold = result["threshold"]

        st.success("Prediction Received")

        st.metric(
            "Fraud Probability",
            f"{prob:.3f}",
            help=f"Threshold = {threshold}"
        )

        if label == 1:
            st.error("⚠ Transaction Flagged as FRAUD")
        else:
            st.success("✓ Transaction Marked as SAFE")

    except Exception as e:
        st.error(f"Connection failed: {e}")
