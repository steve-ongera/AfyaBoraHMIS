import { useLocation, useNavigate, Link } from 'react-router-dom'
import { Construction, ArrowLeft, Home, Clock } from 'lucide-react'

const NEARBY = [
  { label: 'Dashboard',        to: '/dashboard' },
  { label: 'Patients',         to: '/patients' },
  { label: 'Appointments',     to: '/appointments' },
  { label: 'Emergency',        to: '/emergency' },
  { label: 'Inpatient',        to: '/inpatient' },
  { label: 'Laboratory',       to: '/laboratory' },
  { label: 'Pharmacy',         to: '/pharmacy' },
  { label: 'Claims',           to: '/claims' },
  { label: 'Procurement',      to: '/procurement' },
]

export default function UnderDevelopment({ pageName }) {
  const location = useLocation()
  const navigate = useNavigate()
  const name = pageName || location.pathname.replace(/\//g, ' / ').trim() || 'This page'

  return (
    <div className="under-dev-wrap">
      {/* Animated icon */}
      <div className="ud-icon-wrap">
        <div className="ud-icon-ring" />
        <div className="ud-icon">
          <Construction size={36} strokeWidth={1.2} />
        </div>
      </div>

      <h2 className="ud-title anim-fade-up-1">Under Development</h2>
      <p className="ud-subtitle anim-fade-up-2">
        <strong style={{ color: 'var(--accent)', textTransform: 'capitalize' }}>{name}</strong>{' '}
        is currently being built. Check back soon — it's almost ready.
      </p>

      <div className="ud-eta anim-fade-up-2">
        <Clock size={13} />
        Coming in the next release
      </div>

      {/* Action buttons */}
      <div className="ud-actions anim-fade-up-3">
        <button className="btn btn-ghost" onClick={() => navigate(-1)}>
          <ArrowLeft size={15} /> Go Back
        </button>
        <Link to="/dashboard" className="btn btn-primary">
          <Home size={15} /> Dashboard
        </Link>
      </div>

      {/* Quick links */}
      <div className="ud-links anim-fade-up-4">
        <p className="ud-links-label">Jump to a ready page</p>
        <div className="ud-links-grid">
          {NEARBY.filter((n) => n.to !== location.pathname).map((n) => (
            <Link key={n.to} to={n.to} className="ud-chip">
              {n.label}
            </Link>
          ))}
        </div>
      </div>

      <style>{`
        .ud-icon-wrap {
          position: relative;
          width: 90px; height: 90px;
          display: flex; align-items: center; justify-content: center;
          margin-bottom: 28px;
        }
        .ud-icon-ring {
          position: absolute; inset: 0;
          border-radius: 50%;
          border: 1px solid var(--border-accent);
          animation: ud-pulse 2.4s ease-in-out infinite;
        }
        @keyframes ud-pulse {
          0%,100% { transform: scale(1); opacity: .5; }
          50%      { transform: scale(1.12); opacity: .15; }
        }
        .ud-icon {
          width: 80px; height: 80px;
          background: var(--accent-soft);
          border: 1px solid var(--border-accent);
          border-radius: 22px;
          display: flex; align-items: center; justify-content: center;
          color: var(--accent);
          animation: fadeUp .5s ease both;
        }

        .ud-title {
          font-size: 1.9rem;
          margin-bottom: 12px;
        }
        .ud-subtitle {
          font-size: 14.5px;
          color: var(--text-muted);
          max-width: 400px;
          margin-bottom: 14px;
        }
        .ud-eta {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          font-size: 12px;
          color: var(--text-muted);
          background: var(--bg-raised);
          border: 1px solid var(--border);
          border-radius: 99px;
          padding: 4px 14px;
          margin-bottom: 32px;
        }

        .ud-actions {
          display: flex;
          gap: 12px;
          margin-bottom: 48px;
        }

        .ud-links {
          max-width: 520px;
          width: 100%;
        }
        .ud-links-label {
          font-size: 11px;
          text-transform: uppercase;
          letter-spacing: .08em;
          color: var(--text-muted);
          margin-bottom: 14px;
        }
        .ud-links-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          justify-content: center;
        }
        .ud-chip {
          background: var(--bg-raised);
          border: 1px solid var(--border);
          border-radius: 8px;
          padding: 6px 14px;
          font-size: 13px;
          color: var(--text-secondary);
          transition: all var(--transition);
        }
        .ud-chip:hover {
          color: var(--accent);
          border-color: var(--border-accent);
          background: var(--accent-soft);
        }
      `}</style>
    </div>
  )
}