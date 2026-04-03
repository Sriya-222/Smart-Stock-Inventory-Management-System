import streamlit as st
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="StockWise",
    page_icon="📦",
    layout="wide"
)

# Initialize session state for user authentication
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None

# Custom CSS for styling (Cards, Buttons, Spacing)
st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    h1, h2, h3 { color: var(--text-color); font-family: 'Inter', sans-serif; font-weight: 700; }
    .stButton>button { border-radius: 8px; transition: all 0.2s ease-in-out; font-weight: 600; padding: 0.5rem 1rem; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    /* Glass card effect for containers using the data-testid */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background: rgba(255, 255, 255, 0.03); 
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
</style>
""", unsafe_allow_html=True)

def logout():
    st.session_state.user = None
    st.session_state.token = None
    st.rerun()

# Setup Streamlit navigation
login_page = st.Page("pages/1_Login.py", title="Login", icon="🔑")
signup_page = st.Page("pages/2_SignUp.py", title="Sign Up", icon="📝")

dashboard_page = st.Page("pages/3_Dashboard.py", title="Dashboard", icon="📊")
products_page = st.Page("pages/4_Products.py", title="Products", icon="📦")
analytics_page = st.Page("pages/5_Analytics.py", title="Analytics", icon="📈")
alerts_page = st.Page("pages/6_Alerts.py", title="Alerts", icon="🔔")
settings_page = st.Page("pages/7_Settings.py", title="Settings", icon="⚙️")

if st.session_state.token is None:
    pg = st.navigation({
        "Authentication": [login_page, signup_page]
    })
else:
    # Sidebar logout
    with st.sidebar:
        user_avatar = st.session_state.user.get('avatar', '👤')
        st.write(f"### {user_avatar}")
        st.write(f"Welcome, **{st.session_state.user.get('name', 'User')}**")
        st.write(f"Role: {st.session_state.user.get('role', 'user').capitalize()}")
        if st.button("Logout", icon="🚪"):
            logout()
            
    # Authenticated navigation
    pages = {
        "Main Menu": [dashboard_page, products_page, analytics_page, alerts_page, settings_page]
    }
    pg = st.navigation(pages)

pg.run()
