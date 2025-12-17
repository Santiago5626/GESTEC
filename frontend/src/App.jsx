import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AdminDashboard from './pages/AdminDashboard';
import Login from './pages/Login';
import TechnicalDashboard from './pages/TechnicalDashboard';

// Componente simple para proteger rutas
const ProtectedRoute = ({ children, allowedRole }) => {
  const token = localStorage.getItem('token');
  const userStr = localStorage.getItem('user');

  if (!token || !userStr) {
    return <Navigate to="/" replace />;
  }

  const user = JSON.parse(userStr);

  if (allowedRole && user.role !== allowedRole) {
    // Si intenta acceder a una ruta no autorizada, redirigir a su dashboard correspondiente
    return <Navigate to={user.role === 'admin' ? '/admin' : '/technical'} replace />;
  }

  return children;
};

// Componente para manejar ruta raíz (si ya está logueado, ir a su dashboard)
const RootRedirect = () => {
  const token = localStorage.getItem('token');
  const userStr = localStorage.getItem('user');

  if (token && userStr) {
    const user = JSON.parse(userStr);
    return <Navigate to={user.role === 'admin' ? '/admin' : '/technical'} replace />;
  }
  return <Login />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<RootRedirect />} />

        <Route path="/admin" element={
          <ProtectedRoute allowedRole="admin">
            <AdminDashboard />
          </ProtectedRoute>
        } />

        <Route path="/technical" element={
          <ProtectedRoute allowedRole="technical">
            <TechnicalDashboard />
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
