import { PUBLIC_API_URL } from '$env/static/public';


function authHeaders() {
  return { Authorization: `Bearer ${getToken()}` };
}

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

export async function fetchMyTasks() {
  const res = await fetch(`${PUBLIC_API_URL}/tasks/mine`, {
    headers: authHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch tasks');
  return res.json();
}

export async function fetchTheirTasks() {
  const res = await fetch(`${PUBLIC_API_URL}/tasks/theirs`, {
    headers: authHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch tasks');
  return res.json();
}

export async function createTask(title) {
  const res = await fetch(`${PUBLIC_API_URL}/tasks/`, {
    method: 'POST',
    headers: {
      ...authHeaders(),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title })
  });
  if (!res.ok) throw new Error('Failed to create task');
  return res.json();
}

export async function claimTask(taskId) {
  const res = await fetch(`${PUBLIC_API_URL}/tasks/${taskId}/claim`, {
    method: 'PATCH',
    headers: authHeaders()
  });
  if (!res.ok) throw new Error('Failed to claim task');
  return res.json();
}

export async function markDone(taskId) {
  const res = await fetch(`${PUBLIC_API_URL}/tasks/${taskId}/done`, {
    method: 'PATCH',
    headers: authHeaders()
  });
  if (!res.ok) throw new Error('Failed to mark done');
  return res.json();
}
