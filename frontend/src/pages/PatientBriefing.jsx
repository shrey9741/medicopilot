import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import API from '../api/client';

const AGENTS = [
  { name: 'VITAL AGENT', dot: '#1a7a45', msg: 'Monitoring heart rate spikes. Trend analysis initiated.', time: '12:41:02', source: 'Vitals Stream' },
  { name: 'PHARMAGENT', dot: '#1a7a45', msg: 'FLAG: Interaction detected between Warfarin and Ibuprofen.', time: '12:42:15', source: 'Rx Check' },
  { name: 'LABAGENT', dot: '#1a7a45', msg: 'Comparing CBC results with clinical history. WBC elevating.', time: '12:42:50', source: 'Lab Stream' },
  { name: 'RADAGENT', dot: '#9ca3af', msg: 'Waiting for Chest X-ray upload.', time: '12:40:11', source: 'Imaging Queue', idle: true },
  { name: 'RISKAGENT', dot: '#1a7a45', msg: 'Fall Risk score updated based on last mobility test.', time: '12:38:22', source: 'Analytics' },
  { name: 'DIAGNOSAGENT', dot: '#f97316', msg: 'Computing differential confidence scores...', time: '12:33:01', source: 'Processing' },
];

export default function PatientBriefing() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [briefing, setBriefing] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [voicePlaying, setVoicePlaying] = useState(false);

  useEffect(() => {
    const fetchBriefing = async () => {
      try {
        setLoading(true);
        const res = await API.post('/invoke', {
          patient_id: id || 'P001',
          sharp_token: null,
        });
        setBriefing(res.data);
      } catch (err) {
        setError('Could not generate briefing. Showing demo data.');
      } finally {
        setLoading(false);
      }
    };
    fetchBriefing();
  }, [id]);

  const handleVoice = () => setVoicePlaying(!voicePlaying);

  const Sidebar = () => (
    <div style={{ width: '220px', minWidth: '220px', height: '100vh', position: 'fixed', left: 0, top: 0, background: 'rgba(248,249,251,0.95)', backdropFilter: 'blur(14px)', display: 'flex', flexDirection: 'column', zIndex: 40 }}>
      <div style={{ padding: '24px 20px 16px' }}>
        <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '15px', color: '#003178' }}>Clinical Sentinel</div>
        <div style={{ fontSize: '9px', fontWeight: 700, letterSpacing: '0.14em', textTransform: 'uppercase', color: '#9ca3af', marginTop: '2px' }}>Medical AI Copilot</div>
      </div>
      <div style={{ padding: '8px 10px', flex: 1, display: 'flex', flexDirection: 'column', gap: '2px' }}>
        {[
          { label: 'Dashboard', icon: 'dashboard', path: '/dashboard' },
          { label: 'Patient Briefing', icon: 'assignment_ind', path: `/patient/${id}`, active: true },
          { label: 'SOAP Generator', icon: 'history_edu', path: '/soap' },
          { label: 'Agent Status', icon: 'smart_toy', path: '/agents' },
        ].map((item) => (
          <div key={item.label} onClick={() => navigate(item.path)} style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '9px 12px', borderRadius: '8px', cursor: 'pointer', fontSize: '13px', fontWeight: item.active ? 700 : 500, color: item.active ? '#003178' : '#5a5e6b', background: item.active ? 'rgba(0,49,120,0.07)' : 'transparent', borderRight: item.active ? '2.5px solid #003178' : '2.5px solid transparent' }}>
            <span className="material-icons-round" style={{ fontSize: '18px' }}>{item.icon}</span>
            {item.label}
          </div>
        ))}
      </div>
      <div style={{ padding: '14px' }}>
        <button onClick={() => navigate('/dashboard')} style={{ width: '100%', padding: '10px', marginBottom: '12px', background: 'linear-gradient(135deg,#003178,#0d47a1)', color: '#fff', border: 'none', borderRadius: '8px', fontSize: '13px', fontWeight: 600, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
          <span className="material-icons-round" style={{ fontSize: '16px' }}>arrow_back</span>
          Back to Dashboard
        </button>
        <div style={{ fontSize: '11px', color: '#9ca3af', paddingLeft: '4px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
          <span style={{ cursor: 'pointer' }}>⚙ Settings</span>
          <span style={{ cursor: 'pointer' }}>? Support</span>
        </div>
      </div>
    </div>
  );

  if (loading) return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'Inter,sans-serif', background: '#f8f9fb' }}>
      <Sidebar />
      <div style={{ marginLeft: '220px', flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '16px' }}>
        <div style={{ width: '48px', height: '48px', border: '4px solid #f2f4f6', borderTop: '4px solid #003178', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
        <div style={{ fontSize: '14px', color: '#9ca3af', fontWeight: 600 }}>Generating AI briefing for patient {id}...</div>
        <div style={{ fontSize: '12px', color: '#c4c6d2' }}>9 agents working in parallel</div>
        <style>{`@keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }`}</style>
      </div>
    </div>
  );

  // Parse briefing data
  const patientName = briefing?.patient_name || briefing?.name || `Patient ${id}`;
  const summary = briefing?.summary || briefing?.briefing || '';
  const diagnoses = briefing?.diagnoses || briefing?.differential_diagnosis || [];
  const drugWarnings = briefing?.drug_warnings || briefing?.drug_interactions || [];
  const riskScores = briefing?.risk_scores || {};
  const soapNote = briefing?.soap_note || {};
  const anomalies = briefing?.anomalies || briefing?.vital_anomalies || [];

  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'Inter,sans-serif', background: '#f8f9fb' }}>
      <Sidebar />
      <div style={{ marginLeft: '220px', flex: 1 }}>

        {/* Header */}
        <div style={{ position: 'sticky', top: 0, zIndex: 30, background: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(14px)', borderBottom: '1px solid #f2f4f6', display: 'flex', alignItems: 'center', padding: '0 24px', height: '56px', gap: '16px' }}>
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

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 260px', minHeight: 'calc(100vh - 56px)' }}>

          {/* MAIN */}
          <div style={{ padding: '20px 20px 20px 24px' }}>

            {/* Error banner */}
            {error && (
              <div style={{ background: '#ffecd3', border: '1px solid #f97316', color: '#9b6000', padding: '10px 16px', borderRadius: '8px', fontSize: '12px', fontWeight: 600, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span className="material-icons-round" style={{ fontSize: '16px' }}>warning</span>
                {error}
              </div>
            )}

            {/* Patient header */}
            <div style={{ background: '#fff', borderRadius: '12px', padding: '18px 20px', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)', flexWrap: 'wrap' }}>
              <div style={{ width: '52px', height: '52px', borderRadius: '10px', background: '#f2f4f6', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px', fontWeight: 800, color: '#003178', flexShrink: 0 }}>
                {patientName.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '20px', color: '#191c1e' }}>{patientName}</div>
                <div style={{ fontSize: '12px', color: '#9ca3af', marginTop: '3px' }}>ID: {id} · Generated {new Date().toLocaleTimeString()}</div>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                {[
                  { label: 'FHIR SOURCE', value: briefing?.fhir_source || 'mock' },
                  { label: 'AGENTS', value: '9 Active' },
                  { label: 'CONFIDENCE', value: '94%' },
                ].map((s) => (
                  <div key={s.label} style={{ background: '#f2f4f6', borderRadius: '8px', padding: '8px 14px', textAlign: 'center' }}>
                    <div style={{ fontSize: '9px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#9ca3af' }}>{s.label}</div>
                    <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '14px', color: '#191c1e', marginTop: '2px' }}>{s.value}</div>
                  </div>
                ))}
              </div>
              <button onClick={handleVoice} style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 16px', background: voicePlaying ? '#003178' : 'rgba(0,49,120,0.08)', border: 'none', borderRadius: '20px', color: voicePlaying ? '#fff' : '#003178', fontSize: '12px', fontWeight: 600, cursor: 'pointer' }}>
                <span className="material-icons-round" style={{ fontSize: '16px' }}>{voicePlaying ? 'pause' : 'volume_up'}</span>
                {voicePlaying ? 'Pause Briefing' : 'Play Voice Briefing'}
              </button>
            </div>

            {/* AI Summary */}
            {summary && (
              <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', marginBottom: '14px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)', borderLeft: '4px solid #003178' }}>
                <div style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#003178', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span className="material-icons-round" style={{ fontSize: '14px' }}>auto_awesome</span>
                  AI Clinical Summary
                </div>
                <div style={{ fontSize: '13px', color: '#5a5e6b', lineHeight: 1.7 }}>{summary}</div>
              </div>
            )}

            {/* 2x2 Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>

              {/* Vital Anomalies */}
              <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                  <span className="material-icons-round" style={{ fontSize: '16px', color: '#ba1a1a' }}>warning</span>
                  <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: '#5a5e6b' }}>Vital Anomaly Detection</span>
                  {anomalies.length > 0 && (
                    <span style={{ marginLeft: 'auto', background: '#ffdad6', color: '#ba1a1a', fontSize: '10px', fontWeight: 700, padding: '2px 8px', borderRadius: '10px' }}>{anomalies.length} DETECTED</span>
                  )}
                </div>
                {anomalies.length > 0 ? (
                  anomalies.slice(0, 3).map((a, i) => (
                    <div key={i} style={{ paddingTop: i > 0 ? '10px' : 0, borderTop: i > 0 ? '1px solid #f2f4f6' : 'none', marginBottom: i < anomalies.length - 1 ? '10px' : 0 }}>
                      <div style={{ fontSize: '11px', fontWeight: 700, color: '#ba1a1a' }}>{a.vital || a.type || 'Anomaly'}</div>
                      <div style={{ fontSize: '12px', color: '#5a5e6b', marginTop: '2px' }}>{a.description || a.value || JSON.stringify(a)}</div>
                    </div>
                  ))
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    {[
                      { label: 'RESTING HR', value: '114 BPM', color: '#ba1a1a', note: 'Tachycardia detected' },
                      { label: 'BODY TEMP', value: '38.9°C', color: '#ba1a1a', note: 'Rising rapidly' },
                      { label: 'BLOOD PRESSURE', value: '138/92', color: '#9b6000', note: 'Stage 1 Hypertension' },
                    ].map((v, i) => (
                      <div key={v.label} style={{ paddingTop: i > 0 ? '10px' : 0, borderTop: i > 0 ? '1px solid #f2f4f6' : 'none' }}>
                        <div style={{ fontSize: '9px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#9ca3af', marginBottom: '3px' }}>{v.label}</div>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                          <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '18px', color: v.color }}>{v.value}</div>
                          <div style={{ fontSize: '11px', color: v.color, fontWeight: 600, textAlign: 'right' }}>{v.note}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Differential Diagnosis */}
              <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                  <span className="material-icons-round" style={{ fontSize: '16px', color: '#003178' }}>analytics</span>
                  <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: '#5a5e6b' }}>Differential Diagnosis</span>
                  <span style={{ marginLeft: 'auto', fontSize: '10px', color: '#9ca3af', fontWeight: 600 }}>AI CONFIDENCE</span>
                </div>
                {diagnoses.length > 0 ? (
                  diagnoses.slice(0, 3).map((d, i) => {
                    const name = d.condition || d.diagnosis || d.name || 'Unknown';
                    const conf = d.confidence || d.probability || (85 - i * 20);
                    const pct = typeof conf === 'string' ? parseInt(conf) : Math.round(conf * (conf > 1 ? 1 : 100));
                    return (
                      <div key={i} style={{ marginBottom: '12px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                          <span style={{ fontSize: '13px', fontWeight: 600, color: '#191c1e' }}>{name}</span>
                          <span style={{ fontSize: '13px', fontWeight: 700, color: '#003178' }}>{pct}%</span>
                        </div>
                        <div style={{ height: '5px', background: '#f2f4f6', borderRadius: '3px' }}>
                          <div style={{ height: '5px', width: `${pct}%`, background: '#003178', borderRadius: '3px' }} />
                        </div>
                      </div>
                    );
                  })
                ) : (
                  [{ label: 'Acute Pyelonephritis', pct: 84 }, { label: 'Sepsis secondary to UTI', pct: 61 }, { label: 'Nephrolithiasis', pct: 22 }].map((d) => (
                    <div key={d.label} style={{ marginBottom: '12px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                        <span style={{ fontSize: '13px', fontWeight: 600, color: '#191c1e' }}>{d.label}</span>
                        <span style={{ fontSize: '13px', fontWeight: 700, color: '#003178' }}>{d.pct}%</span>
                      </div>
                      <div style={{ height: '5px', background: '#f2f4f6', borderRadius: '3px' }}>
                        <div style={{ height: '5px', width: `${d.pct}%`, background: '#003178', borderRadius: '3px' }} />
                      </div>
                    </div>
                  ))
                )}
              </div>

              {/* Drug Interactions */}
              <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                  <span className="material-icons-round" style={{ fontSize: '16px', color: '#003178' }}>medication</span>
                  <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: '#5a5e6b' }}>Drug Interaction Check</span>
                  <span style={{ marginLeft: 'auto', fontSize: '11px', fontWeight: 600, color: '#003178', cursor: 'pointer' }}>VIEW ALL</span>
                </div>
                {drugWarnings.length > 0 ? (
                  drugWarnings.slice(0, 2).map((w, i) => (
                    <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', padding: '10px', background: '#ffdad6', borderRadius: '8px', marginBottom: i < drugWarnings.length - 1 ? '8px' : 0 }}>
                      <span className="material-icons-round" style={{ fontSize: '18px', color: '#ba1a1a', flexShrink: 0 }}>dangerous</span>
                      <div>
                        <div style={{ fontSize: '12px', fontWeight: 700, color: '#ba1a1a' }}>{w.interaction || w.drugs || w.warning || 'Drug Interaction Detected'}</div>
                        <div style={{ fontSize: '11px', color: '#5a5e6b', marginTop: '2px' }}>{w.severity || w.description || 'Review required'}</div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', padding: '10px', background: '#d9f0e4', borderRadius: '8px' }}>
                    <span className="material-icons-round" style={{ fontSize: '18px', color: '#1a7a45' }}>check_circle</span>
                    <div>
                      <div style={{ fontSize: '12px', fontWeight: 700, color: '#1a7a45' }}>No Critical Interactions</div>
                      <div style={{ fontSize: '11px', color: '#5a5e6b', marginTop: '2px' }}>All medications reviewed</div>
                    </div>
                  </div>
                )}
              </div>

              {/* Risk Scores */}
              <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                  <span className="material-icons-round" style={{ fontSize: '16px', color: '#003178' }}>bar_chart</span>
                  <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: '#5a5e6b' }}>Dynamic Risk Scores</span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                  {Object.entries(riskScores).length > 0 ? (
                    Object.entries(riskScores).slice(0, 2).map(([key, val]) => {
                      const pct = typeof val === 'number' ? Math.round(val * (val > 1 ? 1 : 100)) : parseInt(val) || 0;
                      const isHigh = pct > 60;
                      return (
                        <div key={key} style={{ background: isHigh ? '#ffdad6' : '#f2f4f6', borderRadius: '8px', padding: '14px', textAlign: 'center' }}>
                          <div style={{ fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', color: isHigh ? '#ba1a1a' : '#9ca3af', marginBottom: '6px' }}>{key.replace(/_/g, ' ')}</div>
                          <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '28px', color: isHigh ? '#ba1a1a' : '#191c1e' }}>{pct}<span style={{ fontSize: '14px' }}>%</span></div>
                        </div>
                      );
                    })
                  ) : (
                    <>
                      <div style={{ background: '#f2f4f6', borderRadius: '8px', padding: '14px', textAlign: 'center' }}>
                        <div style={{ fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', color: '#9ca3af', marginBottom: '6px' }}>CARDIO RISK</div>
                        <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '28px', color: '#191c1e' }}>18<span style={{ fontSize: '14px' }}>%</span></div>
                      </div>
                      <div style={{ background: '#ffdad6', borderRadius: '8px', padding: '14px', textAlign: 'center' }}>
                        <div style={{ fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', color: '#ba1a1a', marginBottom: '6px' }}>FALL RISK</div>
                        <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '28px', color: '#ba1a1a' }}>72<span style={{ fontSize: '14px' }}>%</span></div>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>

            {/* SOAP Note Preview */}
            {soapNote && Object.keys(soapNote).length > 0 && (
              <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', marginTop: '14px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <div style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: '#5a5e6b', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span className="material-icons-round" style={{ fontSize: '16px', color: '#003178' }}>history_edu</span>
                    SOAP Note Preview
                  </div>
                  <button onClick={() => navigate('/soap')} style={{ padding: '6px 14px', background: '#003178', color: '#fff', border: 'none', borderRadius: '6px', fontSize: '12px', fontWeight: 600, cursor: 'pointer' }}>
                    Open Full Editor →
                  </button>
                </div>
                {['subjective', 'objective', 'assessment', 'plan'].map((key) => (
                  soapNote[key] && (
                    <div key={key} style={{ marginBottom: '10px', padding: '10px', background: '#f8f9fb', borderRadius: '8px', borderLeft: '3px solid rgba(0,49,120,0.15)' }}>
                      <div style={{ fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', color: '#003178', marginBottom: '4px' }}>{key}</div>
                      <div style={{ fontSize: '12px', color: '#5a5e6b', lineHeight: 1.6 }}>
                        {typeof soapNote[key] === 'string' ? soapNote[key].slice(0, 200) + (soapNote[key].length > 200 ? '...' : '') : JSON.stringify(soapNote[key]).slice(0, 200)}
                      </div>
                    </div>
                  )
                ))}
              </div>
            )}
          </div>

          {/* AI AGENT LOG */}
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
            <button style={{ width: '100%', marginTop: '8px', padding: '10px', background: 'rgba(255,255,255,0.12)', border: 'none', borderRadius: '8px', color: '#fff', fontSize: '12px', fontWeight: 700, cursor: 'pointer' }}>
              CONFIGURE AGENT HIVE
            </button>
          </div>
        </div>
      </div>
      <style>{`@keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }`}</style>
    </div>
  );
}