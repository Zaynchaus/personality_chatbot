import streamlit as st
import requests
import re
from chatbot2 import chat_ui

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Login & Signup System", layout="centered")

# ---------------- SESSION STATE FIX ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False   # ✔ FIXED

if "user_email" not in st.session_state:
    st.session_state.user_email = ""     # ✔ FIXED


def dashboard():


    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()
    chat_ui()


def validate_email(email):
    pattern = r'^[A-Za-z][A-Za-z0-9._]*@[A-Za-z]+\.[A-Za-z.]+'
    return bool(re.match(pattern, email)) and not re.search(r'@\.', email)


def validate_password(password):
    if len(password) < 6 or len(password) > 16:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[@#$%^&*!]', password):
        return False
    return True


# ---------------- MAIN PAGE LOGIC ------------------

# ✔ THIS FIXES THE REDIRECT COMPLETELY
if st.session_state.logged_in:
    dashboard()
else:
    st.title(" User Login & Signup System ")

    menu = ["Login", "Sign Up", "Forgot Password"]
    choice = st.sidebar.selectbox("Menu", menu)

    # ---------------- SIGNUP -------------------

    if choice == "Sign Up":
        st.subheader("Create a New Account")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up"):

            if not validate_email(email):
                st.error(" Invalid email format.")
            elif not validate_password(password):
                st.warning(" Weak password.")
            elif password != confirm_password:
                st.error(" Passwords do not match.")
            else:
                payload = {"email": email, "password": password}
                response = requests.post(f"{API_URL}/signup", json=payload)

                if response.status_code == 200:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error(response.json()['detail'])

    # ---------------- LOGIN ---------------------

    elif choice == "Login":
        st.subheader("Login to Your Account")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if not validate_email(email):
                st.error(" Invalid email format.")
            elif not validate_password(password):
                st.warning(" Invalid password format.")
            else:
                payload = {"email": email, "password": password}
                response = requests.post(f"{API_URL}/login", json=payload)

                if response.status_code == 200:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error(" Incorrect email or password.")

    # --------------- RESET PASSWORD ---------------

    elif choice == "Forgot Password":
        st.subheader("Reset Your Password")

        email = st.text_input("Registered Email")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Reset Password"):

            if not validate_email(email):
                st.error(" Invalid email format.")
            elif not validate_password(new_pass):
                st.warning(" Weak password.")
            else:
                payload = {"email": email, "new_password": new_pass}
                response = requests.post(f"{API_URL}/reset_password", json=payload)

                if response.status_code == 200:
                    st.success(" Password updated successfully!")
                else:
                    st.error(" Error resetting password")