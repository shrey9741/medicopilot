import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

const MODAL_CONTENT = {
  Settings: {
    title: '⚙️ Settings',
    items: [
      { label: 'Theme', value: 'Clinical Light' },
      { label: 'Language', value: 'English (US)' },
      { label: 'Voice Speed', value: 'Normal (0.9x)' },
      { label: 'FHIR Source', value: 'HAPI R4 Sandbox' },
      { label: 'Session Duration', value: '8 hours (shift)' },
      { label: 'Auto-briefing', value: 'Enabled' },
    ]
  },
  Support: {
    title: '💬 Support',
    items: [
      { label: 'Documentation', value: 'docs.clinicalsentinel.ai' },
      { label: 'Email Support', value: 'support@clinicalsentinel.ai' },
      { label: 'Version', value: 'v2.0.0 (Production)' },
      { label: 'Backend Status', value: '✅ All systems operational' },
      { label: 'FHIR Sandbox', value: '✅ Connected' },
      { label: 'License', value: 'HIPAA Enterprise' },
    ]
  }
};

export default function Sidebar({ activePatientId }) {
  const navigate = useNavigate();
  const location = useLocation();
  const doctor = useAuthStore((s) => s.doctor);
  const logout = useAuthStore((s) => s.logout);
  const [modal, setModal] = useState(null);

  const handleLogout = () => { logout(); navigate('/login'); };

  const navItems = [
    { label: 'Dashboard', icon: 'dashboard', path: '/dashboard' },
    { label: 'Patient Briefing', icon: 'assignment_ind', path: '/dashboard' },
    { label: 'SOAP Generator', icon: 'history_edu', path: '/soap' },
    { label: 'Agent Status', icon: 'smart_toy', path: '/agents' },
  ];

  const isActive = (item) => {
    if (item.label === 'Patient Briefing') return location.pathname.startsWith('/patient/');
    return location.pathname === item.path;
  };

  return (
    <>
      <div style={{
        width: '220px', minWidth: '220px', height: '100vh',
        position: 'fixed', left: 0, top: 0,
        background: '#001d4a',
        display: 'flex', flexDirection: 'column', zIndex: 40,
      }}>
        {/* Brand */}
        <div style={{ padding: '24px 20px 20px' }}>
          <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '15px', color: '#ffffff' }}>Clinical Sentinel</div>
          <div style={{ fontSize: '9px', fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', color: 'rgba(255,255,255,0.4)', marginTop: '3px' }}>Medical AI Copilot</div>
        </div>

        <div style={{ height: '1px', background: 'rgba(255,255,255,0.08)', margin: '0 16px' }} />

        {/* Nav */}
        <nav style={{ flex: 1, padding: '12px 10px', display: 'flex', flexDirection: 'column', gap: '2px' }}>
          {navItems.map((item) => {
            const active = isActive(item);
            return (
              <div
                key={item.label}
                onClick={() => navigate(item.path)}
                style={{
                  display: 'flex', alignItems: 'center', gap: '10px',
                  padding: '10px 12px', borderRadius: '8px', cursor: 'pointer',
                  fontSize: '13px', fontWeight: active ? 700 : 500,
                  color: active ? '#ffffff' : 'rgba(255,255,255,0.55)',
                  background: active ? 'rgba(255,255,255,0.12)' : 'transparent',
                  borderLeft: active ? '3px solid #b0c6ff' : '3px solid transparent',
                  transition: 'all 0.15s',
                }}
                onMouseEnter={(e) => {
                  if (!active) {
                    e.currentTarget.style.background = 'rgba(255,255,255,0.07)';
                    e.currentTarget.style.color = 'rgba(255,255,255,0.85)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!active) {
                    e.currentTarget.style.background = 'transparent';
                    e.currentTarget.style.color = 'rgba(255,255,255,0.55)';
                  }
                }}
              >
                <span className="material-icons-round" style={{ fontSize: '18px' }}>{item.icon}</span>
                {item.label}
              </div>
            );
          })}
        </nav>

        <div style={{ height: '1px', background: 'rgba(255,255,255,0.08)', margin: '0 16px' }} />

        {/* Bottom */}
        <div style={{ padding: '14px 10px' }}>
          <button
            onClick={() => navigate('/dashboard')}
            style={{
              width: '100%', padding: '10px 14px', marginBottom: '16px',
              background: 'rgba(255,255,255,0.12)',
              border: '1px solid rgba(255,255,255,0.15)',
              color: '#fff', borderRadius: '8px',
              fontSize: '13px', fontWeight: 600, cursor: 'pointer',
              display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px',
              transition: 'background 0.15s', fontFamily: 'Inter,sans-serif',
            }}
            onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.2)'}
            onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.12)'}
          >
            <span className="material-icons-round" style={{ fontSize: '16px' }}>add</span>
            New Consultation
          </button>

          {/* Settings + Support */}
          <div style={{ display: 'flex', gap: '8px', marginBottom: '16px', padding: '0 4px' }}>
            {['Settings', 'Support'].map((item) => (
              <div
                key={item}
                onClick={() => setModal(item)}
                style={{
                  flex: 1, padding: '6px 10px', borderRadius: '6px',
                  fontSize: '11px', fontWeight: 500,
                  color: 'rgba(255,255,255,0.45)',
                  cursor: 'pointer', textAlign: 'center',
                  transition: 'all 0.15s',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '4px',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.color = 'rgba(255,255,255,0.8)';
                  e.currentTarget.style.background = 'rgba(255,255,255,0.07)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.color = 'rgba(255,255,255,0.45)';
                  e.currentTarget.style.background = 'transparent';
                }}
              >
                <span className="material-icons-round" style={{ fontSize: '13px' }}>
                  {item === 'Settings' ? 'settings' : 'help_outline'}
                </span>
                {item}
              </div>
            ))}
          </div>

          <div style={{ height: '1px', background: 'rgba(255,255,255,0.08)', marginBottom: '14px' }} />

          {/* Doctor card */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '4px 4px' }}>
            <div style={{
              width: '34px', height: '34px', borderRadius: '50%',
              background: 'linear-gradient(135deg, #3a5ca4, #0d47a1)',
              border: '2px solid rgba(255,255,255,0.2)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              color: '#fff', fontSize: '12px', fontWeight: 700, flexShrink: 0,
            }}>
              {doctor?.name?.split(' ').map(w => w[0]).join('').slice(0, 2) || 'DR'}
            </div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: '12px', fontWeight: 700, color: '#fff', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {doctor?.name || 'Dr. Julian Thorne'}
              </div>
              <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.45)', marginTop: '1px' }}>
                {doctor?.role || 'Chief Medical Officer'}
              </div>
            </div>
            <span
              className="material-icons-round"
              onClick={handleLogout}
              title="Sign out"
              style={{ fontSize: '16px', color: 'rgba(255,255,255,0.35)', cursor: 'pointer', flexShrink: 0, transition: 'color 0.15s' }}
              onMouseEnter={(e) => e.currentTarget.style.color = 'rgba(255,255,255,0.8)'}
              onMouseLeave={(e) => e.currentTarget.style.color = 'rgba(255,255,255,0.35)'}
            >
              logout
            </span>
          </div>
        </div>
      </div>

      {/* Modal */}
      {modal && (
        <div
          onClick={() => setModal(null)}
          style={{
            position: 'fixed', inset: 0, zIndex: 100,
            background: 'rgba(0,0,0,0.4)', backdropFilter: 'blur(4px)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              background: '#fff', borderRadius: '16px', padding: '28px',
              width: '380px', boxShadow: '0 24px 64px rgba(0,0,0,0.2)',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '18px', color: '#191c1e' }}>
                {MODAL_CONTENT[modal].title}
              </h2>
              <span
                className="material-icons-round"
                onClick={() => setModal(null)}
                style={{ fontSize: '20px', color: '#9ca3af', cursor: 'pointer' }}
              >close</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {MODAL_CONTENT[modal].items.map((item) => (
                <div key={item.label} style={{
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  padding: '10px 14px', background: '#f8f9fb', borderRadius: '8px',
                }}>
                  <span style={{ fontSize: '13px', color: '#5a5e6b', fontWeight: 500 }}>{item.label}</span>
                  <span style={{ fontSize: '13px', color: '#191c1e', fontWeight: 600 }}>{item.value}</span>
                </div>
              ))}
            </div>

            <button
              onClick={() => setModal(null)}
              style={{
                width: '100%', marginTop: '20px', padding: '12px',
                background: '#001d4a', color: '#fff', border: 'none',
                borderRadius: '8px', fontSize: '14px', fontWeight: 700,
                cursor: 'pointer', fontFamily: 'Inter,sans-serif',
              }}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
}