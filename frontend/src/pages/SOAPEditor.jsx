import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';

const sections = [
  {
    key: 'subjective', icon: 'person', label: 'Subjective',
    content: 'Patient reports persistent tingling and occasional "sharp, shooting pains" in both feet, significantly worse at night. She notes a reduction in overall activity levels over the past 3 months due to discomfort. Denies any recent falls or balance issues. Adherence to Metformin (1000mg BID) is reported as consistent, though dietary management has been "challenging" during recent holiday period.',
  },
  {
    key: 'objective', icon: 'bar_chart', label: 'Objective',
    bullets: true,
    content: 'Physical Exam: Bilateral diminished vibratory sensation at the hallux.\nMonofilament testing: 4/10 sites undetected on left foot, 3/10 on right.\nLower extremity pulses: Posterior tibial 2+ bilaterally, Dorsalis pedis 1+ bilaterally.\nSkin: Dry, with minor hyperkeratosis at the 1st MTP joint. No active ulceration.',
  },
  {
    key: 'assessment', icon: 'assignment', label: 'Assessment',
    content: 'Primary Diagnosis: Diabetic Peripheral Neuropathy (ICD-10 E11.40)\n\nThe patient\'s clinical presentation and objective findings are highly suggestive of advancing diabetic peripheral neuropathy. Elevation in HbA1c (7.4%) correlates with the exacerbation of symptoms.',
  },
  {
    key: 'plan', icon: 'event_note', label: 'Plan',
    plan: [
      { label: 'Medication', text: 'Initiate Gabapentin 300mg QHS for neuropathic pain; titrate as tolerated.' },
      { label: 'Diagnostics', text: 'Order Vitamin B12 and folate levels to rule out nutritional deficiencies.' },
      { label: 'Referral', text: 'Podiatry consultation for hyperkeratosis management and diabetic foot care education.' },
      { label: 'Follow-up', text: 'Repeat HbA1c in 3 months; patient scheduled for 4-week follow-up for Gabapentin review.' },
    ],
  },
];

