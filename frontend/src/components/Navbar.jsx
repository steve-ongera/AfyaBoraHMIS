import { NavLink, useLocation } from 'react-router-dom'
import {
  LayoutDashboard, Users, UserCog, Stethoscope, BedDouble,
  FlaskConical, Pill, Siren, Baby, ShoppingCart, FileCheck,
  HeartPulse, Shield, Settings, ClipboardList, BarChart3,
  Bell, LogOut, ChevronDown, ChevronRight, Building2, Wallet,
  UserCheck, Package, Receipt, Cpu
} from 'lucide-react'
import { useState } from 'react'
import { logout } from '../utils/api'

const NAV = [
  {
    section: 'Overview',
    items: [
      { label: 'Dashboard',       icon: LayoutDashboard, to: '/dashboard' },
    ],
  },
  {
    section: 'Administration',
    items: [
      { label: 'Users & Access',  icon: UserCog,          to: '/admin/users' },
      { label: 'Audit Logs',      icon: ClipboardList,    to: '/admin/audit-logs' },
      { label: 'Settings',        icon: Settings,         to: '/admin/settings' },
    ],
  },
  {
    section: 'Clinical',
    items: [
      { label: 'Patients',        icon: Users,            to: '/patients' },
      { label: 'Appointments',    icon: Stethoscope,      to: '/appointments' },
      { label: 'Consultations',   icon: HeartPulse,       to: '/consultations' },
      { label: 'Patient Visits',  icon: ClipboardList,    to: '/visits' },
    ],
  },
  {
    section: 'Departments',
    items: [
      { label: 'Emergency',       icon: Siren,            to: '/emergency' },
      { label: 'Inpatient',       icon: BedDouble,        to: '/inpatient' },
      { label: 'Maternity & MCH', icon: Baby,             to: '/maternity' },
      { label: 'Laboratory',      icon: FlaskConical,     to: '/laboratory' },
      { label: 'Pharmacy',        icon: Pill,             to: '/pharmacy' },
      { label: 'Radiology',       icon: Cpu,              to: '/radiology' },
    ],
  },
  {
    section: 'Finance',
    items: [
      { label: 'Billing & Payments', icon: Wallet,        to: '/billing' },
      { label: 'Insurance Claims',   icon: FileCheck,     to: '/claims' },
      { label: 'SHA',                icon: Shield,        to: '/sha' },
      { label: 'eTIMS Invoices',     icon: Receipt,       to: '/etims' },
    ],
  },
  {
    section: 'Operations',
    items: [
      { label: 'Procurement',     icon: ShoppingCart,     to: '/procurement' },
      { label: 'Inventory',       icon: Package,          to: '/inventory' },
      { label: 'Assets',          icon: Building2,        to: '/assets' },
    ],
  },
  {
    section: 'HR',
    items: [
      { label: 'Attendance',      icon: UserCheck,        to: '/hr/attendance' },
      { label: 'Leave Management',icon: ClipboardList,    to: '/hr/leave' },
      { label: 'Staff Directory', icon: Users,            to: '/hr/staff' },
    ],
  },
  {
    section: 'Reports',
    items: [
      { label: 'Analytics',       icon: BarChart3,        to: '/analytics' },
      { label: 'Security',        icon: Shield,           to: '/security' },
    ],
  },
]

