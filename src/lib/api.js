const API_URL = 'http://localhost:5000/api';

export const apiCall = async (endpoint, options = {}) => {
  const token = localStorage.getItem('token');

  const headers = new Headers(options.headers || {});
  headers.set('Content-Type', 'application/json');

  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers
  });

  const contentType = response.headers.get("content-type");
  let data;
  if (contentType && contentType.indexOf("application/json") !== -1) {
    data = await response.json();
  } else {
    const textData = await response.text();
    throw new Error(`Unexpected response from server: ${textData.substring(0, 100)}... Please make sure your backend is running the latest code.`);
  }

  if (!response.ok) {
    throw new Error(data.message || data.error || 'API Request Failed');
  }

  return data;
};