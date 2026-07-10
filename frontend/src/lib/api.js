import { PUBLIC_API_URL } from '$env/static/public';

export async function login(username, password) {
  const body = new URLSearchParams({ username, password });
  const res = await fetch(`${PUBLIC_API_URL}/auth/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body
  });
  if (!res.ok) throw new Error('Login failed');
  const data = await res.json();
  localStorage.setItem('token', data.access_token);
  return data.access_token;
}

export function getToken() {
  return localStorage.getItem('token');
}

export function logout() {
  localStorage.removeItem('token');
}
