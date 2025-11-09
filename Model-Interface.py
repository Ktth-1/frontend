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
    response = requests.post("https://nonpestilent-mercedez-mousey.ngrok-free.dev/predict", json=payload)
    if response.status_code == 200:
        st.write("Predicted Stress Status:", response.json().get("prediction"))
    else:
        st.error(f"API Error: {response.status_code}")
        st.text(response.text)
    st.write("Predicted Stress Status:", response.json()["prediction"])
