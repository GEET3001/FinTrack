import streamlit as st
import hashlib
from components.utils import load_json, save_json

USER_FILE = "data/users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    users = load_json(USER_FILE)
    for user in users:
        if user["username"] == username and user["password"] == hash_password(password):
            return user
    return None

def user_exists(username):
    users = load_json(USER_FILE)
    return any(user["username"] == username for user in users)

def register_user(username, password, email):
    users = load_json(USER_FILE)
    new_user = {
        "username": username,
        "password": hash_password(password),
        "email": email
    }
    users.append(new_user)
    save_json(USER_FILE, users)

def apply_auth_styling():
    st.markdown("""
    <style>
    .stApp {
        background-color: #2d2d2d;
        color: white;
    }
    
    .stTextInput > div > div > input {
        background-color: #404040 !important;
        color: #ffffff !important;
        border: 1px solid #555 !important;
        border-radius: 5px !important;
    }
    
    .stTextInput > label {
        color: #e0e0e0 !important;
    }
    
    .stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background-color: #45a049 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def login_user():
    apply_auth_styling()
    
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Login"):
            if not username or not password:
                st.warning("Please fill in both username and password.")
            else:
                user = verify_user(username, password)
                if user:
                    st.success("Login successful!")
                    st.session_state.user = user
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    with col2:
        if st.button("New User? Sign Up"):
            st.session_state.page = "signup"
            st.rerun()


def is_strong_password(password):
    has_upper = False
    has_lower = False
    has_special = False
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif not char.isalnum():
            has_special = True
    return has_upper and has_lower and has_special

def signup_user():
    apply_auth_styling()
    
    st.header("Sign Up")
    username = st.text_input("Choose a Username")
    email = st.text_input("Email")
    password = st.text_input("Choose a Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Create Account"):
            if not username or not email or not password or not confirm:
                st.warning("All fields are required.")
            elif not is_strong_password(password):
                st.warning("Password must contain at least one uppercase letter, one lowercase letter, and one special character.")
            elif password != confirm:
                st.warning("Passwords do not match.")
            elif user_exists(username):
                st.warning("Username already exists.")
            else:
                register_user(username, password, email)
                st.success("Account created! Please log in.")
                st.session_state.page = "login"
                st.rerun()
    
    with col2:
        if st.button("Already a user? Login"):
            st.session_state.page = "login"
            st.rerun()
