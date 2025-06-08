# streamlit_login_api.py
import streamlit as st
import pandas as pd

# Load user credentials from Excel
@st.cache_data
def load_credentials():
    try:
        df = pd.read_excel("credentials.xlsx")
        df["username"] = df["username"].astype(str)
        df["password"] = df["password"].astype(str)
        return df
    except Exception as e:
        st.error("Error loading credentials file.")
        st.stop()

# API-like behavior for desktop app
query_params = st.query_params
username = query_params.get("username", [""])[0]
password = query_params.get("password", [""])[0]

st.set_page_config(page_title="Streamlit Login API", layout="centered")
st.title("🔐 Streamlit Login API")

# If called from desktop app with parameters
if username and password:
    df = load_credentials()
    match = df[(df["username"] == username) & (df["password"] == password)]
    
    if not match.empty:
        user_data = match.iloc[0]
        st.json({
            "success": True,
            "username": user_data["username"],
            "role": user_data["role"]
        })
    else:
        st.json({"success": False, "error": "Invalid credentials"})
else:
    st.markdown("""
        ### 🚀 Usage:
        Append credentials to URL like this:
        
        ```
        ?username=admin&password=admin123
        ```
        
        Example:
        [Try Now](?username=admin&password=admin123)
    """)
