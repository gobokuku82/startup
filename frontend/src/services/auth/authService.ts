import { api } from '@services/api/apiClient';
import { LoginCredentials, AuthResponse, User } from '@types/index';

class AuthService {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await api.post<AuthResponse>('/api/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    return response.data;
  }

  async logout(): Promise<void> {
    try {
      await api.post('/api/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    }
  }

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/api/auth/me');
    return response.data;
  }

  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/api/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  }

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await api.patch<User>('/api/auth/profile', data);
    return response.data;
  }

  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    await api.post('/api/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  }
}

export default new AuthService();