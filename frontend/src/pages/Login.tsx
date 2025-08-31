import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  IconButton,
  InputAdornment,
  Container,
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  BusinessCenter,
} from '@mui/icons-material';
import { useSnackbar } from 'notistack';
import useAuthStore from '@store/authStore';
import authService from '@services/auth/authService';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const setAuth = useAuthStore((state) => state.setAuth);
  
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.username || !formData.password) {
      setError('이메일과 비밀번호를 입력해주세요.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await authService.login(formData);
      
      // Get user info
      const user = await authService.getCurrentUser();
      
      // Set auth state
      setAuth(user, response.access_token, response.refresh_token || response.access_token);
      
      enqueueSnackbar('로그인 성공!', { variant: 'success' });
      navigate('/dashboard');
    } catch (err: any) {
      console.error('Login error:', err);
      if (err.response?.status === 401) {
        setError('이메일 또는 비밀번호가 올바르지 않습니다.');
      } else {
        setError('로그인 중 오류가 발생했습니다. 다시 시도해주세요.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = (role: 'admin' | 'rep') => {
    const credentials = {
      admin: { username: 'admin@startup.com', password: 'admin123' },
      rep: { username: 'rep@startup.com', password: 'rep123' },
    };
    
    setFormData(credentials[role]);
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Paper
          elevation={3}
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: '100%',
          }}
        >
          <BusinessCenter sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
          
          <Typography component="h1" variant="h4" gutterBottom>
            Startup Manager
          </Typography>
          
          <Typography variant="body2" color="text.secondary" gutterBottom>
            AI Business Automation Platform
          </Typography>

          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3, width: '100%' }}>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <TextField
              fullWidth
              label="이메일"
              name="username"
              type="email"
              value={formData.username}
              onChange={handleChange}
              margin="normal"
              required
              autoComplete="email"
              autoFocus
            />

            <TextField
              fullWidth
              label="비밀번호"
              name="password"
              type={showPassword ? 'text' : 'password'}
              value={formData.password}
              onChange={handleChange}
              margin="normal"
              required
              autoComplete="current-password"
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={isLoading}
            >
              {isLoading ? '로그인 중...' : '로그인'}
            </Button>

            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="text.secondary" align="center">
                테스트 계정
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                <Button
                  size="small"
                  variant="outlined"
                  fullWidth
                  onClick={() => handleDemoLogin('admin')}
                >
                  Admin
                </Button>
                <Button
                  size="small"
                  variant="outlined"
                  fullWidth
                  onClick={() => handleDemoLogin('rep')}
                >
                  Rep
                </Button>
              </Box>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default Login;