export default function SOAPEditor() {
  const navigate = useNavigate();

  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'Inter,sans-serif', background: '#f8f9fb' }}>
      <Sidebar />
      <div style={{ marginLeft: '220px', flex: 1 }}>

        {/* Header */}
        <div style={{ position: 'sticky', top: 0, zIndex: 30, background: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(14px)', borderBottom: '1px solid #f2f4f6', display: 'flex', alignItems: 'center', padding: '0 24px', height: '56px', gap: '16px' }}>
          <div style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '15px', color: '#003178' }}>THE CLINICAL SENTINEL</div>
          {['Active Cases', 'Alerts'].map((t, i) => (
            <div key={t} style={{ padding: '0 12px', height: '56px', display: 'flex', alignItems: 'center', fontSize: '13px', fontWeight: 500, color: '#9ca3af', cursor: 'pointer' }}>{t}</div>
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

        <div style={{ padding: '24px', display: 'grid', gridTemplateColumns: '280px 1fr', gap: '20px' }}>

          {/* LEFT */}
          <div>
            <div style={{ fontSize: '12px', color: '#9ca3af', marginBottom: '12px' }}>
              Patient Case #9982 › <span style={{ color: '#003178', fontWeight: 600 }}>Generated SOAP Note</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', flexWrap: 'wrap', gap: '8px' }}>
              <h1 style={{ fontFamily: 'Manrope,sans-serif', fontWeight: 800, fontSize: '22px', color: '#191c1e' }}>Interactive Editor</h1>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button style={{ padding: '7px 12px', background: 'none', border: '1px solid #e1e2e4', borderRadius: '8px', fontSize: '11px', fontWeight: 600, cursor: 'pointer', color: '#5a5e6b' }}>✏ Edit</button>
                <button style={{ padding: '7px 12px', background: '#f2f4f6', border: 'none', borderRadius: '8px', fontSize: '11px', fontWeight: 600, cursor: 'pointer' }}>✨ Refine</button>
                <button style={{ padding: '7px 12px', background: '#003178', border: 'none', borderRadius: '8px', fontSize: '11px', fontWeight: 600, cursor: 'pointer', color: '#fff' }}>✓ Accept</button>
              </div>
            </div>

            <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)', marginBottom: '14px' }}>
              <div style={{ display: 'flex', gap: '12px', alignItems: 'center', marginBottom: '14px' }}>
                <div style={{ width: '44px', height: '44px', borderRadius: '8px', background: '#f2f4f6', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '16px', fontWeight: 800, color: '#003178' }}>ER</div>
                <div>
                  <div style={{ fontSize: '14px', fontWeight: 700, color: '#191c1e' }}>Elena Rodriguez</div>
                  <div style={{ fontSize: '11px', color: '#9ca3af' }}>72 Years · Female</div>
                  <span style={{ fontSize: '10px', fontWeight: 700, background: 'rgba(0,49,120,0.08)', color: '#003178', padding: '2px 8px', borderRadius: '10px' }}>TYPE 2 DIABETES</span>
                </div>
              </div>
              <div style={{ fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', color: '#9ca3af', marginBottom: '6px' }}>Chief Complaint</div>
              <div style={{ fontSize: '12px', color: '#5a5e6b', lineHeight: 1.6, marginBottom: '14px' }}>Intermittent neuropathy and bilateral fatigue in lower extremities.</div>
              <div style={{ fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', color: '#9ca3af', marginBottom: '8px' }}>Vitals (Current)</div>
              <div style={{ display: 'flex', gap: '16px' }}>
                <div><div style={{ fontSize: '10px', color: '#9ca3af' }}>BP</div><div style={{ fontWeight: 700, color: '#191c1e' }}>132/84</div></div>
                <div><div style={{ fontSize: '10px', color: '#9ca3af' }}>HbA1c</div><div style={{ fontWeight: 700, color: '#ba1a1a' }}>7.4%</div></div>
              </div>
            </div>

            <div style={{ background: '#fff', borderRadius: '12px', padding: '16px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
              <div style={{ fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#003178', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '5px' }}>
                <span className="material-icons-round" style={{ fontSize: '14px' }}>auto_awesome</span> AI Confidence
              </div>
              <div style={{ height: '5px', background: '#f2f4f6', borderRadius: '3px', marginBottom: '8px' }}>
                <div style={{ height: '5px', width: '94%', background: 'linear-gradient(90deg,#003178,#0d47a1)', borderRadius: '3px' }} />
              </div>
              <div style={{ fontSize: '11px', color: '#5a5e6b', lineHeight: 1.5 }}>
                Sentinel processed 14 minutes of consultation audio with 94% accuracy.
              </div>
            </div>
          </div>

          {/* RIGHT — SOAP */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {sections.map((section) => (
              <div key={section.key} style={{ background: '#fff', borderRadius: '12px', padding: '18px 20px', boxShadow: '0 1px 4px rgba(0,0,0,0.06)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                  <span className="material-icons-round" style={{ fontSize: '16px', color: '#003178' }}>{section.icon}</span>
                  <span style={{ fontSize: '14px', fontWeight: 700, color: '#003178' }}>{section.label}</span>
                </div>
                <div style={{ fontSize: '13px', color: '#5a5e6b', lineHeight: 1.75, padding: '12px', background: '#f8f9fb', borderRadius: '8px', borderLeft: '3px solid rgba(0,49,120,0.15)' }}>
                  {section.plan ? (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      {section.plan.map((p, i) => (
                        <div key={p.label}><span style={{ fontWeight: 700, color: '#003178' }}>{i + 1}. {p.label}: </span>{p.text}</div>
                      ))}
                    </div>
                  ) : section.bullets ? (
                    <ul style={{ paddingLeft: '16px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      {section.content.split('\n').map((line, i) => <li key={i}>{line}</li>)}
                    </ul>
                  ) : (
                    section.content
                  )}
                </div>
              </div>
            ))}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0', borderTop: '1px solid #f2f4f6' }}>
              <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: '#9ca3af' }}>
                <span>💾 Auto-saved 2m ago</span>
                <span>🔒 HIPAA Compliant Session</span>
              </div>
              <span style={{ fontSize: '11px', color: '#9ca3af', fontStyle: 'italic' }}>Generated by Sentinel Engine v4.2.1</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}