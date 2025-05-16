import { Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import CoursePage from './pages/CoursePage';
import RegisterPage from './pages/RegisterPage';
import Calendar from './pages/Calendar';
import Assignments from './pages/Assignments';
import Forums from './pages/Forums';
import Reports from './pages/Reports';
import PrivateRoute from './components/PrivateRoute';  

function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      
      {/* Protected Routes */}
      <Route path="/dashboard" element={
        <PrivateRoute>
          <Dashboard />
        </PrivateRoute>
      } />
      
      <Route path="/courses/:id" element={
        <PrivateRoute>
          <CoursePage />
        </PrivateRoute>
      } />
      
      <Route path="/courses/:id/calendar" element={
        <PrivateRoute>
          <Calendar />
        </PrivateRoute>
      } />
      
      <Route path="/courses/:id/assignments" element={
        <PrivateRoute>
          <Assignments />
        </PrivateRoute>
      } />
      
      <Route path="/courses/:id/forums" element={
        <PrivateRoute>
          <Forums />
        </PrivateRoute>
      } />
      
      <Route path="/reports" element={
        <PrivateRoute>
          <Reports />
        </PrivateRoute>
      } />
    </Routes>
  );
}

export default App;

