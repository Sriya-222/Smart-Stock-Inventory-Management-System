import streamlit as st
from src.lib.api import api_call
import time

st.title("Settings")
st.write("Manage your account settings and preferences.")

user = st.session_state.user

tab1, tab2, tab3 = st.tabs(["Profile", "Preferences", "Notifications"])

with tab1:
    st.subheader("Profile Information")
    st.write("Update your account profile information and avatar.")
    
    with st.container(border=True):
        with st.form("profile_settings"):
            name = st.text_input("Name", value=user.get('name', ''))
            email = st.text_input("Email", value=user.get('email', ''))
            
            avatars = [
                "🐶 Dog", "🐱 Cat", "🐼 Panda", "🦊 Fox", "🐉 Dragon", 
                "🥷 Ninja", "🧙 Wizard", "🦸 Hero", "🧛 Vampire", "🧝 Elf"
            ]
            current_avatar = user.get('avatar', '🐶 Dog')
            if current_avatar not in avatars:
                avatars.append(current_avatar)
                
            avatar = st.selectbox("Choose an Avatar", avatars, index=avatars.index(current_avatar))
            
            if st.form_submit_button("Save Changes", type="primary"):
                try:
                    data = api_call('/auth/profile', method='PUT', data={
                        'id': user.get('id'),
                        'name': name,
                        'email': email,
                        'avatar': avatar
                    })
                    st.session_state.user = data['user']
                    st.success("Profile saved successfully!")
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to update profile: {str(e)}")

    st.markdown("---")
    st.subheader("Danger Zone")
    st.write("Permanently delete your account and all of its contents.")
    if st.button("Delete Account"):
        st.error("Account deletion requested. Please contact an admin.")

with tab2:
    st.subheader("General Preferences")
    
    with st.container(border=True):
        with st.form("general_prefs"):
            themes = ["System", "Light", "Dark"]
            current_theme = user.get('theme', 'System')
            if current_theme not in themes: themes.append(current_theme)
            
            theme = st.selectbox("Theme", themes, index=themes.index(current_theme))
            language = st.selectbox("Language", ["English (US)", "English (UK)", "Español", "Français"])
            
            if st.form_submit_button("Save Preferences", type="primary"):
                try:
                    data = api_call('/auth/profile', method='PUT', data={
                        'id': user.get('id'),
                        'theme': theme
                    })
                    st.session_state.user = data['user']
                    
                    if theme == "Dark":
                        st.info("Theme updated. Please use the Streamlit menu (Top Right) > Settings to physically switch Streamlit to Dark Mode!")
                    else:
                        st.info("Theme updated. Please use the Streamlit menu (Top Right) > Settings to physically switch Streamlit to Light Mode!")
                        
                except Exception as e:
                    st.error(f"Failed to update preferences: {str(e)}")

with tab3:
    st.subheader("Notification Settings")
    st.write("Configure how you receive system alerts and updates.")
    
    with st.container(border=True):
        with st.form("notification_prefs"):
            email_notif = st.checkbox("Email Notifications (Daily Summary)", value=True)
            order_alerts = st.checkbox("Order Alerts", value=True)
            marketing = st.checkbox("Marketing Communications", value=False)
            
            if st.form_submit_button("Save Notifications", type="primary"):
                st.success("Notification settings saved successfully")
