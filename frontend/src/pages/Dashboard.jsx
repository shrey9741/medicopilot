import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

const PATIENTS = [
  {
    id: 'P001', time: '08:15', timeAlert: false,
    name: 'Elena Rodriguez', meta: 'F 64y · Case #MS-9920',
    condition: 'Post-Op Cardiology',
    vitals: [{ label: '112 bpm', color: '#ba1a1a', bg: '#ffdad6' }, { label: '138/88', color: '#9b6000', bg: '#ffecd3' }],
    status: 'briefing', statusLabel: 'Briefing Ready',
    status2: 'pending', status2Label: 'Chart Review Pending',
  },
  {
    id: 'P002', time: '09:00', timeAlert: true,
    name: 'Marcus Chen', meta: 'M 42y · Case #MS-4412',
    condition: 'Type 2 Diabetes',
    vitals: [{ label: 'High Glucose', color: '#ba1a1a', bg: '#ffdad6' }, { label: 'A1C 8.4%', color: '#9b6000', bg: '#ffecd3' }],
    status: 'anomaly', statusLabel: '⚠ Anomaly Detected',
  },
  {
    id: 'P003', time: '09:30', timeAlert: false,
    name: 'Sarah Miller', meta: 'F 29y · Case #MS-1102',
    condition: 'Prenatal Check-up Wk 24',
    vitals: [{ label: 'All Stable', color: '#1a7a45', bg: '#d9f0e4' }],
    status: 'briefing', statusLabel: 'Briefing Ready',
  },
  {
    id: 'P004', time: '10:15', timeAlert: false,
    name: 'James Wilson', meta: 'M 72y · Case #MS-8831',
    condition: 'CKD Review',
    vitals: [{ label: 'eGFR 45', color: '#9b6000', bg: '#ffecd3' }, { label: 'K+ 4.8', color: '#9b6000', bg: '#ffecd3' }],
    status: 'waiting', statusLabel: 'Awaiting Intake',
  },
];

const STATUS_STYLES = {
  briefing: { background: '#e8f4fd', color: '#1565c0' },
  anomaly:  { background: '#ffdad6', color: '#ba1a1a' },
  pending:  { background: '#f2f4f6', color: '#5a5e6b' },
  waiting:  { background: '#f2f4f6', color: '#5a5e6b' },
};

