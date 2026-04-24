import { useNavigate, useParams } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

const AGENTS = [
  { name: 'VITAL AGENT', dot: '#1a7a45', msg: 'Monitoring heart rate spikes. Trend analysis initiated.', time: '12:41:02', source: 'Vitals Stream' },
  { name: 'PHARMAGENT', dot: '#1a7a45', msg: 'FLAG: Interaction detected between Warfarin and Ibuprofen.', time: '12:42:15', source: 'Rx Check' },
  { name: 'LABAGENT', dot: '#1a7a45', msg: 'Comparing CBC results with clinical history. WBC elevating.', time: '12:42:98', source: 'Lab Stream' },
  { name: 'RADAGENT', dot: '#9ca3af', msg: 'Waiting for Chest X-ray upload.', time: '12:40:11', source: 'Imaging Queue', idle: true },
  { name: 'RISKAGENT', dot: '#1a7a45', msg: 'Fall Risk score updated based on last mobility test.', time: '12:30:22', source: 'Analytics' },
  { name: 'HISTAGENT', dot: '#1a7a45', msg: 'Parsing 2018 oncology records for relevant history.', time: '12:35:45', source: 'EHR Scan' },
  { name: 'DIAGNOSAGENT', dot: '#f97316', msg: 'Computing differential confidence scores...', time: '12:37:05', source: 'Processing' },
];

