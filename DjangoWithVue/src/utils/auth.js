import axios from './axios';

export async function refreshAccessToken() {
  const refresh = localStorage.getItem('refresh');
  if (!refresh) return null;

  try {
    const res = await axios.post('/api/token/refresh/', { refresh });
    const newAccess = res.data.access;
    localStorage.setItem('access', newAccess);
    return newAccess;
  } catch (err) {
    console.error('Refresh failed', err);
    return null;
  }
}
