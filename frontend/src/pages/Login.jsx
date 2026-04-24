import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import API from '../api/client';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const login = useAuthStore((s) => s.login);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await API.post('/auth/login', { username, password });
      login(res.data.access_token, {
        name: res.data.doctor_name,
        role: res.data.role,
        username,
      });
      navigate('/dashboard');
    } catch {
      setError('Invalid credentials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      minHeight: '100vh',
      fontFamily: 'Inter, sans-serif',
      background: '#f8f9fb',
    }}>
      <main style={{ display: 'flex', flex: 1 }}>

        {/* ── LEFT PANEL ── */}
        <div style={{
          width: '42%',
          minHeight: '100vh',
          background: 'linear-gradient(160deg, #001d4a 0%, #003178 55%, #0d47a1 100%)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          padding: '40px 48px',
          color: '#fff',
          position: 'relative',
          overflow: 'hidden',
        }}>
          {/* subtle grain overlay */}
          <div style={{
            position: 'absolute', inset: 0, opacity: 0.04,
            backgroundImage: 'url("https://grainy-gradients.vercel.app/noise.svg")',
            pointerEvents: 'none',
          }} />

          {/* Logo */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', position: 'relative', zIndex: 1 }}>
            <div style={{
              width: '40px', height: '40px', borderRadius: '8px',
              background: 'rgba(255,255,255,0.12)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              <span className="material-icons-round" style={{ fontSize: '22px' }}>clinical_notes</span>
            </div>
            <div>
              <div style={{ fontFamily: 'Manrope, sans-serif', fontWeight: 800, fontSize: '16px', lineHeight: 1.2 }}>
                Clinical Sentinel
              </div>
              <div style={{ fontSize: '9px', letterSpacing: '0.18em', textTransform: 'uppercase', opacity: 0.55, fontWeight: 600 }}>
                Medical AI Copilot
              </div>
            </div>
          </div>

          {/* Headline + Stats */}
          <div style={{ position: 'relative', zIndex: 1 }}>
            <h1 style={{
              fontFamily: 'Manrope, sans-serif', fontWeight: 800,
              fontSize: '42px', lineHeight: 1.1, letterSpacing: '-0.02em',
              marginBottom: '48px',
            }}>
              Know your patient<br />before you walk in.
            </h1>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              {[
                { value: '< 5s', label: 'Avg briefing time' },
                { value: '9', label: 'Specialized agents' },
                { value: '0.87', label: 'RAG faithfulness' },
              ].map((s) => (
                <div key={s.label} style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <span style={{
                    fontFamily: 'Manrope, sans-serif', fontWeight: 800,
                    fontSize: '32px', color: '#d9e2ff', minWidth: '80px',
                  }}>{s.value}</span>
                  <div style={{ width: '1px', height: '28px', background: 'rgba(255,255,255,0.2)' }} />
                  <span style={{ fontSize: '15px', color: 'rgba(255,255,255,0.65)', fontWeight: 500 }}>
                    {s.label}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Badges */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', position: 'relative', zIndex: 1 }}>
            {['HIPAA COMPLIANT', 'FHIR R4 READY', 'JWT SECURED', 'A2A COMPATIBLE'].map((b) => (
              <span key={b} style={{
                padding: '5px 14px',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: '999px',
                fontSize: '9px', fontWeight: 700,
                letterSpacing: '0.1em',
                color: 'rgba(255,255,255,0.85)',
                background: 'rgba(255,255,255,0.06)',
              }}>{b}</span>
            ))}
          </div>
        </div>

        {/* ── RIGHT PANEL ── */}
        <div style={{
          flex: 1,
          background: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '48px 64px',
          overflowY: 'auto',
        }}>
          <div style={{ width: '100%', maxWidth: '400px' }}>

            {/* Header */}
            <div style={{ marginBottom: '36px' }}>
              <h2 style={{
                fontFamily: 'Manrope, sans-serif', fontWeight: 800,
                fontSize: '32px', color: '#001d4e',
                letterSpacing: '-0.02em', marginBottom: '8px',
              }}>Clinician Sign In</h2>
              <p style={{ fontSize: '14px', color: '#5a5e6b', lineHeight: 1.6 }}>
                Enter your hospital credentials to access the dashboard
              </p>
            </div>

            {/* Form */}
            <form onSubmit={handleLogin}>

              {/* Doctor ID */}
              <div style={{ marginBottom: '16px' }}>
                <label style={{
                  display: 'block', fontSize: '10px', fontWeight: 700,
                  textTransform: 'uppercase', letterSpacing: '0.12em',
                  color: '#747782', marginBottom: '8px',
                }}>Doctor ID</label>
                <div style={{ position: 'relative' }}>
                  <span className="material-icons-round" style={{
                    position: 'absolute', left: '14px', top: '50%',
                    transform: 'translateY(-50%)', fontSize: '18px', color: '#9ca3af',
                  }}>badge</span>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="e.g. dr.thorne"
                    required
                    style={{
                      width: '100%', padding: '13px 14px 13px 44px',
                      background: '#f2f4f6',
                      border: '2px solid transparent',
                      borderBottom: '2px solid #e1e2e4',
                      borderRadius: '6px 6px 0 0',
                      fontSize: '14px', fontFamily: 'Inter, sans-serif',
                      color: '#001d4e', outline: 'none',
                      transition: 'border-color 0.15s',
                    }}
                    onFocus={(e) => e.target.style.borderBottomColor = '#003178'}
                    onBlur={(e) => e.target.style.borderBottomColor = '#e1e2e4'}
                  />
                </div>
              </div>

              {/* Password */}
              <div style={{ marginBottom: '20px' }}>
                <label style={{
                  display: 'block', fontSize: '10px', fontWeight: 700,
                  textTransform: 'uppercase', letterSpacing: '0.12em',
                  color: '#747782', marginBottom: '8px',
                }}>Password</label>
                <div style={{ position: 'relative' }}>
                  <span className="material-icons-round" style={{
                    position: 'absolute', left: '14px', top: '50%',
                    transform: 'translateY(-50%)', fontSize: '18px', color: '#9ca3af',
                  }}>lock</span>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                    style={{
                      width: '100%', padding: '13px 14px 13px 44px',
                      background: '#f2f4f6',
                      border: '2px solid transparent',
                      borderBottom: '2px solid #e1e2e4',
                      borderRadius: '6px 6px 0 0',
                      fontSize: '14px', fontFamily: 'Inter, sans-serif',
                      color: '#001d4e', outline: 'none',
                      transition: 'border-color 0.15s',
                    }}
                    onFocus={(e) => e.target.style.borderBottomColor = '#003178'}
                    onBlur={(e) => e.target.style.borderBottomColor = '#e1e2e4'}
                  />
                </div>
              </div>

              {/* Remember + Forgot */}
              <div style={{
                display: 'flex', justifyContent: 'space-between',
                alignItems: 'center', marginBottom: '24px',
              }}>
                <label style={{
                  display: 'flex', alignItems: 'center', gap: '8px',
                  fontSize: '13px', color: '#5a5e6b', cursor: 'pointer',
                }}>
                  <input
                    type="checkbox"
                    checked={remember}
                    onChange={(e) => setRemember(e.target.checked)}
                    style={{ accentColor: '#003178', width: '14px', height: '14px' }}
                  />
                  Remember this device
                </label>
                <span style={{
                  fontSize: '13px', fontWeight: 700,
                  color: '#003178', cursor: 'pointer',
                }}>Forgot password?</span>
              </div>

              {/* Error */}
              {error && (
                <div style={{
                  display: 'flex', alignItems: 'center', gap: '8px',
                  background: '#fff1f1', border: '1px solid #fca5a5',
                  color: '#b91c1c', padding: '10px 14px',
                  borderRadius: '8px', fontSize: '13px',
                  fontWeight: 600, marginBottom: '16px',
                }}>
                  <span className="material-icons-round" style={{ fontSize: '16px' }}>error_outline</span>
                  {error}
                </div>
              )}

              {/* Submit */}
              <button
                type="submit"
                disabled={loading}
                style={{
                  width: '100%', padding: '14px',
                  background: loading ? '#94a3b8' : 'linear-gradient(90deg, #001d4e 0%, #003178 100%)',
                  color: '#fff', border: 'none', borderRadius: '8px',
                  fontSize: '15px', fontWeight: 700,
                  fontFamily: 'Manrope, sans-serif',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  transition: 'all 0.2s',
                  letterSpacing: '0.01em',
                }}
              >
                {loading ? 'Authenticating...' : 'Sign In to Dashboard'}
              </button>
            </form>

            {/* Divider */}
            <div style={{
              display: 'flex', alignItems: 'center', gap: '16px',
              margin: '28px 0',
            }}>
              <div style={{ flex: 1, height: '1px', background: '#e1e2e4' }} />
              <span style={{
                fontSize: '9px', fontWeight: 800, letterSpacing: '0.25em',
                textTransform: 'uppercase', color: '#9ca3af',
              }}>Secure Access</span>
              <div style={{ flex: 1, height: '1px', background: '#e1e2e4' }} />
            </div>

            {/* Security badges 2x2 */}
            <div style={{
              display: 'grid', gridTemplateColumns: '1fr 1fr',
              gap: '10px', marginBottom: '16px',
            }}>
              {[
                { icon: 'verified_user', label: 'HIPAA Compliant' },
                { icon: 'key', label: 'JWT Secured' },
                { icon: 'sync_alt', label: 'FHIR R4 Ready' },
                { icon: 'schedule', label: '8-Hour Session' },
              ].map((b) => (
                <div key={b.label} style={{
                  display: 'flex', alignItems: 'center', gap: '10px',
                  padding: '12px 14px', background: '#f2f4f6',
                  borderRadius: '10px',
                }}>
                  <span className="material-icons-round" style={{ fontSize: '18px', color: '#003178' }}>
                    {b.icon}
                  </span>
                  <span style={{
                    fontSize: '10px', fontWeight: 700,
                    textTransform: 'uppercase', letterSpacing: '0.08em',
                    color: '#434651',
                  }}>{b.label}</span>
                </div>
              ))}
            </div>

            {/* Demo box */}
            <div style={{
              display: 'flex', alignItems: 'flex-start', gap: '14px',
              padding: '16px 18px',
              background: '#eef2ff',
              border: '1px solid #c7d2fe',
              borderRadius: '10px', marginBottom: '20px',
            }}>
              <span className="material-icons-round" style={{ fontSize: '18px', color: '#4f6bbd', marginTop: '1px' }}>
                lightbulb
              </span>
              <div>
                <div style={{
                  fontSize: '10px', fontWeight: 700,
                  textTransform: 'uppercase', letterSpacing: '0.1em',
                  color: '#4f6bbd', marginBottom: '4px',
                }}>Demo Access</div>
                <div style={{ fontSize: '13px', color: '#535e7c', fontWeight: 500 }}>
                  dr.thorne / demo123
                </div>
              </div>
            </div>

            <p style={{
              textAlign: 'center', fontSize: '10px',
              color: '#9ca3af', fontWeight: 500,
              textTransform: 'uppercase', letterSpacing: '0.1em',
              lineHeight: 1.8,
            }}>
              This system is for authorized medical personnel only.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        padding: '16px 48px',
        background: '#f8f9fb',
        borderTop: '1px solid #e1e2e4',
        fontSize: '10px', fontWeight: 600,
        textTransform: 'uppercase', letterSpacing: '0.08em',
      }}>
        <span style={{ color: '#001d4e' }}>
          © 2026 Clinical Sentinel. HIPAA & SOC2 Compliant. Precision Medical Intelligence.
        </span>
        <div style={{ display: 'flex', gap: '24px' }}>
          {['Privacy Statement', 'Terms of Service', 'Regulatory Affairs'].map((l) => (
            <span key={l} style={{ color: '#9ca3af', cursor: 'pointer' }}>{l}</span>
          ))}
        </div>
      </footer>
    </div>
  );
}