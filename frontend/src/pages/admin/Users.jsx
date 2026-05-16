import { useState, useEffect, useCallback } from 'react'
import {
  UserPlus, Search, RefreshCw, ChevronLeft, ChevronRight,
  CheckCircle2, XCircle, MoreVertical, Shield, User
} from 'lucide-react'
import Navbar from '../../components/Navbar'
import { usersApi } from '../../utils/api'

const USER_TYPES = [
  'ADMIN','DOCTOR','RECEPTIONIST','NURSE','PROCUREMENT',
  'LAB_TECH','CASHIER','PHARMACIST','ACCOUNTANT','INSURANCE','HR',
]
const TYPE_COLOR = {
  ADMIN:'accent', DOCTOR:'info', NURSE:'success',
  RECEPTIONIST:'muted', LAB_TECH:'warning', PHARMACIST:'success',
  CASHIER:'muted', PROCUREMENT:'info', ACCOUNTANT:'muted',
  INSURANCE:'warning', HR:'muted',
}

function UserRow({ user, onToggle }) {
  return (
    <tr>
      <td>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{
            width: 32, height: 32, borderRadius: 8,
            background: 'var(--accent-soft)',
            border: '1px solid var(--border-accent)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 11, fontWeight: 700, color: 'var(--accent)',
            flexShrink: 0,
          }}>
            {user.first_name?.[0]}{user.last_name?.[0]}
          </div>
          <div>
            <strong>{user.first_name} {user.last_name}</strong>
            <div style={{ fontSize: 11.5, color: 'var(--text-muted)' }}>@{user.username}</div>
          </div>
        </div>
      </td>
      <td>{user.email || '—'}</td>
      <td>
        <span className={`badge badge-${TYPE_COLOR[user.user_type] || 'muted'}`}>
          {user.user_type}
        </span>
      </td>
      <td>{user.phone_number || '—'}</td>
      <td>
        <span className={`badge ${user.is_active ? 'badge-success' : 'badge-danger'}`}>
          {user.is_active
            ? <><CheckCircle2 size={10} /> Active</>
            : <><XCircle size={10} /> Inactive</>
          }
        </span>
      </td>
      <td style={{ fontSize: 12, color: 'var(--text-muted)' }}>
        {new Date(user.date_joined).toLocaleDateString('en-KE')}
      </td>
      <td>
        <button
          className={`btn btn-sm ${user.is_active ? 'btn-danger' : 'btn-ghost'}`}
          onClick={() => onToggle(user)}
        >
          {user.is_active ? 'Deactivate' : 'Activate'}
        </button>
      </td>
    </tr>
  )
}

