# streamlit_login_api.py

import streamlit as st

# --- Hardcoded Users ---
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "user123", "role": "user"},
    "ammar": {"password": "secret", "role": "user"},
}

# --- Streamlit App ---
st.set_page_config(page_title="Login API")
st.title("🔐 Streamlit Login API")
st.write("This is a simulated login API for desktop applications.")

# ✅ Updated method to get query params
query_params = st.query_params
username = query_params.get("username", "")
password = query_params.get("password", "")

if username and password:
    if username in USERS and USERS[username]["password"] == password:
        st.json({"success": True, "user": username, "role": USERS[username]["role"]})
    else:
        st.json({"success": False, "error": "Invalid credentials"})
else:
    st.info("Pass `?username=yourname&password=yourpass` in URL.")
