import { useState, useEffect } from 'react'
import {
  Users, BedDouble, FlaskConical, Siren, Pill,
  TrendingUp, Activity, AlertTriangle, CheckCircle2,
  Clock, Stethoscope,
} from 'lucide-react'
import {
  AreaChart, Area, BarChart, Bar, XAxis, YAxis,
  Tooltip, ResponsiveContainer, CartesianGrid,
} from 'recharts'
import Navbar from '../../components/Navbar'
import { dashboardApi } from '../../utils/api'

// ── Helpers ──────────────────────────────────────────────────
const COLORS = {
  teal: '#0ecfb0', red: '#f04747', yellow: '#f5a623',
  blue: '#4a9eff', green: '#22d36e',
}

// Fake trend data (replace with a real endpoint)
const trendData = [
  { day: 'Mon', visits: 38, admissions: 7, lab: 22 },
  { day: 'Tue', visits: 52, admissions: 11, lab: 31 },
  { day: 'Wed', visits: 44, admissions: 8,  lab: 27 },
  { day: 'Thu', visits: 61, admissions: 14, lab: 40 },
  { day: 'Fri', visits: 55, admissions: 10, lab: 35 },
  { day: 'Sat', visits: 29, admissions: 5,  lab: 18 },
  { day: 'Sun', visits: 22, admissions: 4,  lab: 12 },
]

const claimData = [
  { name: 'Consultation', pending: 12, approved: 45, paid: 38 },
  { name: 'Pharmacy',     pending: 8,  approved: 30, paid: 22 },
  { name: 'Inpatient',    pending: 5,  approved: 18, paid: 14 },
  { name: 'SHA',          pending: 3,  approved: 12, paid: 10 },
]

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: 'var(--bg-overlay)',
      border: '1px solid var(--border)',
      borderRadius: 10,
      padding: '10px 14px',
      fontSize: 12.5,
    }}>
      <div style={{ color: 'var(--text-muted)', marginBottom: 6 }}>{label}</div>
      {payload.map((p) => (
        <div key={p.dataKey} style={{ color: p.color, marginBottom: 2 }}>
          {p.name}: <strong>{p.value}</strong>
        </div>
      ))}
    </div>
  )
}

function StatCard({ label, value, sub, icon: Icon, color = COLORS.teal, delay = 0 }) {
  return (
    <div className="stat-card" style={{ animationDelay: `${delay}ms` }}>
      <div className="stat-label">{label}</div>
      <div className="stat-value" style={{ color }}>{value ?? '—'}</div>
      {sub && <div className="stat-sub">{sub}</div>}
      <div className="stat-icon">
        <Icon size={48} strokeWidth={0.8} />
      </div>
    </div>
  )
}

