# streamlit_login_api.py

import streamlit as st
import json

# --- Hardcoded Users ---
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "user123", "role": "user"},
    "ammar": {"password": "secret", "role": "user"},
}

# API Simulation
st.set_page_config(page_title="Login API")

st.title("🔐 Streamlit Login API")
st.write("This is a simulated login API for desktop applications.")

# Accept GET or POST from the desktop app
query_params = st.experimental_get_query_params()
username = query_params.get("username", [""])[0]
password = query_params.get("password", [""])[0]

if username and password:
    if username in USERS and USERS[username]["password"] == password:
        st.json({"success": True, "user": username, "role": USERS[username]["role"]})
    else:
        st.json({"success": False, "error": "Invalid credentials"})
else:
    st.info("Pass `?username=yourname&password=yourpass` in URL.")
