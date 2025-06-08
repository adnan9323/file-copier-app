# streamlit_admin_portal.py

import streamlit as st
import pandas as pd
import requests
import json

# Simulated database (in memory for now)
# You should replace this with a real database like Firebase, Supabase, or a Google Sheet
@st.cache_data

def load_users():
    return pd.DataFrame([
        {"username": "admin", "password": "admin123", "role": "admin"},
        {"username": "user1", "password": "user123", "role": "user"}
    ])

# Save to session for changes during interaction
if "users" not in st.session_state:
    st.session_state.users = load_users()

# Function to check login

def login(username, password):
    df = st.session_state.users
    user = df[(df["username"] == username) & (df["password"] == password)]
    if not user.empty:
        return user.iloc[0].to_dict()
    return None

# Function to add a new user

def add_user(username, password, role):
    st.session_state.users = pd.concat([
        st.session_state.users,
        pd.DataFrame([{"username": username, "password": password, "role": role}])
    ], ignore_index=True)

# Function to delete a user

def delete_user(username):
    st.session_state.users = st.session_state.users[st.session_state.users.username != username]

# --- Streamlit UI ---
st.set_page_config(page_title="Admin Portal", layout="centered")
st.title("🔐 User Management Portal")

# --- Login Section ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

if not st.session_state.logged_in:
    st.subheader("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(username, password)
        if user:
            st.success(f"Welcome {user['username']}")
            st.session_state.logged_in = True
            st.session_state.current_user = user
        else:
            st.error("Invalid credentials")

# --- Admin Panel ---
else:
    user = st.session_state.current_user
    st.write(f"👋 Logged in as **{user['username']}**")

    if user['role'] == 'admin':
        st.subheader("👤 Add New User")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        new_role = st.selectbox("Role", ["user", "admin"])

        if st.button("➕ Add User"):
            if new_username and new_password:
                add_user(new_username, new_password, new_role)
                st.success("User added successfully")
            else:
                st.warning("Username and password cannot be empty")

        st.divider()
        st.subheader("📋 Existing Users")
        df_users = st.session_state.users
        st.dataframe(df_users.drop("password", axis=1), use_container_width=True)

        del_user = st.selectbox("Select user to delete", df_users[df_users.username != 'admin'].username.unique())
        if st.button("🗑️ Delete User"):
            delete_user(del_user)
            st.success(f"User '{del_user}' deleted")

    else:
        st.info("You are logged in as a regular user. No admin privileges.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.experimental_rerun()
