import streamlit as st
import time
from src.lib.api import api_call

st.title("Create account")
st.write("Get started with StockWise")

with st.form("signup_form"):
    name = st.text_input("Full Name", placeholder="Enter your name")
    email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="••••••••••")
    role = st.selectbox("Account Role", options=[("user", "User (Buy Products)"), ("admin", "Admin (Manage Products)")], format_func=lambda x: x[1])
    
    avatar = st.selectbox("Choose an Avatar", [
        "🐶 Dog", "🐱 Cat", "🐼 Panda", "🦊 Fox", "🐉 Dragon", 
        "🥷 Ninja", "🧙 Wizard", "🦸 Hero", "🧛 Vampire", "🧝 Elf"
    ])
    
    submit = st.form_submit_button("Create Account")

if submit:
    if not name or not email or not password:
        st.error("Please fill in all fields.")
    else:
        try:
            with st.spinner("Creating account..."):
                data = api_call('/auth/register', method='POST', data={
                    'name': name,
                    'email': email,
                    'password': password,
                    'role': role[0],
                    'avatar': avatar
                })
            
            st.session_state.token = data.get('token')
            st.session_state.user = data.get('user')
            
            st.success("Account created successfully!")
            time.sleep(0.5)
            st.rerun()
        except Exception as e:
            st.error(str(e))

st.markdown("---")
st.markdown("Already have an account? Navigate to the **Login** page.")
