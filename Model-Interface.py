# frontend.py
import streamlit as st
import requests

st.title("Stress Detection Web App")

BVP = st.number_input("Blood Volume Pulse - (-500 - 1200)")
EDA = st.number_input("Electrodermal Activity (µS)")
TEMP = st.number_input("Body Temperature (°C)")
ACC_option = st.selectbox("Movement activity", ["No movement", "Little movement", "Medium movement", "High movement"])

# Map ACC option to example values (you can customize)
ACC_map = {
    "No movement":        (2, -3, 12),    # magnitude ≈ 12
    "Little movement":    (25, 10, 45),   # magnitude ≈ 52
    "Medium movement":    (55, -20, 85),  # magnitude ≈ 102
    "High movement":      (110, -60, 180) # magnitude ≈ 215
}

ACC_x, ACC_y, ACC_z = ACC_map[ACC_option]

if st.button("Predict Stress"):

    # Validate input ranges
    if BVP < -500 or BVP > 1200:
        st.error("BVP value is out of realistic range (-500 - 1200).")
        st.stop()
    if EDA < 0 or EDA > 20:
        st.error("EDA value is out of realistic range (0–20 µS).")
        st.stop()
    if TEMP < 30 or TEMP > 40:
        st.error("Body Temperature value is out of realistic range (30-40°C).")
        st.stop()

    payload = {
        "BVP": BVP,
        "EDA": EDA,
        "TEMP": TEMP,
        "ACC_x": ACC_x,
        "ACC_y": ACC_y,
        "ACC_z": ACC_z
    }

    response = requests.post(
        "https://nonpestilent-mercedez-mousey.ngrok-free.dev/predict",
        json=payload
    )

    # Handle API response safely
    try:
        data = response.json()
    except:
        st.error("API did not return valid JSON.")
        st.text(response.text)
        st.stop()

    if response.status_code == 200:
        st.write("Predicted Stress Status:", data.get("prediction"))
    else:
        st.error(f"API Error: {response.status_code}")
        st.text(response.text)










