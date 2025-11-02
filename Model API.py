from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib

# ----------------------------
# Load model & scaler
# ----------------------------
MODEL_PATH = "random_forest_wrist_stress_WESAD_with_BVP.pkl"
SCALER_PATH = "random_forest_wrist_stress_scaler_with_BVP.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ----------------------------
# FastAPI setup
# ----------------------------
app = FastAPI(title="Stress Detection API")

class SensorInput(BaseModel):
    BVP: float
    EDA: float
    TEMP: float
    ACC_x: float
    ACC_y: float
    ACC_z: float

def stats(arr):
    s = pd.Series(arr)
    return {
        'mean': float(s.mean()),
        'std': float(s.std()),
        'min': float(s.min()),
        'max': float(s.max()),
        'median': float(s.median()),
        'skew': float(s.skew()),
        'kurt': float(s.kurt())
    }

def extract_features_window(signals):
    row = {}
    # EDA
    if "EDA" in signals:
        st = stats(signals["EDA"])
        row.update({f"EDA_{k}": v for k, v in st.items()})
    # TEMP
    if "TEMP" in signals:
        st = stats(signals["TEMP"])
        row.update({f"TEMP_{k}": v for k, v in st.items()})
        row["TEMP_slope"] = (signals["TEMP"][-1] - signals["TEMP"][0]) / len(signals["TEMP"])
    # ACC magnitude
    if all(k in signals for k in ["ACC_x", "ACC_y", "ACC_z"]):
        ax, ay, az = signals["ACC_x"], signals["ACC_y"], signals["ACC_z"]
        mag = np.sqrt(ax ** 2 + ay ** 2 + az ** 2)
        st = stats(mag)
        row.update({f"ACC_mag_{k}": v for k, v in st.items()})
        row["ACC_energy"] = float(np.sum(mag ** 2) / len(mag))
    # BVP features
    if "BVP" in signals:
        st = stats(signals["BVP"])
        row.update({f"BVP_{k}": v for k, v in st.items()})
    return row

@app.post("/predict")
def predict_stress(input: SensorInput):
    # Create window arrays (single-value repeated to avoid empty slice warnings)
    signals = {
        "BVP": np.array([input.BVP] * 160),   # 5s * 32Hz
        "EDA": np.array([input.EDA] * 160),
        "TEMP": np.array([input.TEMP] * 160),
        "ACC_x": np.array([input.ACC_x] * 160),
        "ACC_y": np.array([input.ACC_y] * 160),
        "ACC_z": np.array([input.ACC_z] * 160),
    }
    features = extract_features_window(signals)
    df_features = pd.DataFrame([features])
    df_scaled = scaler.transform(df_features)
    prediction = model.predict(df_scaled)[0]
    status = "STRESSED" if prediction == 1 else "NOT STRESSED"
    return {"prediction": status}
