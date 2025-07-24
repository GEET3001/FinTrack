import streamlit as st
import hashlib
from db import Database

class AuthManager:
    def __init__(self, db=None):
        self.db = db or Database()

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_user(self, username, password):
        pw_hash = self.hash_password(password)
        user = self.db.fetchone("SELECT * FROM users WHERE username=%s AND password=%s", (username, pw_hash))
        return user

    def user_exists(self, username):
        user = self.db.fetchone("SELECT id FROM users WHERE username=%s", (username,))
        return user is not None

    def register_user(self, username, password, email):
        pw_hash = self.hash_password(password)
        self.db.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            (username, pw_hash, email)
        )

    @staticmethod
    def is_strong_password(password):
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_special = any(not c.isalnum() for c in password)
        return has_upper and has_lower and has_special

    @staticmethod
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

    def login_user(self):
        self.apply_auth_styling()
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("Login"):
                if not username or not password:
                    st.warning("Please fill in both username and password.")
                else:
                    user = self.verify_user(username, password)
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

    def signup_user(self):
        self.apply_auth_styling()
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
                elif not self.is_strong_password(password):
                    st.warning("Password must contain at least one uppercase letter, one lowercase letter, and one special character.")
                elif password != confirm:
                    st.warning("Passwords do not match.")
                elif self.user_exists(username):
                    st.warning("Username already exists.")
                else:
                    self.register_user(username, password, email)
                    st.success("Account created! Please log in.")
                    st.session_state.page = "login"
                    st.rerun()
        with col2:
            if st.button("Already a user? Login"):
                st.session_state.page = "login"
                st.rerun()
