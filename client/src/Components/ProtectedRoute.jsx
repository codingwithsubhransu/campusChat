import {React, useState, useEffect} from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import isAuthenticated from './api/isAuthenticated'
import { useAuth } from './AuthContext';

const ProtectedRoute = () => {
    
    const { user, loading } = useAuth();
    
    if (loading) {
      return <div className='h-screen flex justify-center items-center text-white'> Checking Authentication....</div>;
    }

  return user ? <Outlet /> : <Navigate to="/login" replace />;
}

export default ProtectedRoute;