export default function Dashboard() {
  const [activeFilter, setActiveFilter] = useState('all');
  const navigate = useNavigate();
  const doctor = useAuthStore((s) => s.doctor);
  const logout = useAuthStore((s) => s.logout);

  const handleLogout = () => { logout(); navigate('/login'); };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'Inter, sans-serif', background: '#f8f9fb' }}>

      {/* ── SIDEBAR ── */}
      <div style={{
        width: '220px', minWidth: '220px', height: '100vh',
        position: 'fixed', left: 0, top: 0,
        background: 'rgba(248,249,251,0.92)',
        backdropFilter: 'blur(14px)',
        display: 'flex', flexDirection: 'column',
        borderRight: 'none', zIndex: 40,
      }}>
        {/* Brand */}
        <div style={{ padding: '24px 20px 16px' }}>
          <div style={{ fontFamily: 'Manrope, sans-serif', fontWeight: 800, fontSize: '15px', color: '#003178' }}>
            Clinical Sentinel
          </div>
          <div style={{ fontSize: '9px', fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', color: '#9ca3af', marginTop: '2px' }}>
            Precision Medicine
          </div>
        </div>

        {/* Nav */}
        <nav style={{ flex: 1, padding: '8px 10px', display: 'flex', flexDirection: 'column', gap: '2px' }}>
          {[
            { label: 'Dashboard', icon: 'dashboard', path: '/dashboard', active: true },
            { label: 'Patient Briefing', icon: 'assignment_ind', path: '/patient/P001' },
            { label: 'SOAP Generator', icon: 'history_edu', path: '/soap' },
            { label: 'Agent Status', icon: 'smart_toy', path: '/agents' },
          ].map((item) => (
            <div
              key={item.label}
              onClick={() => navigate(item.path)}
              style={{
                display: 'flex', alignItems: 'center', gap: '10px',
                padding: '9px 12px', borderRadius: '8px',
                cursor: 'pointer', fontSize: '13px', fontWeight: item.active ? 700 : 500,
                color: item.active ? '#003178' : '#5a5e6b',
                background: item.active ? 'rgba(0,49,120,0.07)' : 'transparent',
                borderRight: item.active ? '2.5px solid #003178' : '2.5px solid transparent',
                transition: 'all 0.15s',
              }}
            >
              <span className="material-icons-round" style={{ fontSize: '18px' }}>{item.icon}</span>
              {item.label}
            </div>
          ))}
        </nav>

        {/* Bottom */}
        <div style={{ padding: '14px' }}>
          <button
            onClick={() => navigate('/patient/P001')}
            style={{
              width: '100%', padding: '10px 14px', marginBottom: '12px',
              background: 'linear-gradient(135deg, #003178, #0d47a1)',
              color: '#fff', border: 'none', borderRadius: '8px',
              fontSize: '13px', fontWeight: 600, cursor: 'pointer',
              display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px',
              fontFamily: 'Inter, sans-serif',
            }}
          >
            <span className="material-icons-round" style={{ fontSize: '16px' }}>add</span>
            New Consultation
          </button>

          {/* Doctor card */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '8px 6px' }}>
            <div style={{
              width: '32px', height: '32px', borderRadius: '50%',
              background: 'linear-gradient(135deg, #003178, #0d47a1)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              color: '#fff', fontSize: '12px', fontWeight: 700, flexShrink: 0,
            }}>
              {doctor?.name?.split(' ').map(w => w[0]).join('').slice(0, 2) || 'DR'}
            </div>
            <div style={{ minWidth: 0 }}>
              <div style={{ fontSize: '12px', fontWeight: 700, color: '#191c1e', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {doctor?.name || 'Dr. Julian Thorne'}
              </div>
              <div style={{ fontSize: '10px', color: '#9ca3af' }}>Chief Medical Officer</div>
            </div>
          </div>

          <div
            onClick={handleLogout}
            style={{ fontSize: '11px', color: '#9ca3af', cursor: 'pointer', textAlign: 'center', marginTop: '8px' }}
          >
            Sign out
          </div>
        </div>
      </div>

      {/* ── MAIN ── */}
      <div style={{ marginLeft: '220px', flex: 1, display: 'flex', flexDirection: 'column' }}>

        {/* TOP HEADER */}
        <div style={{
          position: 'sticky', top: 0, zIndex: 30,
          background: 'rgba(255,255,255,0.92)', backdropFilter: 'blur(14px)',
          borderBottom: '1px solid #f2f4f6',
          display: 'flex', alignItems: 'center', padding: '0 24px', height: '56px', gap: '16px',
        }}>
          <div style={{ fontFamily: 'Manrope, sans-serif', fontWeight: 800, fontSize: '15px', color: '#003178', whiteSpace: 'nowrap' }}>
            Clinical Sentinel
          </div>

          {/* Tabs */}
          <div style={{ display: 'flex', gap: '0' }}>
            {['Dashboard', 'Active Cases', 'Alerts', 'Schedule'].map((tab, i) => (
              <div key={tab} style={{
                padding: '0 14px', height: '56px', display: 'flex', alignItems: 'center',
                fontSize: '13px', fontWeight: i === 1 ? 700 : 500,
                color: i === 1 ? '#003178' : '#9ca3af',
                borderBottom: i === 1 ? '2.5px solid #003178' : '2.5px solid transparent',
                cursor: 'pointer', whiteSpace: 'nowrap',
              }}>{tab}</div>
            ))}
          </div>

          {/* Search */}
          <div style={{ flex: 1, position: 'relative', maxWidth: '280px', marginLeft: 'auto' }}>
            <span className="material-icons-round" style={{
              position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)',
              fontSize: '16px', color: '#9ca3af',
            }}>search</span>
            <input
              placeholder="Search electronic health records..."
              style={{
                width: '100%', padding: '7px 12px 7px 34px',
                background: '#f2f4f6', border: 'none', borderRadius: '8px',
                fontSize: '12px', fontFamily: 'Inter, sans-serif',
                color: '#191c1e', outline: 'none',
              }}
            />
          </div>

          {/* Emergency */}
          <button style={{
            padding: '7px 14px', background: '#ba1a1a', color: '#fff',
            border: 'none', borderRadius: '8px', fontSize: '11px',
            fontWeight: 700, cursor: 'pointer', whiteSpace: 'nowrap',
            display: 'flex', alignItems: 'center', gap: '5px',
          }}>
            <span className="material-icons-round" style={{ fontSize: '14px' }}>bolt</span>
            Emergency Mode
          </button>

          <span className="material-icons-round" style={{ fontSize: '22px', color: '#9ca3af', cursor: 'pointer' }}>notifications</span>
          <span className="material-icons-round" style={{ fontSize: '22px', color: '#9ca3af', cursor: 'pointer' }}>account_circle</span>
        </div>

        {/* PAGE CONTENT */}
        <div style={{ flex: 1, padding: '24px', display: 'grid', gridTemplateColumns: '1fr 260px', gap: '20px' }}>

          {/* LEFT — main content */}
          <div>
            {/* Page header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '20px' }}>
              <div>
                <div style={{ fontSize: '12px', color: '#9ca3af', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Monday, April 23, 2026
                </div>
                <h1 style={{ fontFamily: 'Manrope, sans-serif', fontWeight: 800, fontSize: '28px', color: '#191c1e', marginTop: '2px' }}>
                  Clinical Overview
                </h1>
              </div>
              <div style={{ display: 'flex', gap: '10px' }}>
                {[
                  { icon: 'circle', iconColor: '#1a7a45', label: '12 Patients Today' },
                  { icon: 'schedule', iconColor: '#003178', label: 'Next: 09:30 AM' },
                ].map((b) => (
                  <div key={b.label} style={{
                    display: 'flex', alignItems: 'center', gap: '6px',
                    padding: '6px 12px', background: '#fff',
                    borderRadius: '8px', fontSize: '12px', fontWeight: 600, color: '#191c1e',
                    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
                  }}>
                    <span className="material-icons-round" style={{ fontSize: '14px', color: b.iconColor }}>{b.icon}</span>
                    {b.label}
                  </div>
                ))}
              </div>
            </div>

            {/* Filter tabs */}
            <div style={{ display: 'flex', gap: '4px', marginBottom: '16px' }}>
              {[
                { key: 'all', label: 'All Appointments' },
                { key: 'critical', label: 'Critical Only' },
                { key: 'followup', label: 'Follow-ups' },
                { key: 'completed', label: 'Completed' },
              ].map((f) => (
                <button
                  key={f.key}
                  onClick={() => setActiveFilter(f.key)}
                  style={{
                    padding: '7px 16px', border: 'none', borderRadius: '6px',
                    fontSize: '12px', fontWeight: 600, cursor: 'pointer',
                    background: activeFilter === f.key ? '#003178' : 'transparent',
                    color: activeFilter === f.key ? '#fff' : '#9ca3af',
                    transition: 'all 0.15s',
                    borderBottom: activeFilter === f.key ? 'none' : '2px solid transparent',
                  }}
                >{f.label}</button>
              ))}
            </div>

            {/* Table */}
            <div style={{ background: '#fff', borderRadius: '12px', overflow: 'hidden', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
              {/* Table header */}
              <div style={{
                display: 'grid', gridTemplateColumns: '80px 1fr 160px 180px 60px',
                padding: '10px 20px', background: '#f8f9fb',
                fontSize: '10px', fontWeight: 700, textTransform: 'uppercase',
                letterSpacing: '0.08em', color: '#9ca3af',
              }}>
                <span>Time</span>
                <span>Patient Details</span>
                <span>Vitals & Status</span>
                <span>AI Sentinel Status</span>
                <span>Actions</span>
              </div>

              {/* Rows */}
              {PATIENTS.map((p, i) => (
                <div
                  key={p.id}
                  onClick={() => navigate(`/patient/${p.id}`)}
                  style={{
                    display: 'grid', gridTemplateColumns: '80px 1fr 160px 180px 60px',
                    padding: '16px 20px', cursor: 'pointer',
                    borderTop: i > 0 ? '1px solid #f2f4f6' : 'none',
                    transition: 'background 0.1s', alignItems: 'center',
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = '#f8f9fb'}
                  onMouseLeave={(e) => e.currentTarget.style.background = '#fff'}
                >
                  {/* Time */}
                  <div>
                    <span style={{
                      padding: '4px 8px', borderRadius: '6px', fontSize: '12px', fontWeight: 700,
                      background: p.timeAlert ? '#ffdad6' : 'rgba(0,49,120,0.08)',
                      color: p.timeAlert ? '#ba1a1a' : '#003178',
                    }}>{p.time}</span>
                  </div>

                  {/* Patient */}
                  <div>
                    <div style={{ fontSize: '14px', fontWeight: 700, color: '#191c1e' }}>{p.name}</div>
                    <div style={{ fontSize: '11px', color: '#9ca3af', marginTop: '2px' }}>{p.meta}</div>
                    <div style={{ fontSize: '11px', color: '#003178', fontWeight: 600, marginTop: '4px' }}>{p.condition}</div>
                  </div>

                  {/* Vitals */}
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                    {p.vitals.map((v) => (
                      <span key={v.label} style={{
                        padding: '3px 8px', borderRadius: '4px', fontSize: '11px', fontWeight: 600,
                        background: v.bg, color: v.color,
                      }}>{v.label}</span>
                    ))}
                  </div>

                  {/* Status */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    <span style={{
                      padding: '4px 10px', borderRadius: '5px', fontSize: '11px', fontWeight: 700,
                      width: 'fit-content', ...STATUS_STYLES[p.status],
                    }}>{p.statusLabel}</span>
                    {p.status2 && (
                      <span style={{
                        padding: '4px 10px', borderRadius: '5px', fontSize: '11px', fontWeight: 600,
                        width: 'fit-content', ...STATUS_STYLES[p.status2],
                      }}>{p.status2Label}</span>
                    )}
                  </div>

                  {/* Action */}
                  <div style={{ display: 'flex', justifyContent: 'center' }}>
                    <span className="material-icons-round" style={{ fontSize: '20px', color: '#003178' }}>chevron_right</span>
                  </div>
                </div>
              ))}

              {/* Pagination */}
              <div style={{
                padding: '12px 20px', borderTop: '1px solid #f2f4f6',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
              }}>
                <span style={{ fontSize: '12px', color: '#9ca3af' }}>Showing 4 of 12 patients scheduled today</span>
                <div style={{ display: 'flex', gap: '6px' }}>
                  {['‹', '›'].map((a) => (
                    <button key={a} style={{
                      width: '28px', height: '28px', borderRadius: '6px',
                      border: '1px solid #e1e2e4', background: '#fff',
                      cursor: 'pointer', fontSize: '14px', color: '#5a5e6b',
                    }}>{a}</button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* RIGHT PANEL */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>

            {/* Sentinel Pulse */}
            <div style={{
              background: 'linear-gradient(135deg, #003178, #0d47a1)',
              borderRadius: '12px', padding: '18px', color: '#fff',
            }}>
              <div style={{ fontSize: '9px', fontWeight: 700, letterSpacing: '0.12em', textTransform: 'uppercase', opacity: 0.65, marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '5px' }}>
                <span className="material-icons-round" style={{ fontSize: '12px' }}>bolt</span>
                Sentinel Pulse
              </div>
              <div style={{ fontFamily: 'Manrope, sans-serif', fontWeight: 800, fontSize: '16px', marginBottom: '8px' }}>
                Afternoon Outlook
              </div>
              <p style={{ fontSize: '12px', lineHeight: 1.6, opacity: 0.85, marginBottom: '12px' }}>
                Cluster of post-op vitals anomalies detected in Ward 4. AI suggests prioritizing cardiac reviews for Rodriguez and Chen.
              </p>
              <div style={{
                background: 'rgba(255,255,255,0.12)', borderRadius: '8px',
                padding: '10px 12px', fontSize: '11px', lineHeight: 1.5,
                display: 'flex', gap: '8px', alignItems: 'flex-start',
              }}>
                <span className="material-icons-round" style={{ fontSize: '14px', color: '#ffd700', marginTop: '1px' }}>lightbulb</span>
                Update dosage protocols for Ward 4 before 2 PM shift handover.
              </div>
            </div>

            {/* Critical Alerts */}
            <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
              <div style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px',
              }}>
                <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#9ca3af' }}>
                  Critical Alerts
                </span>
                <span style={{
                  background: '#ba1a1a', color: '#fff',
                  borderRadius: '10px', fontSize: '10px', fontWeight: 700,
                  padding: '1px 7px',
                }}>3</span>
              </div>

              {[
                { type: 'URGENT LAB', typeColor: '#ba1a1a', title: 'Potassium level critical', patient: 'Patient: Marcus Chen', time: '3m ago' },
                { type: 'MEDICATION', typeColor: '#9b6000', title: 'Warfarin Conflict', patient: 'Patient: James Wilson', time: '10m ago' },
                { type: 'ADMIN', typeColor: '#5a5e6b', title: 'Prior Auth Required', patient: 'Patient: Sarah Miller', time: '1h ago' },
              ].map((alert, i) => (
                <div key={alert.title} style={{
                  paddingTop: i > 0 ? '12px' : 0,
                  borderTop: i > 0 ? '1px solid #f2f4f6' : 'none',
                  marginBottom: i < 2 ? '12px' : 0,
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3px' }}>
                    <span style={{ fontSize: '9px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: alert.typeColor }}>
                      {alert.type}
                    </span>
                    <span style={{ fontSize: '10px', color: '#9ca3af' }}>{alert.time}</span>
                  </div>
                  <div style={{ fontSize: '13px', fontWeight: 700, color: '#191c1e' }}>{alert.title}</div>
                  <div style={{ fontSize: '11px', color: '#9ca3af', marginTop: '2px' }}>{alert.patient}</div>
                </div>
              ))}
            </div>

            {/* System Logs */}
            <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
              <div style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#9ca3af', marginBottom: '12px' }}>
                System Logs
              </div>
              {[
                { text: 'AI Briefing generated for Rodriguez (Cardio).', dot: '#1a7a45' },
                { text: 'Dr. Thorne reviewed 3 charts in the last hour.', dot: '#003178' },
              ].map((log, i) => (
                <div key={i} style={{ display: 'flex', gap: '10px', alignItems: 'flex-start', marginBottom: i === 0 ? '10px' : 0 }}>
                  <div style={{ width: '7px', height: '7px', borderRadius: '50%', background: log.dot, marginTop: '5px', flexShrink: 0 }} />
                  <span style={{ fontSize: '12px', color: '#5a5e6b', lineHeight: 1.5 }}>{log.text}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}