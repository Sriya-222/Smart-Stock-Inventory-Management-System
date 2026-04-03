import streamlit as st
import time
from src.lib.api import api_call

st.title("Sign in to StockWise")
st.write("Enter your credentials to continue")

with st.form("login_form"):
    email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="••••••••••")
    submit = st.form_submit_button("Sign In")

if submit:
    if not email or not password:
        st.error("Please fill in all fields.")
    else:
        try:
            with st.spinner("Signing in..."):
                data = api_call('/auth/login', method='POST', data={'email': email, 'password': password})
            
            st.session_state.token = data.get('token')
            st.session_state.user = data.get('user')
            
            st.success("Logged in successfully!")
            time.sleep(0.5)
            st.rerun()
        except Exception as e:
            st.error(str(e))

st.markdown("---")
st.markdown("Don't have an account? Navigate to the **Sign Up** page.")
