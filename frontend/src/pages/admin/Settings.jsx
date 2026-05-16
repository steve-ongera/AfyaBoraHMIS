import { useState, useEffect } from 'react'
import { Save, RefreshCw, Globe, Shield, Bell, Database, Zap } from 'lucide-react'
import Navbar from '../../components/Navbar'
import { settingsApi } from '../../utils/api'

const Tab = ({ active, onClick, icon: Icon, label }) => (
  <button
    onClick={onClick}
    style={{
      display: 'flex', alignItems: 'center', gap: 8,
      padding: '9px 16px', borderRadius: 8,
      background: active ? 'var(--accent-soft)' : 'transparent',
      border: active ? '1px solid var(--border-accent)' : '1px solid transparent',
      color: active ? 'var(--accent)' : 'var(--text-muted)',
      cursor: 'pointer', fontSize: 13.5, fontFamily: 'var(--font-body)',
      transition: 'all 180ms ease',
      whiteSpace: 'nowrap',
    }}
  >
    <Icon size={15} /> {label}
  </button>
)

export default function Settings() {
  const [tab, setTab]       = useState('clinic')
  const [clinic, setClinic] = useState({ clinic_name: '', address: '', phone_number: '', email: '', appointment_duration: 30, max_patients_per_day: 20 })
  const [etims, setEtims]   = useState({ tin_number: '', business_name: '', branch_name: '', test_mode: true, auto_submit_invoices: false })
  const [loading, setLoading] = useState(false)
  const [saved, setSaved]   = useState(false)
  const [clinicId, setClinicId] = useState(null)

  useEffect(() => {
    settingsApi.clinic().then(({ data }) => {
      const item = data.results?.[0] || data[0] || data
      if (item) { setClinic(item); setClinicId(item.id) }
    }).catch(() => {})
    settingsApi.etims().then(({ data }) => {
      const item = data.results?.[0] || data[0] || data
      if (item) setEtims(item)
    }).catch(() => {})
  }, [])

  const handleSave = async () => {
    setLoading(true)
    try {
      if (tab === 'clinic' && clinicId) await settingsApi.updateClinic(clinicId, clinic)
      setSaved(true)
      setTimeout(() => setSaved(false), 2500)
    } catch (e) {}
    finally { setLoading(false) }
  }

  const Field = ({ label, value, onChange, type = 'text', hint }) => (
    <div className="form-group">
      <label className="form-label">{label}</label>
      <input className="form-input" type={type} value={value ?? ''} onChange={e => onChange(e.target.value)} />
      {hint && <div style={{ fontSize: 11.5, color: 'var(--text-muted)', marginTop: 4 }}>{hint}</div>}
    </div>
  )

  const Toggle = ({ label, value, onChange, hint }) => (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '14px 0', borderBottom: '1px solid var(--border)' }}>
      <div>
        <div style={{ fontSize: 14, color: 'var(--text-primary)', fontWeight: 500 }}>{label}</div>
        {hint && <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>{hint}</div>}
      </div>
      <button
        onClick={() => onChange(!value)}
        style={{
          width: 44, height: 24, borderRadius: 99, border: 'none',
          background: value ? 'var(--accent)' : 'var(--bg-overlay)',
          position: 'relative', cursor: 'pointer', transition: 'background 200ms',
          flexShrink: 0,
        }}
      >
        <span style={{
          position: 'absolute', top: 3,
          left: value ? 'calc(100% - 21px)' : 3,
          width: 18, height: 18,
          background: '#fff', borderRadius: 99,
          transition: 'left 200ms',
        }} />
      </button>
    </div>
  )

  const TABS = [
    { id: 'clinic',   label: 'Clinic Info',  icon: Globe },
    { id: 'etims',    label: 'eTIMS / KRA',  icon: Database },
    { id: 'security', label: 'Security',     icon: Shield },
    { id: 'notify',   label: 'Notifications',icon: Bell },
    { id: 'system',   label: 'System',       icon: Zap },
  ]

  return (
    <>
      <Navbar title="Admin / Settings" />
      <div className="page-body">
        <div className="page-header anim-fade-up">
          <div>
            <h1 className="page-title">System Settings</h1>
            <p className="page-subtitle">Configure AfyaBora HMIS facility-wide settings</p>
          </div>
          {saved && <span className="badge badge-success"><Save size={11} /> Saved</span>}
        </div>

        <div style={{ display: 'flex', gap: 24 }} className="anim-fade-up-1">
          {/* Sidebar tabs */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4, width: 200, flexShrink: 0 }}>
            {TABS.map(t => (
              <Tab key={t.id} active={tab === t.id} onClick={() => setTab(t.id)} icon={t.icon} label={t.label} />
            ))}
          </div>

          {/* Content */}
          <div className="card" style={{ flex: 1 }}>
            {/* Clinic */}
            {tab === 'clinic' && (
              <>
                <h3 style={{ fontFamily: 'var(--font-display)', marginBottom: 24, fontSize: '1.25rem' }}>Clinic Information</h3>
                <div className="grid-2">
                  <Field label="Clinic Name"  value={clinic.clinic_name}  onChange={v => setClinic({...clinic, clinic_name: v})} />
                  <Field label="Phone Number" value={clinic.phone_number} onChange={v => setClinic({...clinic, phone_number: v})} />
                  <Field label="Email"        value={clinic.email}        onChange={v => setClinic({...clinic, email: v})} type="email" />
                  <Field label="Appointment Duration (min)" value={clinic.appointment_duration} onChange={v => setClinic({...clinic, appointment_duration: v})} type="number" />
                  <Field label="Max Patients Per Day" value={clinic.max_patients_per_day} onChange={v => setClinic({...clinic, max_patients_per_day: v})} type="number" />
                </div>
                <div className="form-group">
                  <label className="form-label">Address</label>
                  <textarea className="form-input" rows={3} value={clinic.address ?? ''} onChange={e => setClinic({...clinic, address: e.target.value})} />
                </div>
              </>
            )}

            {/* eTIMS */}
            {tab === 'etims' && (
              <>
                <h3 style={{ fontFamily: 'var(--font-display)', marginBottom: 24, fontSize: '1.25rem' }}>eTIMS / KRA Configuration</h3>
                <div className="grid-2">
                  <Field label="TIN Number"    value={etims.tin_number}    onChange={v => setEtims({...etims, tin_number: v})} />
                  <Field label="Business Name" value={etims.business_name} onChange={v => setEtims({...etims, business_name: v})} />
                  <Field label="Branch Name"   value={etims.branch_name}   onChange={v => setEtims({...etims, branch_name: v})} />
                </div>
                <div className="divider" />
                <Toggle label="Test Mode"             value={etims.test_mode}             onChange={v => setEtims({...etims, test_mode: v})}             hint="Use KRA sandbox environment (disable in production)" />
                <Toggle label="Auto-submit Invoices"  value={etims.auto_submit_invoices}  onChange={v => setEtims({...etims, auto_submit_invoices: v})}  hint="Automatically submit invoices to KRA eTIMS upon creation" />
              </>
            )}

            {/* Security — static for now */}
            {tab === 'security' && (
              <>
                <h3 style={{ fontFamily: 'var(--font-display)', marginBottom: 24, fontSize: '1.25rem' }}>Security Settings</h3>
                <Toggle label="Two-Factor Authentication" value={true}  onChange={() => {}} hint="Require 2FA code on login for all staff" />
                <Toggle label="Account Lockout"           value={true}  onChange={() => {}} hint="Lock accounts after 5 failed login attempts" />
                <Toggle label="Audit Logging"             value={true}  onChange={() => {}} hint="Record all create / update / delete actions" />
                <Toggle label="Session Timeout (8 hrs)"  value={true}  onChange={() => {}} hint="Auto-logout idle sessions after one shift" />
                <div className="alert alert-info" style={{ marginTop: 20 }}>
                  <Shield size={15} /> Security policies are also controlled via Django settings.py. Changes here affect database-level toggles only.
                </div>
              </>
            )}

            {/* Notifications */}
            {tab === 'notify' && (
              <>
                <h3 style={{ fontFamily: 'var(--font-display)', marginBottom: 24, fontSize: '1.25rem' }}>Notification Preferences</h3>
                <Toggle label="Low Stock Alerts"       value={true}  onChange={() => {}} hint="Alert pharmacists when medicines reach reorder level" />
                <Toggle label="Critical Lab Results"   value={true}  onChange={() => {}} hint="Immediately notify ordering doctor of critical values" />
                <Toggle label="Appointment Reminders"  value={true}  onChange={() => {}} hint="Send SMS reminders 24 hours before appointments" />
                <Toggle label="Insurance Claim Updates"value={false} onChange={() => {}} hint="Notify claims officers of status changes" />
              </>
            )}

            {/* System */}
            {tab === 'system' && (
              <>
                <h3 style={{ fontFamily: 'var(--font-display)', marginBottom: 24, fontSize: '1.25rem' }}>System Configuration</h3>
                <div className="grid-2">
                  <div className="card card-sm" style={{ background: 'var(--bg-raised)' }}>
                    <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '.07em', marginBottom: 6 }}>Backend</div>
                    <div style={{ fontSize: 14, color: 'var(--text-primary)' }}>Django 5.x + DRF</div>
                  </div>
                  <div className="card card-sm" style={{ background: 'var(--bg-raised)' }}>
                    <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '.07em', marginBottom: 6 }}>Frontend</div>
                    <div style={{ fontSize: 14, color: 'var(--text-primary)' }}>React 18 + Vite</div>
                  </div>
                  <div className="card card-sm" style={{ background: 'var(--bg-raised)' }}>
                    <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '.07em', marginBottom: 6 }}>Database</div>
                    <div style={{ fontSize: 14, color: 'var(--text-primary)' }}>PostgreSQL</div>
                  </div>
                  <div className="card card-sm" style={{ background: 'var(--bg-raised)' }}>
                    <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '.07em', marginBottom: 6 }}>Auth</div>
                    <div style={{ fontSize: 14, color: 'var(--text-primary)' }}>JWT + 2FA</div>
                  </div>
                </div>
              </>
            )}

            {/* Save */}
            {(tab === 'clinic' || tab === 'etims') && (
              <div style={{ marginTop: 28, display: 'flex', gap: 10 }}>
                <button className="btn btn-primary" disabled={loading} onClick={handleSave}>
                  <Save size={14} /> {loading ? 'Saving…' : 'Save Changes'}
                </button>
                <button className="btn btn-ghost">Discard</button>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}