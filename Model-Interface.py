# frontend.py
import streamlit as st
import requests

st.title("Stress Detection Web App")

BVP = st.number_input("BVP")
EDA = st.number_input("EDA")
TEMP = st.number_input("TEMP")
ACC_option = st.selectbox("ACC activity", ["No movement", "Little active", "Highly active"])

# Map ACC option to example values (you can customize)
ACC_map = {
    "No movement": (0, 0, 0),
    "Little active": (10, 5, 12),
    "Highly active": (30, -6, 55)
}
ACC_x, ACC_y, ACC_z = ACC_map[ACC_option]

if st.button("Predict Stress"):
    payload = {
        "BVP": BVP,
        "EDA": EDA,
        "TEMP": TEMP,
        "ACC_x": ACC_x,
        "ACC_y": ACC_y,
        "ACC_z": ACC_z
    }
    response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    st.write("Predicted Stress Status:", response.json()["prediction"])
