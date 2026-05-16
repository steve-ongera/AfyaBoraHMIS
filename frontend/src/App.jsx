import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { Suspense, lazy } from 'react'

import Sidebar from './components/Sidebar'
import Navbar  from './components/Navbar'

// Eagerly loaded (always needed)
import Login           from './pages/Login'
import Dashboard       from './pages/admin/Dashboard'
import Users           from './pages/admin/Users'
import Settings        from './pages/admin/Settings'
import AuditLogs       from './pages/admin/AuditLogs'
import UnderDevelopment from './pages/UnderDevelopment'

// ── Auth guard ───────────────────────────────────────────────
function RequireAuth({ children }) {
  const token = localStorage.getItem('access_token')
  const location = useLocation()
  if (!token) return <Navigate to="/login" state={{ from: location }} replace />
  return children
}

// ── Shell that wraps protected pages ─────────────────────────
function AppShell({ children, title }) {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content">
        {children}
      </main>
    </div>
  )
}

// ── Under Development shorthand ───────────────────────────────
const UD = ({ name }) => (
  <AppShell>
    <Navbar title={name} />
    <div className="page-body">
      <UnderDevelopment pageName={name} />
    </div>
  </AppShell>
)

// ── App ───────────────────────────────────────────────────────
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public */}
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />

        {/* Protected — Admin */}
        <Route path="/dashboard" element={
          <RequireAuth>
            <AppShell title="Dashboard">
              <Dashboard />
            </AppShell>
          </RequireAuth>
        } />
        <Route path="/admin/users" element={
          <RequireAuth>
            <AppShell>
              <Users />
            </AppShell>
          </RequireAuth>
        } />
        <Route path="/admin/audit-logs" element={
          <RequireAuth>
            <AppShell>
              <AuditLogs />
            </AppShell>
          </RequireAuth>
        } />
        <Route path="/admin/settings" element={
          <RequireAuth>
            <AppShell>
              <Settings />
            </AppShell>
          </RequireAuth>
        } />

        {/* Under Development — Clinical */}
        <Route path="/patients"        element={<RequireAuth><UD name="Patients" /></RequireAuth>} />
        <Route path="/appointments"    element={<RequireAuth><UD name="Appointments" /></RequireAuth>} />
        <Route path="/consultations"   element={<RequireAuth><UD name="Consultations" /></RequireAuth>} />
        <Route path="/visits"          element={<RequireAuth><UD name="Patient Visits" /></RequireAuth>} />

        {/* Under Development — Departments */}
        <Route path="/emergency"       element={<RequireAuth><UD name="Emergency Department" /></RequireAuth>} />
        <Route path="/inpatient"       element={<RequireAuth><UD name="Inpatient / Wards" /></RequireAuth>} />
        <Route path="/maternity"       element={<RequireAuth><UD name="Maternity & MCH" /></RequireAuth>} />
        <Route path="/laboratory"      element={<RequireAuth><UD name="Laboratory" /></RequireAuth>} />
        <Route path="/pharmacy"        element={<RequireAuth><UD name="Pharmacy" /></RequireAuth>} />
        <Route path="/radiology"       element={<RequireAuth><UD name="Radiology & Imaging" /></RequireAuth>} />

        {/* Under Development — Finance */}
        <Route path="/billing"         element={<RequireAuth><UD name="Billing & Payments" /></RequireAuth>} />
        <Route path="/claims"          element={<RequireAuth><UD name="Insurance Claims" /></RequireAuth>} />
        <Route path="/sha"             element={<RequireAuth><UD name="SHA Integration" /></RequireAuth>} />
        <Route path="/etims"           element={<RequireAuth><UD name="eTIMS Invoices" /></RequireAuth>} />

        {/* Under Development — Operations */}
        <Route path="/procurement"     element={<RequireAuth><UD name="Procurement" /></RequireAuth>} />
        <Route path="/inventory"       element={<RequireAuth><UD name="Inventory Management" /></RequireAuth>} />
        <Route path="/assets"          element={<RequireAuth><UD name="Asset Management" /></RequireAuth>} />

        {/* Under Development — HR */}
        <Route path="/hr/attendance"   element={<RequireAuth><UD name="Attendance" /></RequireAuth>} />
        <Route path="/hr/leave"        element={<RequireAuth><UD name="Leave Management" /></RequireAuth>} />
        <Route path="/hr/staff"        element={<RequireAuth><UD name="Staff Directory" /></RequireAuth>} />

        {/* Under Development — Reports */}
        <Route path="/analytics"       element={<RequireAuth><UD name="Analytics & Reports" /></RequireAuth>} />
        <Route path="/security"        element={<RequireAuth><UD name="Security Dashboard" /></RequireAuth>} />

        {/* 404 fallback */}
        <Route path="*" element={<RequireAuth><UD name="Page Not Found" /></RequireAuth>} />
      </Routes>
    </BrowserRouter>
  )
}