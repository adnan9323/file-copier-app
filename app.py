import streamlit as st
import pandas as pd

# --- Hardcoded Users ---
USERS = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "user1", "password": "user123", "role": "user"},
    {"username": "ammar", "password": "secret", "role": "user"}
]

# --- Login Function ---
def login(username, password):
    for user in USERS:
        if user["username"] == username and user["password"] == password:
            return user
    return None

# --- Streamlit UI ---
st.set_page_config(page_title="User Login Portal", layout="centered")
st.title("🔐 Hardcoded User Login Portal")

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# --- Login Form ---
if not st.session_state.logged_in:
    st.subheader("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = user
            st.success(f"Welcome, {user['username']}!")
        else:
            st.error("❌ Invalid username or password")

# --- Logged In Area ---
else:
    user = st.session_state.current_user
    st.write(f"👋 Logged in as **{user['username']}** (Role: `{user['role']}`)")

    if user["role"] == "admin":
        st.subheader("🧑‍💼 Admin Controls (Read-Only)")
        df = pd.DataFrame(USERS).drop("password", axis=1)
        st.dataframe(df, use_container_width=True)
        st.markdown("ℹ️ User management is hardcoded. Modify the code to update users.")

    else:
        st.info("✅ You are logged in as a standard user.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.experimental_rerun()