export default function Sidebar() {
  const location = useLocation()
  const [collapsed, setCollapsed] = useState({})
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  const toggle = (section) =>
    setCollapsed((c) => ({ ...c, [section]: !c[section] }))

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">
          <HeartPulse size={18} />
        </div>
        <div>
          <div className="sidebar-logo-name">AfyaBora</div>
          <div className="sidebar-logo-sub">HMIS v1.0</div>
        </div>
      </div>

      {/* Nav */}
      <nav className="sidebar-nav">
        {NAV.map(({ section, items }) => (
          <div key={section} className="nav-section">
            <button
              className="nav-section-header"
              onClick={() => toggle(section)}
            >
              <span>{section}</span>
              {collapsed[section] ? <ChevronRight size={13} /> : <ChevronDown size={13} />}
            </button>

            {!collapsed[section] && (
              <ul className="nav-list">
                {items.map(({ label, icon: Icon, to }) => (
                  <li key={to}>
                    <NavLink
                      to={to}
                      className={({ isActive }) =>
                        `nav-link${isActive ? ' nav-link-active' : ''}`
                      }
                    >
                      <Icon size={16} />
                      <span>{label}</span>
                    </NavLink>
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        <div className="sidebar-user">
          <div className="sidebar-avatar">
            {user.first_name?.[0]}{user.last_name?.[0]}
          </div>
          <div className="sidebar-user-info">
            <div className="sidebar-user-name">
              {user.first_name} {user.last_name}
            </div>
            <div className="sidebar-user-role">{user.user_type}</div>
          </div>
        </div>
        <button className="sidebar-logout" onClick={logout} title="Logout">
          <LogOut size={16} />
        </button>
      </div>

      <style>{`
        .sidebar {
          position: fixed;
          top: 0; left: 0;
          width: var(--sidebar-w);
          height: 100vh;
          background: var(--bg-surface);
          border-right: 1px solid var(--border);
          display: flex;
          flex-direction: column;
          z-index: 100;
          overflow: hidden;
        }

        .sidebar-logo {
          display: flex;
          align-items: center;
          gap: 11px;
          padding: 20px 20px 16px;
          border-bottom: 1px solid var(--border);
          flex-shrink: 0;
        }
        .sidebar-logo-icon {
          width: 36px; height: 36px;
          background: var(--accent-soft);
          border: 1px solid var(--border-accent);
          border-radius: 10px;
          display: flex; align-items: center; justify-content: center;
          color: var(--accent);
          flex-shrink: 0;
        }
        .sidebar-logo-name {
          font-family: var(--font-display);
          font-size: 1.1rem;
          color: var(--text-primary);
          line-height: 1.1;
        }
        .sidebar-logo-sub {
          font-size: 10.5px;
          color: var(--text-muted);
          letter-spacing: .05em;
        }

        .sidebar-nav {
          flex: 1;
          overflow-y: auto;
          padding: 10px 0 10px;
        }

        .nav-section { margin-bottom: 4px; }

        .nav-section-header {
          width: 100%;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 7px 20px 5px;
          background: none;
          border: none;
          cursor: pointer;
          font-size: 10px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: .1em;
          color: var(--text-muted);
          transition: color var(--transition);
        }
        .nav-section-header:hover { color: var(--text-secondary); }

        .nav-list { list-style: none; }

        .nav-link {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 8px 20px;
          font-size: 13.5px;
          color: var(--text-secondary);
          transition: all var(--transition);
          border-left: 2px solid transparent;
          position: relative;
        }
        .nav-link:hover {
          color: var(--text-primary);
          background: var(--bg-raised);
        }
        .nav-link-active {
          color: var(--accent) !important;
          background: var(--accent-soft);
          border-left-color: var(--accent);
          font-weight: 500;
        }

        .sidebar-footer {
          padding: 14px 16px;
          border-top: 1px solid var(--border);
          display: flex;
          align-items: center;
          gap: 10px;
          flex-shrink: 0;
        }
        .sidebar-user {
          display: flex;
          align-items: center;
          gap: 10px;
          flex: 1;
          min-width: 0;
        }
        .sidebar-avatar {
          width: 34px; height: 34px;
          background: var(--accent-soft);
          border: 1px solid var(--border-accent);
          border-radius: 8px;
          display: flex; align-items: center; justify-content: center;
          font-size: 11.5px;
          font-weight: 700;
          color: var(--accent);
          flex-shrink: 0;
          text-transform: uppercase;
        }
        .sidebar-user-info { min-width: 0; }
        .sidebar-user-name {
          font-size: 13px;
          font-weight: 500;
          color: var(--text-primary);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .sidebar-user-role {
          font-size: 10.5px;
          color: var(--text-muted);
          text-transform: uppercase;
          letter-spacing: .06em;
        }
        .sidebar-logout {
          background: none;
          border: none;
          color: var(--text-muted);
          cursor: pointer;
          padding: 6px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          transition: all var(--transition);
          flex-shrink: 0;
        }
        .sidebar-logout:hover {
          color: var(--danger);
          background: rgba(240,71,71,0.1);
        }
      `}</style>
    </aside>
  )
}