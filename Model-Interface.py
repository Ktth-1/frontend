# frontend.py
import streamlit as st
import requests

st.title("Stress Detection Web App")

BVP = st.number_input("Blood Volume Pulse")
EDA = st.number_input("Electrodermal Activity")
TEMP = st.number_input("Body Temperature")
ACC_option = st.selectbox("Movement activity", ["No movement", "Little active", "Highly active"])

# Map ACC option to example values (you can customize)
ACC_map = {
    "No movement": (0, 0, 0),
    "Little active": (10, 5, 12),
    "Highly active": (30, -6, 55)
}
ACC_x, ACC_y, ACC_z = ACC_map[ACC_option]

if st.button("Predict Stress"):
    # Validate input ranges
    if BVP < 0 or BVP > 3:
        st.error("BVP value is out of realistic range (0–3 V).")
        st.stop()
    if EDA < 0 or EDA > 100:
        st.error("EDA value is out of realistic range (0–100 µS).")
        st.stop()
    if TEMP < 25 or TEMP > 43:
        st.error("Body Temperature value is out of realistic range (25–43°C).")
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


