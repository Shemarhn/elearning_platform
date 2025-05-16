import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function PrivateRoute({ children }) {
  const { user } = useAuth();
  
  // If user is not authenticated, redirect to login
  if (!user) {
    return <Navigate to="/" replace />;
  }

  return children;
}