// ── Component ────────────────────────────────────────────────
export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  useEffect(() => {
    dashboardApi.stats()
      .then(({ data }) => setStats(data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const Sk = ({ w = '100%', h = 22 }) => (
    <div className="skeleton" style={{ width: w, height: h, borderRadius: 6 }} />
  )

  return (
    <>
      <Navbar title="Dashboard" />
      <div className="page-body">
        {/* Header */}
        <div className="page-header anim-fade-up">
          <div>
            <h1 className="page-title">Good morning, {user.first_name || 'Doctor'} 👋</h1>
            <p className="page-subtitle">
              {new Date().toLocaleDateString('en-KE', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}
              &nbsp;· AfyaBora Level 5 Hospital
            </p>
          </div>
        </div>

        {/* ── Today's Stats ── */}
        <div className="section-header anim-fade-up-1">
          <span className="section-title">Today at a Glance</span>
          <span className="badge badge-accent"><Activity size={11} /> Live</span>
        </div>

        <div className="stat-grid anim-fade-up-1">
          {loading ? (
            Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="stat-card"><Sk /><Sk h={40} /><Sk w="60%" /></div>
            ))
          ) : (
            <>
              <StatCard label="Today's Visits"       value={stats?.today?.visits}       sub="Patient visits registered today"    icon={Users}       delay={0} />
              <StatCard label="Appointments"          value={stats?.today?.appointments} sub="Scheduled for today"                icon={Stethoscope} delay={50} color={COLORS.blue} />
              <StatCard label="Lab Orders"            value={stats?.today?.lab_orders}   sub="Orders placed today"                icon={FlaskConical}delay={100} color={COLORS.yellow} />
              <StatCard label="Admissions"            value={stats?.today?.admissions}   sub="New inpatient admissions"           icon={BedDouble}   delay={150} color={COLORS.green} />
              <StatCard label="Emergency Visits"      value={stats?.today?.emergency_visits} sub="Emergency cases today"         icon={Siren}       delay={200} color={COLORS.red} />
              <StatCard label="Pending Prescriptions" value={stats?.active?.pending_prescriptions} sub="Awaiting dispensing"     icon={Pill}        delay={250} color={COLORS.teal} />
            </>
          )}
        </div>

        {/* ── Active Status ── */}
        <div className="section-header anim-fade-up-2" style={{ marginTop: 8 }}>
          <span className="section-title">Active Right Now</span>
        </div>

        <div className="grid-4 anim-fade-up-2" style={{ marginBottom: 32 }}>
          {[
            { label: 'Active Inpatients',    val: stats?.active?.inpatients,         icon: BedDouble,    color: COLORS.blue },
            { label: 'In Emergency',         val: stats?.active?.emergency,           icon: Siren,        color: COLORS.red },
            { label: 'Pending Lab Orders',   val: stats?.active?.pending_lab_orders,  icon: FlaskConical, color: COLORS.yellow },
            { label: 'Available Beds',       val: stats?.beds?.available,             icon: BedDouble,    color: COLORS.green },
          ].map(({ label, val, icon: Icon, color }) => (
            <div key={label} className="card card-sm" style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
              <div style={{
                width: 42, height: 42, borderRadius: 12,
                background: `${color}14`,
                border: `1px solid ${color}30`,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                color, flexShrink: 0,
              }}>
                <Icon size={18} />
              </div>
              <div>
                <div style={{ fontSize: 22, fontFamily: 'var(--font-display)', color: 'var(--text-primary)', lineHeight: 1 }}>
                  {loading ? <Sk w={40} h={22} /> : (val ?? '—')}
                </div>
                <div style={{ fontSize: 11.5, color: 'var(--text-muted)', marginTop: 3 }}>{label}</div>
              </div>
            </div>
          ))}
        </div>

        {/* ── Charts ── */}
        <div className="grid-2 anim-fade-up-3" style={{ marginBottom: 32 }}>
          {/* Weekly trend */}
          <div className="card">
            <div className="section-header" style={{ marginBottom: 20 }}>
              <span className="section-title">7-Day Activity Trend</span>
              <span className="badge badge-muted">This week</span>
            </div>
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={trendData} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="gVisits" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor={COLORS.teal}  stopOpacity={0.25} />
                    <stop offset="95%" stopColor={COLORS.teal}  stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gLab" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor={COLORS.blue}  stopOpacity={0.2} />
                    <stop offset="95%" stopColor={COLORS.blue}  stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="var(--border)" strokeDasharray="4 4" vertical={false} />
                <XAxis dataKey="day" tick={{ fill: 'var(--text-muted)', fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: 'var(--text-muted)', fontSize: 11 }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="visits" name="Visits" stroke={COLORS.teal} fill="url(#gVisits)" strokeWidth={2} dot={false} />
                <Area type="monotone" dataKey="lab" name="Lab Orders" stroke={COLORS.blue} fill="url(#gLab)" strokeWidth={2} dot={false} />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* Claims */}
          <div className="card">
            <div className="section-header" style={{ marginBottom: 20 }}>
              <span className="section-title">Insurance Claims Status</span>
              <span className="badge badge-muted">All types</span>
            </div>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={claimData} margin={{ top: 5, right: 5, left: -20, bottom: 0 }} barSize={10} barGap={3}>
                <CartesianGrid stroke="var(--border)" strokeDasharray="4 4" vertical={false} />
                <XAxis dataKey="name" tick={{ fill: 'var(--text-muted)', fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: 'var(--text-muted)', fontSize: 11 }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="pending"  name="Pending"  fill={COLORS.yellow} radius={[4,4,0,0]} />
                <Bar dataKey="approved" name="Approved" fill={COLORS.teal}   radius={[4,4,0,0]} />
                <Bar dataKey="paid"     name="Paid"     fill={COLORS.green}  radius={[4,4,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* ── Bottom row ── */}
        <div className="grid-2 anim-fade-up-4">
          {/* Beds occupancy */}
          <div className="card">
            <div className="section-header" style={{ marginBottom: 16 }}>
              <span className="section-title">Bed Occupancy</span>
              <span className="badge badge-accent">
                <Activity size={10} /> Live
              </span>
            </div>
            {loading ? (
              <Sk h={80} />
            ) : (
              <>
                <div style={{ display: 'flex', gap: 24, marginBottom: 16 }}>
                  {[
                    { label: 'Total',     val: stats?.beds?.total,     color: 'var(--text-muted)' },
                    { label: 'Occupied',  val: stats?.beds?.occupied,  color: COLORS.red },
                    { label: 'Available', val: stats?.beds?.available, color: COLORS.green },
                  ].map(({ label, val, color }) => (
                    <div key={label}>
                      <div style={{ fontSize: 24, fontFamily: 'var(--font-display)', color, lineHeight: 1 }}>{val ?? '—'}</div>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 3 }}>{label}</div>
                    </div>
                  ))}
                </div>
                <div style={{ background: 'var(--bg-raised)', borderRadius: 99, height: 8, overflow: 'hidden' }}>
                  <div style={{
                    height: '100%',
                    width: `${stats?.beds?.total ? Math.round((stats.beds.occupied / stats.beds.total) * 100) : 0}%`,
                    background: `linear-gradient(90deg, ${COLORS.teal}, ${COLORS.blue})`,
                    borderRadius: 99,
                    transition: 'width 1s ease',
                  }} />
                </div>
                <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 6 }}>
                  {stats?.beds?.total
                    ? `${Math.round((stats.beds.occupied / stats.beds.total) * 100)}% occupancy rate`
                    : 'No bed data'}
                </div>
              </>
            )}
          </div>

          {/* Pending claims alerts */}
          <div className="card">
            <div className="section-header" style={{ marginBottom: 16 }}>
              <span className="section-title">Claims Requiring Attention</span>
              <span className="badge badge-warning"><AlertTriangle size={10} /> Action needed</span>
            </div>
            {loading ? (
              <>
                <Sk h={20} /><br />
                <Sk h={20} /><br />
                <Sk h={20} />
              </>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                {[
                  { label: 'Consultation Claims', val: stats?.claims?.pending_consultation, color: COLORS.yellow },
                  { label: 'Pharmacy Claims',      val: stats?.claims?.pending_pharmacy,     color: COLORS.blue },
                  { label: 'Inpatient Claims',     val: stats?.claims?.pending_inpatient,    color: COLORS.teal },
                  { label: 'SHA Claims',           val: stats?.claims?.pending_sha,          color: COLORS.green },
                ].map(({ label, val, color }) => (
                  <div key={label} style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    padding: '9px 12px',
                    background: 'var(--bg-raised)',
                    borderRadius: 8,
                    border: '1px solid var(--border)',
                  }}>
                    <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>{label}</span>
                    <span style={{
                      fontSize: 13.5, fontWeight: 700, color,
                      background: `${color}14`,
                      padding: '2px 10px',
                      borderRadius: 99,
                      border: `1px solid ${color}30`,
                    }}>{val ?? 0} pending</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}