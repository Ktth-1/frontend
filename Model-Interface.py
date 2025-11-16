# frontend.py
import streamlit as st
import requests

st.title("Stress Detection Web App")

BVP = st.number_input("Blood Volume Pulse (-500 - 1200)")
EDA = st.number_input("Electrodermal Activity (µS)")
TEMP = st.number_input("Body Temperature (°C)")
ACC_option = st.selectbox("Movement activity", ["No movement", "Little movement", "Medium movement", "High movement"])

# Map ACC option to example values (you can customize)
ACC_map = {
    "No movement": (5, 5, 20),
    "Little movement": (40, 30, 60),
    "Medium movement": (100, 80, 140),
    "High movement": (250, 200, 350)
}
ACC_x, ACC_y, ACC_z = ACC_map[ACC_option]

if st.button("Predict Stress"):
    # Validate input ranges
    if BVP < -500 or BVP > 1200:
        st.error("BVP value is out of realistic range (-500 - 1200).")
        st.stop()
    if EDA < 0 or EDA > 21:
        st.error("EDA value is out of realistic range (0–20 µS).")
        st.stop()
    if TEMP < 30 or TEMP > 40:
        st.error("Body Temperature value is out of realistic range (30-40°C).")
        st.stop()

    # Map ACC
    ACC_x, ACC_y, ACC_z = ACC_map[ACC_option]

    # Send request
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