export default function PatientBriefing() {
  const navigate = useNavigate();
  const { id } = useParams();
  const doctor = useAuthStore((s) => s.doctor);
  const logout = useAuthStore((s) => s.logout);

  const Sidebar = () => (
    <div style={{
      width: '220px', minWidth: '220px', height: '100vh',
      position: 'fixed', left: 0, top: 0,
      background: 'rgba(248,249,251,0.95)',
      backdropFilter: 'blur(14px)',
      display: 'flex', flexDirection: 'column', zIndex: 40,
    }}>
      <div style={{ padding: '24px 20px 16px' }}>
        <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '15px', color: '#003178' }}>Clinical Sentinel</div>
        <div style={{ fontSize: '9px', fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', color: '#9ca3af', marginTop: '2px' }}>Medical AI Copilot</div>
      </div>
      <div style={{ padding: '8px 10px', flex: 1, display: 'flex', flexDirection: 'column', gap: '2px' }}>
        {[
          { label: 'Dashboard', icon: 'dashboard', path: '/dashboard' },
          { label: 'Patient Briefing', icon: 'assignment_ind', path: '/patient/P001', active: true },
          { label: 'SOAP Generator', icon: 'history_edu', path: '/soap' },
          { label: 'Agent Status', icon: 'smart_toy', path: '/agents' },
        ].map((item) => (
          <div key={item.label} onClick={() => navigate(item.path)} style={{
            display: 'flex', alignItems: 'center', gap: '10px',
            padding: '9px 12px', borderRadius: '8px', cursor: 'pointer',
            fontSize: '13px', fontWeight: item.active ? 700 : 500,
            color: item.active ? '#003178' : '#5a5e6b',
            background: item.active ? 'rgba(0,49,120,0.07)' : 'transparent',
            borderRight: item.active ? '2.5px solid #003178' : '2.5px solid transparent',
          }}>
            <span className="material-icons-round" style={{ fontSize: '18px' }}>{item.icon}</span>
            {item.label}
          </div>
        ))}
      </div>
      <div style={{ padding: '14px' }}>
        <button onClick={() => navigate('/patient/P001')} style={{
          width: '100%', padding: '10px', marginBottom: '12px',
          background: 'linear-gradient(135deg,#003178,#0d47a1)',
          color: '#fff', border: 'none', borderRadius: '8px',
          fontSize: '13px', fontWeight: 600, cursor: 'pointer',
          display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px',
        }}>
          <span className="material-icons-round" style={{ fontSize: '16px' }}>add</span>
          New Consultation
        </button>
        <div style={{ fontSize: '11px', color: '#9ca3af', marginBottom: '8px', paddingLeft: '4px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
          <span style={{ cursor: 'pointer' }}>⚙ Settings</span>
          <span style={{ cursor: 'pointer' }}>? Support</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 4px' }}>
          <div style={{ width: '30px', height: '30px', borderRadius: '50%', background: 'linear-gradient(135deg,#003178,#0d47a1)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: '11px', fontWeight: 700 }}>JT</div>
          <div>
            <div style={{ fontSize: '11px', fontWeight: 700, color: '#191c1e' }}>Dr. Julian Thorne</div>
            <div style={{ fontSize: '10px', color: '#9ca3af' }}>Senior Oncologist</div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'Inter,sans-serif', background: '#f8f9fb' }}>
      <Sidebar />
      <div style={{ marginLeft: '220px', flex: 1 }}>

        {/* Header */}
        <div style={{
          position: 'sticky', top: 0, zIndex: 30,
          background: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(14px)',
          borderBottom: '1px solid #f2f4f6',
          display: 'flex', alignItems: 'center', padding: '0 24px', height: '56px', gap: '16px',
        }}>
          <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '15px', color: '#003178' }}>The Clinical Sentinel</div>
          {['Active Cases', 'Alerts'].map((t, i) => (
            <div key={t} style={{ padding: '0 12px', height: '56px', display: 'flex', alignItems: 'center', fontSize: '13px', fontWeight: i === 0 ? 700 : 500, color: i === 0 ? '#003178' : '#9ca3af', borderBottom: i === 0 ? '2.5px solid #003178' : 'none', cursor: 'pointer' }}>{t}</div>
          ))}
          <div style={{ flex: 1, position: 'relative', maxWidth: '260px', marginLeft: 'auto' }}>
            <span className="material-icons-round" style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', fontSize: '16px', color: '#9ca3af' }}>search</span>
            <input placeholder="Search patient or record..." style={{ width: '100%', padding: '7px 12px 7px 34px', background: '#f2f4f6', border: 'none', borderRadius: '8px', fontSize: '12px', outline: 'none' }} />
          </div>
          <button style={{ padding: '7px 14px', background: '#ba1a1a', color: '#fff', border: 'none', borderRadius: '8px', fontSize: '11px', fontWeight: 700, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span className="material-icons-round" style={{ fontSize: '14px' }}>bolt</span> EMERGENCY MODE
          </button>
          <span className="material-icons-round" style={{ fontSize: '22px', color: '#9ca3af', cursor: 'pointer' }}>notifications</span>
          <span className="material-icons-round" style={{ fontSize: '22px', color: '#9ca3af', cursor: 'pointer' }}>account_circle</span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 260px', gap: '0', minHeight: 'calc(100vh - 56px)' }}>

          {/* MAIN CONTENT */}
          <div style={{ padding: '20px 20px 20px 24px' }}>

            {/* Patient Header */}
            <div style={{ background: '#fff', borderRadius: '12px', padding: '18px 20px', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
              <div style={{ width: '52px', height: '52px', borderRadius: '10px', background: '#f2f4f6', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px', fontWeight: 800, color: '#003178', flexShrink: 0 }}>EV</div>
              <div style={{ flex: 1 }}>
                <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '20px', color: '#191c1e' }}>Eleanor Vance, 74</div>
                <div style={{ display: 'flex', gap: '16px', marginTop: '3px' }}>
                  <span style={{ fontSize: '12px', color: '#9ca3af' }}>ID: #MED-8829-X</span>
                  <span style={{ fontSize: '12px', color: '#9ca3af' }}>📅 Adm: Oct 12, 2023</span>
                </div>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                {[{ label: 'BLOOD TYPE', value: 'A Pos' }, { label: 'HEIGHT', value: '162 cm' }, { label: 'WEIGHT', value: '68 kg' }].map((s) => (
                  <div key={s.label} style={{ background: '#f2f4f6', borderRadius: '8px', padding: '8px 14px', textAlign: 'center' }}>
                    <div style={{ fontSize: '9px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#9ca3af' }}>{s.label}</div>
                    <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '16px', color: '#191c1e', marginTop: '2px' }}>{s.value}</div>
                  </div>
                ))}
              </div>
              <button style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 16px', background: 'rgba(0,49,120,0.08)', border: 'none', borderRadius: '20px', color: '#003178', fontSize: '12px', fontWeight: 600, cursor: 'pointer' }}>
                <span className="material-icons-round" style={{ fontSize: '16px' }}>volume_up</span>
                Play Voice Briefing
              </button>
            </div>

            {/* 2x2 Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '14px' }}>

              {/* Vital Anomaly */}
              <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                  <span className="material-icons-round" style={{ fontSize: '16px', color: '#ba1a1a' }}>warning</span>
                  <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: '#5a5e6b' }}>Vital Anomaly Detection</span>
                  <span style={{ marginLeft: 'auto', background: '#ffdad6', color: '#ba1a1a', fontSize: '10px', fontWeight: 700, padding: '2px 8px', borderRadius: '10px' }}>2 CRITICAL</span>
                </div>
                {[
                  { icon: 'favorite', label: 'RESTING HR', value: '114 BPM', valueColor: '#ba1a1a', note: '+22% vs Baseline', sub: 'Tachycardia detected', subColor: '#ba1a1a' },
                  { icon: 'thermostat', label: 'BODY TEMP', value: '38.9°C', valueColor: '#ba1a1a', note: 'Rising rapidly', sub: 'Fever spiked at 02:15', subColor: '#ba1a1a' },
                  { icon: 'monitor_heart', label: 'BLOOD PRESSURE', value: '138 / 92', valueColor: '#191c1e', note: 'High/Stable', sub: 'Stage 1 Hypertension', subColor: '#9b6000' },
                ].map((v, i) => (
                  <div key={v.label} style={{ paddingTop: i > 0 ? '12px' : 0, borderTop: i > 0 ? '1px solid #f2f4f6' : 'none', marginBottom: i < 2 ? '12px' : 0 }}>
                    <div style={{ fontSize: '9px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#9ca3af', marginBottom: '4px' }}>{v.label}</div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '22px', color: v.valueColor }}>{v.value}</div>
                      <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '11px', fontWeight: 600, color: '#ba1a1a' }}>{v.note}</div>
                        <div style={{ fontSize: '10px', color: v.subColor }}>{v.sub}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Differential Diagnosis */}
              <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                  <span className="material-icons-round" style={{ fontSize: '16px', color: '#003178' }}>analytics</span>
                  <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: '#5a5e6b' }}>Differential Diagnosis</span>
                  <span style={{ marginLeft: 'auto', fontSize: '10px', color: '#9ca3af', fontWeight: 600 }}>AI CONFIDENCE INDEX</span>
                </div>
                {[
                  { label: 'Acute Pyelonephritis', pct: 84, color: '#003178' },
                  { label: 'Sepsis secondary to UTI', pct: 61, color: '#003178' },
                  { label: 'Nephrolithiasis', pct: 22, color: '#9ca3af' },
                ].map((d) => (
                  <div key={d.label} style={{ marginBottom: '12px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                      <span style={{ fontSize: '13px', fontWeight: 600, color: '#191c1e' }}>{d.label}</span>
                      <span style={{ fontSize: '13px', fontWeight: 700, color: d.color }}>{d.pct}%</span>
                    </div>
                    <div style={{ height: '5px', background: '#f2f4f6', borderRadius: '3px' }}>
                      <div style={{ height: '5px', width: `${d.pct}%`, background: d.color, borderRadius: '3px' }} />
                    </div>
                  </div>
                ))}
                <div style={{ marginTop: '12px', padding: '10px', background: '#f8f9fb', borderRadius: '8px', fontSize: '11px', color: '#5a5e6b', lineHeight: 1.5, fontStyle: 'italic' }}>
                  "Agent Diagnostic detected correlated white blood cell count spikes in recent labs."
                </div>
              </div>

              {/* Drug Interaction */}
              <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                  <span className="material-icons-round" style={{ fontSize: '16px', color: '#003178' }}>medication</span>
                  <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: '#5a5e6b' }}>Drug Interaction Check</span>
                  <span style={{ marginLeft: 'auto', fontSize: '11px', fontWeight: 600, color: '#003178', cursor: 'pointer' }}>VIEW FULL LIST</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '12px', background: '#ffdad6', borderRadius: '8px' }}>
                  <span className="material-icons-round" style={{ fontSize: '20px', color: '#ba1a1a' }}>dangerous</span>
                  <div>
                    <div style={{ fontSize: '13px', fontWeight: 700, color: '#ba1a1a' }}>Warfarin × Ibuprofen</div>
                    <div style={{ fontSize: '11px', color: '#5a5e6b', marginTop: '2px' }}>High risk of internal bleeding</div>
                  </div>
                </div>
              </div>

              {/* Risk Scores */}
              <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                  <span className="material-icons-round" style={{ fontSize: '16px', color: '#003178' }}>bar_chart</span>
                  <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: '#5a5e6b' }}>Dynamic Risk Scores</span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                  <div style={{ background: '#f2f4f6', borderRadius: '8px', padding: '14px', textAlign: 'center' }}>
                    <div style={{ fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', color: '#9ca3af', marginBottom: '6px' }}>CARDIO RISK</div>
                    <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '28px', color: '#191c1e' }}>18<span style={{ fontSize: '14px' }}>%</span></div>
                  </div>
                  <div style={{ background: '#ffdad6', borderRadius: '8px', padding: '14px', textAlign: 'center' }}>
                    <div style={{ fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', color: '#ba1a1a', marginBottom: '6px' }}>FALL RISK</div>
                    <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '28px', color: '#ba1a1a' }}>72<span style={{ fontSize: '14px' }}>%</span></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* AI AGENT LOG SIDEBAR */}
          <div style={{ background: 'linear-gradient(160deg,#001d4a,#003178,#0d47a1)', padding: '20px 16px', minHeight: 'calc(100vh - 56px)' }}>
            <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '14px', color: '#fff', marginBottom: '4px' }}>🤖 AI Agent Log</div>
            <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.6)', marginBottom: '16px' }}>9 Agents Active · Real-time Monitoring</div>

            {AGENTS.map((agent, i) => (
              <div key={agent.name} style={{ borderTop: i > 0 ? '1px solid rgba(255,255,255,0.1)' : 'none', paddingTop: i > 0 ? '12px' : 0, marginBottom: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span style={{ fontSize: '10px', fontWeight: 700, letterSpacing: '0.08em', color: agent.idle ? 'rgba(255,255,255,0.4)' : 'rgba(255,255,255,0.75)' }}>{agent.name}</span>
                    <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: agent.dot }} />
                  </div>
                  {agent.idle && <span style={{ fontSize: '9px', color: 'rgba(255,255,255,0.35)', fontWeight: 600 }}>IDLE</span>}
                </div>
                <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.85)', lineHeight: 1.5, marginBottom: '3px' }}>{agent.msg}</div>
                <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.4)' }}>{agent.time} · {agent.source}</div>
              </div>
            ))}

            <button style={{ width: '100%', marginTop: '8px', padding: '10px', background: 'rgba(255,255,255,0.12)', border: 'none', borderRadius: '8px', color: '#fff', fontSize: '12px', fontWeight: 700, cursor: 'pointer', letterSpacing: '0.04em' }}>
              CONFIGURE AGENT HIVE
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}