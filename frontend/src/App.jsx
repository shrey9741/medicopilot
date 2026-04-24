import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/authStore';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import PatientBriefing from './pages/PatientBriefing';
import SOAPEditor from './pages/SOAPEditor';
import AgentTrace from './pages/AgentTrace';

const PrivateRoute = ({ children }) => {
  const token = useAuthStore((s) => s.token);
  return token ? children : <Navigate to="/login" replace />;
};

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        <Route path="/patient/:id" element={<PrivateRoute><PatientBriefing /></PrivateRoute>} />
        <Route path="/soap" element={<PrivateRoute><SOAPEditor /></PrivateRoute>} />
        <Route path="/agents" element={<PrivateRoute><AgentTrace /></PrivateRoute>} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}