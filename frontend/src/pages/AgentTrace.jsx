import { useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';

const AGENTS = [
  { name: 'Anomaly Detector', status: 'ACTIVE', statusColor: '#1a7a45', statusBg: '#d9f0e4', msg: 'Cross-referencing historical vitals with current spike in Troponin levels.' },
  { name: 'Diagnosis Engine', status: 'PROCESSING', statusColor: '#9b6000', statusBg: '#ffecd3', msg: 'Applying Bayesian inference across 40k cardiology case studies.' },
  { name: 'Interaction Checker', status: 'VERIFIED', statusColor: '#1565c0', statusBg: '#e8f4fd', msg: 'No contraindications found between ACE inhibitors and Nitro spray.' },
  { name: 'Protocol Auditor', status: 'STANDBY', statusColor: '#5a5e6b', statusBg: '#f2f4f6', msg: 'Awaiting secondary labs to confirm AHA STEMI pathway alignment.' },
];

const NOTES = [
  '"Pt c/o chest tightness for 2hrs, radiating to L-arm. BP 145/90…"',
  '"Labs: Trop I pending, ECG shows sinus tach with possible T-wave inversion."',
  '"Hx of HTN, non-compliant with meds. Last LDL 160."',
];

const STATS = [
  { label: 'ACTIVE AGENTS', value: '09 / 12', sub: '3 on standby' },
  { label: 'KNOWLEDGE BASE', value: '2.4 TB', sub: '+142MB / s' },
  { label: 'ORCHESTRATION HEALTH', value: '98.2%', sub: 'Optimal', bar: true },
  { label: 'AVG BRIEFING LATENCY', value: '4.2s', sub: 'RAG faithfulness: 0.87' },
];

const FEATURES = ['Zero-Hallucination Guardrails', 'Multi-Model Consensus', 'HIPAA-Native Processing', 'Explainable AI Logic'];

export default function AgentTrace() {
  const navigate = useNavigate();

  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'Inter,sans-serif', background: '#f8f9fb' }}>
      <Sidebar />
      <div style={{ marginLeft: '220px', flex: 1 }}>

        {/* Header */}
        <div style={{ position: 'sticky', top: 0, zIndex: 30, background: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(14px)', borderBottom: '1px solid #f2f4f6', display: 'flex', alignItems: 'center', padding: '0 24px', height: '56px', gap: '16px' }}>
          <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '15px', color: '#003178' }}>The Clinical Sentinel</div>
          {['Active Cases', 'Alerts'].map((t, i) => (
            <div key={t} style={{ padding: '0 12px', height: '56px', display: 'flex', alignItems: 'center', fontSize: '13px', fontWeight: i === 1 ? 700 : 500, color: i === 1 ? '#003178' : '#9ca3af', borderBottom: i === 1 ? '2.5px solid #003178' : 'none', cursor: 'pointer' }}>{t}</div>
          ))}
          <div style={{ flex: 1, position: 'relative', maxWidth: '260px', marginLeft: 'auto' }}>
            <span className="material-icons-round" style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', fontSize: '16px', color: '#9ca3af' }}>search</span>
            <input placeholder="Search medical records..." style={{ width: '100%', padding: '7px 12px 7px 34px', background: '#f2f4f6', border: 'none', borderRadius: '8px', fontSize: '12px', outline: 'none' }} />
          </div>
          <button style={{ padding: '7px 14px', background: '#ba1a1a', color: '#fff', border: 'none', borderRadius: '8px', fontSize: '11px', fontWeight: 700, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span className="material-icons-round" style={{ fontSize: '14px' }}>bolt</span> Emergency Mode
          </button>
          <span className="material-icons-round" style={{ fontSize: '22px', color: '#9ca3af', cursor: 'pointer' }}>notifications</span>
          <span className="material-icons-round" style={{ fontSize: '22px', color: '#9ca3af', cursor: 'pointer' }}>account_circle</span>
        </div>

        <div style={{ padding: '24px' }}>

          {/* Page header */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
            <div>
              <h1 style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '26px', color: '#191c1e' }}>Agent Orchestration</h1>
              <p style={{ fontSize: '13px', color: '#9ca3af', marginTop: '4px', maxWidth: '480px' }}>Real-time visualization of clinical data ingestion, specialized agent synthesis, and final briefing generation.</p>
            </div>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '6px 12px', background: '#fff', borderRadius: '8px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
                <div style={{ width: '7px', height: '7px', borderRadius: '50%', background: '#1a7a45', animation: 'pulse 1.5s infinite' }} />
                <span style={{ fontSize: '11px', fontWeight: 700, color: '#191c1e' }}>LIVE PIPELINE</span>
              </div>
              <div style={{ padding: '6px 12px', background: '#fff', borderRadius: '8px', fontSize: '11px', fontWeight: 700, color: '#9ca3af', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>LATENCY: 42MS</div>
            </div>
          </div>

          {/* 3 column grid */}
          <div style={{ display: 'grid', gridTemplateColumns: '200px 1fr 200px', gap: '14px', marginBottom: '14px' }}>

            {/* Scattered Notes */}
            <div style={{ background: '#fff', borderRadius: '12px', padding: '14px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '12px' }}>
                <span className="material-icons-round" style={{ fontSize: '16px', color: '#003178' }}>description</span>
                <span style={{ fontSize: '12px', fontWeight: 700, color: '#191c1e' }}>Scattered Notes</span>
              </div>
              {NOTES.map((note, i) => (
                <div key={i} style={{ background: '#f8f9fb', borderRadius: '6px', padding: '10px', marginBottom: i < 2 ? '8px' : 0, fontSize: '11px', color: '#5a5e6b', lineHeight: 1.5, fontStyle: 'italic', borderLeft: '3px solid #e1e2e4' }}>{note}</div>
              ))}
            </div>

            {/* Agent Cards */}
            <div style={{ background: '#fff', borderRadius: '12px', padding: '14px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '10px' }}>
                {AGENTS.map((agent) => (
                  <div key={agent.name} style={{ background: '#f8f9fb', borderRadius: '8px', padding: '12px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                      <span style={{ fontSize: '12px', fontWeight: 700, color: '#191c1e' }}>{agent.name}</span>
                      <span style={{ fontSize: '9px', fontWeight: 700, padding: '2px 7px', borderRadius: '10px', background: agent.statusBg, color: agent.statusColor }}>{agent.status}</span>
                    </div>
                    <div style={{ fontSize: '11px', color: '#5a5e6b', lineHeight: 1.4 }}>{agent.msg}</div>
                  </div>
                ))}
              </div>
              <div style={{ background: '#f8f9fb', borderRadius: '8px', padding: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <span style={{ fontSize: '12px', fontWeight: 700, color: '#191c1e' }}>Longitudinal Analyst</span>
                  <span style={{ fontSize: '9px', fontWeight: 700, padding: '2px 7px', borderRadius: '10px', background: '#f3e5f5', color: '#6a1b9a' }}>SYNTHESIZING</span>
                </div>
                <div style={{ fontSize: '11px', color: '#5a5e6b' }}>Correlating 5 years of outpatient visits with current acute presentation.</div>
              </div>
            </div>

            {/* Final Briefing */}
            <div style={{ background: 'linear-gradient(160deg,#001d4a,#003178)', borderRadius: '12px', padding: '16px', color: '#fff' }}>
              <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '15px', marginBottom: '12px' }}>Final Briefing</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '16px' }}>
                {['High confidence ACS diagnosis (94%).', 'Immediate Cardiac consult recommended.', 'Medication adjustments prepared for review.'].map((item, i) => (
                  <div key={i} style={{ display: 'flex', gap: '8px', fontSize: '12px', lineHeight: 1.5 }}>
                    <span style={{ opacity: 0.5, marginTop: '2px' }}>•</span>
                    <span style={{ opacity: 0.9 }}>{item}</span>
                  </div>
                ))}
              </div>
              <button onClick={() => navigate('/patient/P001')} style={{ width: '100%', padding: '10px', background: 'rgba(255,255,255,0.15)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '8px', color: '#fff', fontSize: '12px', fontWeight: 700, cursor: 'pointer' }}>
                View Full Report
              </button>
            </div>
          </div>

          {/* Stats bar */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '12px', marginBottom: '20px' }}>
            {STATS.map((s) => (
              <div key={s.label} style={{ background: '#fff', borderRadius: '10px', padding: '14px 16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
                <div style={{ fontSize: '9px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#9ca3af', marginBottom: '6px' }}>{s.label}</div>
                <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '22px', color: '#191c1e', marginBottom: '4px' }}>{s.value}</div>
                {s.bar && <div style={{ height: '4px', background: '#f2f4f6', borderRadius: '2px', marginBottom: '4px' }}><div style={{ height: '4px', width: '98%', background: '#1a7a45', borderRadius: '2px' }} /></div>}
                <div style={{ fontSize: '11px', color: '#9ca3af' }}>{s.sub}</div>
              </div>
            ))}
          </div>

          {/* Hackathon Spotlight */}
          <div style={{ background: '#fff', borderRadius: '12px', padding: '32px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)', display: 'grid', gridTemplateColumns: '280px 1fr', gap: '32px', alignItems: 'center' }}>
            <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuBVhL4sqFbqSYnTOJH9AeecV131gQNw4Z7BSE-mbTGdmZExqAkgo7xB-Og_KS2Umg9e_Effx8jNSD2WTSZLr8qFUjtaPAGlu7N1w6U-joyPqFxxs4bzFNyYzn1SO0ZmnJRqYicHj-ulKfo2rF8QrTvNz1Sm1TdVSHVo99mExzC9q5CNques4SIFUN5P8dX2XXJiBo-Yx0eIJxznkXRPcK7yFyo9YMfsvTa-9FMzD5Pa_8Fmu_lsTibSVpXwTc4YLZXhNZnd-CVrTEw" alt="Hyper-Specialized AI" style={{ width: '100%', borderRadius: '10px', objectFit: 'cover' }} />
            <div>
              <div style={{ display: 'inline-block', fontSize: '9px', fontWeight: 700, letterSpacing: '0.15em', textTransform: 'uppercase', color: '#003178', background: 'rgba(0,49,120,0.07)', padding: '4px 12px', borderRadius: '20px', marginBottom: '16px' }}>Hackathon Tech Spotlight</div>
              <h2 style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '28px', color: '#003178', lineHeight: 1.15, marginBottom: '16px' }}>Hyper-Specialized Micro-Agents</h2>
              <p style={{ fontSize: '14px', color: '#5a5e6b', lineHeight: 1.7, marginBottom: '24px' }}>Instead of one generic LLM, Clinical Sentinel orchestrates 9 specialized agents. Each agent is tuned for a specific medical domain — from pharmacokinetics to billing compliance — ensuring precision that "one-size-fits-all" AI simply cannot match.</p>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                {FEATURES.map((feature) => (
                  <div key={feature} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div style={{ width: '20px', height: '20px', borderRadius: '50%', background: '#003178', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                      <span className="material-icons-round" style={{ fontSize: '12px', color: '#fff' }}>check</span>
                    </div>
                    <span style={{ fontSize: '13px', fontWeight: 600, color: '#191c1e' }}>{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
      <style>{`@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }`}</style>
    </div>
  );
}