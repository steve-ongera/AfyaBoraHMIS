


import { Bell, Search, RefreshCw } from 'lucide-react'
import { useState, useEffect } from 'react'
import { notificationsApi } from '../utils/api'

export default function Navbar({ title = '' }) {
  const [unread, setUnread] = useState(0)
  const [time, setTime]     = useState(new Date())

  useEffect(() => {
    const tick = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(tick)
  }, [])

  useEffect(() => {
    notificationsApi.unread()
      .then(({ data }) => setUnread(data.count || 0))
      .catch(() => {})
  }, [])

  const fmt = (d) =>
    d.toLocaleString('en-KE', {
      weekday: 'short', day: '2-digit', month: 'short',
      hour: '2-digit', minute: '2-digit', second: '2-digit',
      hour12: false,
    })

  return (
    <header className="navbar">
      <div className="navbar-left">
        <span className="navbar-breadcrumb">{title}</span>
      </div>

      <div className="navbar-center">
        <div className="navbar-search">
          <Search size={14} />
          <input placeholder="Search patients, visits, orders…" />
        </div>
      </div>

      <div className="navbar-right">
        <div className="navbar-time">{fmt(time)}</div>

        <button className="nav-icon-btn" title="Refresh" onClick={() => window.location.reload()}>
          <RefreshCw size={16} />
        </button>

        <button className="nav-icon-btn nav-bell" title="Notifications">
          <Bell size={16} />
          {unread > 0 && <span className="bell-badge">{unread > 99 ? '99+' : unread}</span>}
        </button>
      </div>

      <style>{`
        .navbar {
          position: fixed;
          top: 0;
          left: var(--sidebar-w);
          right: 0;
          height: var(--navbar-h);
          background: var(--bg-surface);
          border-bottom: 1px solid var(--border);
          display: flex;
          align-items: center;
          padding: 0 24px;
          gap: 16px;
          z-index: 90;
          backdrop-filter: blur(8px);
        }

        .navbar-left { flex-shrink: 0; }
        .navbar-breadcrumb {
          font-size: 13px;
          color: var(--text-muted);
          font-weight: 500;
          letter-spacing: .03em;
        }

        .navbar-center {
          flex: 1;
          display: flex;
          justify-content: center;
        }
        .navbar-search {
          display: flex;
          align-items: center;
          gap: 9px;
          background: var(--bg-raised);
          border: 1px solid var(--border);
          border-radius: 8px;
          padding: 7px 14px;
          width: 340px;
          color: var(--text-muted);
          transition: border-color var(--transition);
        }
        .navbar-search:focus-within {
          border-color: var(--accent);
          color: var(--text-primary);
        }
        .navbar-search input {
          background: none;
          border: none;
          outline: none;
          font-family: var(--font-body);
          font-size: 13.5px;
          color: var(--text-primary);
          width: 100%;
        }
        .navbar-search input::placeholder { color: var(--text-muted); }

        .navbar-right {
          display: flex;
          align-items: center;
          gap: 8px;
          flex-shrink: 0;
        }

        .navbar-time {
          font-size: 12px;
          color: var(--text-muted);
          font-variant-numeric: tabular-nums;
          letter-spacing: .03em;
          padding-right: 8px;
          border-right: 1px solid var(--border);
          margin-right: 4px;
        }

        .nav-icon-btn {
          position: relative;
          background: none;
          border: 1px solid var(--border);
          border-radius: 8px;
          width: 34px; height: 34px;
          display: flex; align-items: center; justify-content: center;
          cursor: pointer;
          color: var(--text-muted);
          transition: all var(--transition);
        }
        .nav-icon-btn:hover {
          color: var(--text-primary);
          background: var(--bg-raised);
          border-color: var(--border-accent);
        }

        .nav-bell .bell-badge {
          position: absolute;
          top: -4px; right: -4px;
          background: var(--danger);
          color: #fff;
          font-size: 9.5px;
          font-weight: 700;
          border-radius: 99px;
          padding: 1px 4px;
          min-width: 16px;
          text-align: center;
          line-height: 14px;
        }

        @media (max-width: 900px) {
          .navbar { left: 0; }
          .navbar-center { display: none; }
        }
      `}</style>
    </header>
  )
}