export default function Users() {
  const [users, setUsers]       = useState([])
  const [loading, setLoading]   = useState(true)
  const [search, setSearch]     = useState('')
  const [typeFilter, setType]   = useState('')
  const [statusFilter, setStatus] = useState('')
  const [page, setPage]         = useState(1)
  const [count, setCount]       = useState(0)
  const [showModal, setModal]   = useState(false)
  const [newUser, setNewUser]   = useState({ username:'', first_name:'', last_name:'', email:'', user_type:'DOCTOR', password:'', password2:'' })
  const [creating, setCreating] = useState(false)
  const [createErr, setCreateErr] = useState('')
  const PAGE_SIZE = 20

  const load = useCallback(() => {
    setLoading(true)
    const params = { page, page_size: PAGE_SIZE }
    if (search)       params.search   = search
    if (typeFilter)   params.user_type = typeFilter
    if (statusFilter) params.is_active = statusFilter === 'active'
    usersApi.list(params)
      .then(({ data }) => { setUsers(data.results ?? data); setCount(data.count ?? (data.results ?? data).length) })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [page, search, typeFilter, statusFilter])

  useEffect(() => { load() }, [load])

  const handleToggle = async (user) => {
    await (user.is_active ? usersApi.deactivate(user.id) : usersApi.activate(user.id))
    load()
  }

  const handleCreate = async () => {
    setCreateErr('')
    if (newUser.password !== newUser.password2) { setCreateErr('Passwords do not match.'); return }
    setCreating(true)
    try {
      await usersApi.create(newUser)
      setModal(false)
      setNewUser({ username:'', first_name:'', last_name:'', email:'', user_type:'DOCTOR', password:'', password2:'' })
      load()
    } catch (e) {
      setCreateErr(JSON.stringify(e.response?.data || 'Error creating user'))
    } finally { setCreating(false) }
  }

  const totalPages = Math.ceil(count / PAGE_SIZE)

  return (
    <>
      <Navbar title="Admin / Users" />
      <div className="page-body">
        {/* Header */}
        <div className="page-header anim-fade-up">
          <div>
            <h1 className="page-title">User Management</h1>
            <p className="page-subtitle">{count} registered users · {USER_TYPES.length} role types</p>
          </div>
          <div style={{ display: 'flex', gap: 10 }}>
            <button className="btn btn-ghost" onClick={load}><RefreshCw size={14} /></button>
            <button className="btn btn-primary" onClick={() => setModal(true)}>
              <UserPlus size={15} /> New User
            </button>
          </div>
        </div>

        {/* Filters */}
        <div className="card anim-fade-up-1" style={{ padding: '16px 20px', marginBottom: 20 }}>
          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
            <div style={{ position: 'relative', flex: 1, minWidth: 200 }}>
              <Search size={14} style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
              <input
                className="form-input"
                style={{ paddingLeft: 36 }}
                placeholder="Search name, username, email…"
                value={search}
                onChange={e => { setSearch(e.target.value); setPage(1) }}
              />
            </div>
            <select className="form-select" style={{ width: 160 }} value={typeFilter} onChange={e => { setType(e.target.value); setPage(1) }}>
              <option value="">All Types</option>
              {USER_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
            <select className="form-select" style={{ width: 130 }} value={statusFilter} onChange={e => { setStatus(e.target.value); setPage(1) }}>
              <option value="">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>

        {/* Table */}
        <div className="card anim-fade-up-2" style={{ padding: 0 }}>
          <div className="table-wrap" style={{ border: 'none', borderRadius: 'var(--radius-lg)' }}>
            <table>
              <thead>
                <tr>
                  <th>User</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Phone</th>
                  <th>Status</th>
                  <th>Joined</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  Array.from({ length: 8 }).map((_, i) => (
                    <tr key={i}>
                      {Array.from({ length: 7 }).map((_, j) => (
                        <td key={j}><div className="skeleton" style={{ height: 18, borderRadius: 4 }} /></td>
                      ))}
                    </tr>
                  ))
                ) : users.length === 0 ? (
                  <tr><td colSpan={7} style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>No users found.</td></tr>
                ) : (
                  users.map(u => <UserRow key={u.id} user={u} onToggle={handleToggle} />)
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '14px 20px', borderTop: '1px solid var(--border)' }}>
              <span style={{ fontSize: 12.5, color: 'var(--text-muted)' }}>
                Showing {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, count)} of {count}
              </span>
              <div style={{ display: 'flex', gap: 6 }}>
                <button className="btn btn-ghost btn-sm" disabled={page === 1} onClick={() => setPage(p => p - 1)}><ChevronLeft size={14} /></button>
                <span style={{ padding: '4px 12px', fontSize: 13, color: 'var(--text-secondary)' }}>{page} / {totalPages}</span>
                <button className="btn btn-ghost btn-sm" disabled={page >= totalPages} onClick={() => setPage(p => p + 1)}><ChevronRight size={14} /></button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Create Modal */}
      {showModal && (
        <div style={{
          position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.65)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          zIndex: 200, padding: 20,
        }}>
          <div className="card" style={{ width: '100%', maxWidth: 500, maxHeight: '90vh', overflowY: 'auto' }}>
            <div className="flex-between" style={{ marginBottom: 24 }}>
              <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.4rem' }}>Create New User</h3>
              <button className="btn btn-ghost btn-sm" onClick={() => { setModal(false); setCreateErr('') }}>✕</button>
            </div>

            {createErr && <div className="alert alert-danger" style={{ marginBottom: 16 }}>{createErr}</div>}

            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">First Name</label>
                <input className="form-input" value={newUser.first_name} onChange={e => setNewUser({...newUser, first_name: e.target.value})} />
              </div>
              <div className="form-group">
                <label className="form-label">Last Name</label>
                <input className="form-input" value={newUser.last_name} onChange={e => setNewUser({...newUser, last_name: e.target.value})} />
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">Username</label>
              <input className="form-input" value={newUser.username} onChange={e => setNewUser({...newUser, username: e.target.value})} />
            </div>
            <div className="form-group">
              <label className="form-label">Email</label>
              <input className="form-input" type="email" value={newUser.email} onChange={e => setNewUser({...newUser, email: e.target.value})} />
            </div>
            <div className="form-group">
              <label className="form-label">Role</label>
              <select className="form-select" value={newUser.user_type} onChange={e => setNewUser({...newUser, user_type: e.target.value})}>
                {USER_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
            <div className="grid-2">
              <div className="form-group">
                <label className="form-label">Password</label>
                <input className="form-input" type="password" value={newUser.password} onChange={e => setNewUser({...newUser, password: e.target.value})} />
              </div>
              <div className="form-group">
                <label className="form-label">Confirm Password</label>
                <input className="form-input" type="password" value={newUser.password2} onChange={e => setNewUser({...newUser, password2: e.target.value})} />
              </div>
            </div>

            <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end', marginTop: 8 }}>
              <button className="btn btn-ghost" onClick={() => { setModal(false); setCreateErr('') }}>Cancel</button>
              <button className="btn btn-primary" disabled={creating} onClick={handleCreate}>
                {creating ? 'Creating…' : 'Create User'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}