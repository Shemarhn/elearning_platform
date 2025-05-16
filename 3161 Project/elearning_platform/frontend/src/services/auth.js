import axios from 'axios';

const API_URL = 'http://localhost:5000/api'; // adjust based on your backend

export const login = async (email, password) => {
  const response = await axios.post(`${API_URL}/auth/login`, { email, password });
  return response.data; // contains token/user info
};

export const signup = async (userData) => {
  const response = await axios.post(`${API_URL}/auth/signup`, userData);
  return response.data;
};

export async function register(name, email, password) {
  const response = await fetch('http://localhost:5000/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password }),
  });
  if (!response.ok) throw new Error('Registration failed');
  return await response.json();
}
