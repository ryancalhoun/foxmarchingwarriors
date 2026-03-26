import jwt from 'jsonwebtoken'
import { useCookies } from '@vueuse/integrations/useCookies'

const cookies = useCookies(['auth_token']);

export function useAuth() {
  function getEmail() {
    const token = cookies.get('auth_token');
    if(token) {
      return jwt.decode(token).email;
    }
  }

  function logout() {
    cookies.remove('auth_token');
  }

  async function submit(params) {
    const response = await fetch('api/authenticate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams(params),
    });

    if(response.ok) {
      const token = (await response.json()).auth;
      cookies.set('auth_token', token);
    } else {
      throw new Error('Authentication error');
    }
  }

  return { getEmail, logout, submit };
}
