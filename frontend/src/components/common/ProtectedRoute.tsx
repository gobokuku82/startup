import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import useAuthStore from '@store/authStore';
import LoadingSpinner from './LoadingSpinner';

const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuthStore();

  if (isLoading) {
    return <LoadingSpinner fullScreen message="인증 확인 중..." />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;