import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { HeartPulse, Eye, EyeOff, Loader2, AlertCircle } from 'lucide-react'
import { authApi } from '../utils/api'

export default function Login() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [showPw, setShowPw] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handle = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const submit = async (e) => {
    e.preventDefault()
    if (!form.username || !form.password) { setError('Please fill in all fields.'); return }
    setLoading(true); setError('')
    try {
      const { data } = await authApi.login(form)
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      const { data: me } = await authApi.me()
      localStorage.setItem('user', JSON.stringify(me))
      navigate('/dashboard')
    } catch (err) {
      setError(
        err.response?.status === 401
          ? 'Invalid username or password.'
          : 'Connection error. Please try again.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-root">
      {/* Background grid */}
      <div className="login-bg" aria-hidden />

      <div className="login-card anim-fade-up">
        {/* Brand */}
        <div className="login-brand">
          <div className="login-brand-icon">
            <HeartPulse size={26} strokeWidth={1.5} />
          </div>
          <h1 className="login-title">AfyaBora</h1>
          <p className="login-subtitle">Hospital Management Information System</p>
        </div>

        {/* Divider */}
        <div className="login-divider" />

        {/* Form */}
        <form onSubmit={submit} className="login-form" autoComplete="off">
          {error && (
            <div className="alert alert-danger anim-fade-up" style={{ marginBottom: 18 }}>
              <AlertCircle size={15} />
              {error}
            </div>
          )}

          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              className="form-input"
              name="username"
              value={form.username}
              onChange={handle}
              placeholder="Enter your username"
              autoFocus
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <div style={{ position: 'relative' }}>
              <input
                className="form-input"
                name="password"
                type={showPw ? 'text' : 'password'}
                value={form.password}
                onChange={handle}
                placeholder="Enter your password"
                autoComplete="current-password"
                style={{ paddingRight: 42 }}
              />
              <button
                type="button"
                onClick={() => setShowPw(!showPw)}
                style={{
                  position: 'absolute', right: 12, top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'none', border: 'none',
                  color: 'var(--text-muted)', cursor: 'pointer',
                  display: 'flex', alignItems: 'center',
                }}
              >
                {showPw ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-lg"
            disabled={loading}
            style={{ width: '100%', justifyContent: 'center', marginTop: 6 }}
          >
            {loading ? <Loader2 size={17} className="spin" /> : null}
            {loading ? 'Signing in…' : 'Sign In'}
          </button>
        </form>

        <p className="login-footer-note">
          AfyaBora HMIS · Level 5 Facility · &copy; {new Date().getFullYear()}
        </p>
      </div>

      <style>{`
        .login-root {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          background: var(--bg-base);
          position: relative;
          overflow: hidden;
        }

        .login-bg {
          position: absolute; inset: 0;
          background-image:
            linear-gradient(rgba(14,207,176,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(14,207,176,0.03) 1px, transparent 1px);
          background-size: 40px 40px;
          pointer-events: none;
        }
        .login-bg::before {
          content: '';
          position: absolute; inset: 0;
          background: radial-gradient(ellipse 60% 50% at 50% 50%,
            rgba(14,207,176,0.06) 0%, transparent 70%);
        }

        .login-card {
          position: relative;
          width: 100%;
          max-width: 420px;
          background: var(--bg-surface);
          border: 1px solid var(--border);
          border-radius: 20px;
          padding: 44px 40px 36px;
          box-shadow: 0 24px 80px rgba(0,0,0,0.5), 0 0 0 1px var(--border);
          margin: 20px;
        }

        .login-brand {
          text-align: center;
          margin-bottom: 24px;
        }
        .login-brand-icon {
          width: 60px; height: 60px;
          background: var(--accent-soft);
          border: 1px solid var(--border-accent);
          border-radius: 16px;
          display: flex; align-items: center; justify-content: center;
          color: var(--accent);
          margin: 0 auto 16px;
          position: relative;
        }
        .login-brand-icon::after {
          content: '';
          position: absolute; inset: -6px;
          border-radius: 22px;
          border: 1px solid var(--border-accent);
          opacity: 0.4;
          animation: pulse-ring 2.5s ease-in-out infinite;
        }
        .login-title {
          font-family: var(--font-display);
          font-size: 2rem;
          color: var(--text-primary);
          margin-bottom: 4px;
        }
        .login-subtitle {
          font-size: 12.5px;
          color: var(--text-muted);
          letter-spacing: .03em;
        }

        .login-divider {
          height: 1px;
          background: var(--border);
          margin-bottom: 28px;
        }

        .login-form { }

        .login-footer-note {
          text-align: center;
          font-size: 11px;
          color: var(--text-muted);
          margin-top: 28px;
        }

        .spin {
          animation: spin 0.8s linear infinite;
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}