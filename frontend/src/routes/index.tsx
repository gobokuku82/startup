import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from '@components/layout/MainLayout';
import ProtectedRoute from '@components/common/ProtectedRoute';
import LoadingSpinner from '@components/common/LoadingSpinner';

// Lazy load pages
const Login = lazy(() => import('@pages/Login'));
const Dashboard = lazy(() => import('@pages/Dashboard'));
const Analytics = lazy(() => import('@pages/Analytics'));
const Clients = lazy(() => import('@pages/Clients'));
const Documents = lazy(() => import('@pages/Documents'));
const Schedule = lazy(() => import('@pages/Schedule'));
const Compliance = lazy(() => import('@pages/Compliance'));

const AppRoutes: React.FC = () => {
  return (
    <Suspense fallback={<LoadingSpinner fullScreen />}>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        
        {/* Protected Routes */}
        <Route element={<ProtectedRoute />}>
          <Route element={<MainLayout />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/clients" element={<Clients />} />
            <Route path="/documents" element={<Documents />} />
            <Route path="/schedule" element={<Schedule />} />
            <Route path="/compliance" element={<Compliance />} />
          </Route>
        </Route>
        
        {/* 404 */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Suspense>
  );
};

export default AppRoutes;