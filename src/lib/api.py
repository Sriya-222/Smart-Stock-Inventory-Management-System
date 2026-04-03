import requests
import streamlit as st

API_URL = 'http://localhost:5000/api'

def api_call(endpoint, method='GET', data=None, params=None):
    headers = {'Content-Type': 'application/json'}
    
    # Check if user is logged in
    if 'token' in st.session_state and st.session_state.token:
        headers['Authorization'] = f"Bearer {st.session_state.token}"
    
    url = f"{API_URL}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")
            
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            resp_data = response.json()
        else:
            resp_text = response.text
            raise Exception(f"Unexpected response from server: {resp_text[:100]}")
            
        if not response.ok:
            error_msg = resp_data.get('message') or resp_data.get('error') or 'API Request Failed'
            raise Exception(error_msg)
            
        return resp_data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {str(e)}")
