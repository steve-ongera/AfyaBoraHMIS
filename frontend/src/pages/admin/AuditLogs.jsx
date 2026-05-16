import { useState, useEffect, useCallback } from 'react'
import { Search, RefreshCw, Shield, AlertTriangle, Eye, ChevronLeft, ChevronRight } from 'lucide-react'
import Navbar from '../../components/Navbar'
import { auditApi } from '../../utils/api'

const ACTION_COLOR = {
  create: 'success', update: 'info', delete: 'danger',
  view: 'muted', approve: 'success', reject: 'danger',
  login: 'accent', logout: 'muted', export: 'warning', print: 'muted',
}

export default function AuditLogs() {
  const [logs, setLogs]       = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch]   = useState('')
  const [action, setAction]   = useState('')
  const [page, setPage]       = useState(1)
  const [count, setCount]     = useState(0)
  const [selected, setSelected] = useState(null)
  const PAGE_SIZE = 25

  const load = useCallback(() => {
    setLoading(true)
    const params = { page, page_size: PAGE_SIZE }
    if (search) params.search = search
    if (action) params.action = action
    auditApi.logs(params)
      .then(({ data }) => { setLogs(data.results ?? data); setCount(data.count ?? (data.results ?? data).length) })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [page, search, action])

  useEffect(() => { load() }, [load])

  const totalPages = Math.ceil(count / PAGE_SIZE)
  const ACTIONS = ['create','update','delete','view','approve','reject','login','logout','export','print']

  return (
    <>
      <Navbar title="Admin / Audit Logs" />
      <div className="page-body">
        <div className="page-header anim-fade-up">
          <div>
            <h1 className="page-title">Audit Logs</h1>
            <p className="page-subtitle">Complete tamper-evident record of all system actions</p>
          </div>
          <button className="btn btn-ghost" onClick={load}><RefreshCw size={14} /></button>
        </div>

        {/* Filters */}
        <div className="card anim-fade-up-1" style={{ padding: '14px 18px', marginBottom: 20 }}>
          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
            <div style={{ position: 'relative', flex: 1, minWidth: 220 }}>
              <Search size={14} style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
              <input className="form-input" style={{ paddingLeft: 36 }} placeholder="Search description, record ID…"
                value={search} onChange={e => { setSearch(e.target.value); setPage(1) }} />
            </div>
            <select className="form-select" style={{ width: 140 }} value={action} onChange={e => { setAction(e.target.value); setPage(1) }}>
              <option value="">All Actions</option>
              {ACTIONS.map(a => <option key={a} value={a}>{a}</option>)}
            </select>
          </div>
        </div>

        {/* Table */}
        <div className="card anim-fade-up-2" style={{ padding: 0 }}>
          <div className="table-wrap" style={{ border: 'none' }}>
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>User</th>
                  <th>Action</th>
                  <th>Table</th>
                  <th>Record</th>
                  <th>IP Address</th>
                  <th>Description</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  Array.from({ length: 10 }).map((_, i) => (
                    <tr key={i}>
                      {Array.from({ length: 8 }).map((_, j) => (
                        <td key={j}><div className="skeleton" style={{ height: 16, borderRadius: 4 }} /></td>
                      ))}
                    </tr>
                  ))
                ) : logs.length === 0 ? (
                  <tr><td colSpan={8} style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>No log entries found.</td></tr>
                ) : (
                  logs.map((log) => (
                    <tr key={log.id}>
                      <td style={{ fontSize: 12, color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
                        {new Date(log.timestamp).toLocaleString('en-KE')}
                      </td>
                      <td><strong>{log.user_name || 'System'}</strong></td>
                      <td>
                        <span className={`badge badge-${ACTION_COLOR[log.action] || 'muted'}`}>
                          {log.action}
                        </span>
                      </td>
                      <td style={{ fontSize: 12.5 }}>{log.table_affected}</td>
                      <td style={{ fontSize: 12, color: 'var(--text-muted)' }}>{log.record_id || '—'}</td>
                      <td style={{ fontSize: 12, fontFamily: 'monospace', color: 'var(--text-muted)' }}>{log.ip_address}</td>
                      <td style={{ maxWidth: 260, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontSize: 13 }}>
                        {log.description}
                      </td>
                      <td>
                        <button className="btn btn-ghost btn-sm" onClick={() => setSelected(log)}>
                          <Eye size={13} />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {totalPages > 1 && (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '14px 20px', borderTop: '1px solid var(--border)' }}>
              <span style={{ fontSize: 12.5, color: 'var(--text-muted)' }}>
                {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, count)} of {count} entries
              </span>
              <div style={{ display: 'flex', gap: 6 }}>
                <button className="btn btn-ghost btn-sm" disabled={page === 1} onClick={() => setPage(p => p - 1)}><ChevronLeft size={14} /></button>
                <span style={{ padding: '4px 12px', fontSize: 13 }}>{page} / {totalPages}</span>
                <button className="btn btn-ghost btn-sm" disabled={page >= totalPages} onClick={() => setPage(p => p + 1)}><ChevronRight size={14} /></button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Detail Modal */}
      {selected && (
        <div style={{
          position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.65)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          zIndex: 200, padding: 20,
        }}>
          <div className="card" style={{ width: '100%', maxWidth: 560, maxHeight: '85vh', overflowY: 'auto' }}>
            <div className="flex-between" style={{ marginBottom: 20 }}>
              <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.3rem' }}>Log Detail</h3>
              <button className="btn btn-ghost btn-sm" onClick={() => setSelected(null)}>✕</button>
            </div>

            {[
              ['Action',    <span className={`badge badge-${ACTION_COLOR[selected.action] || 'muted'}`}>{selected.action}</span>],
              ['User',      selected.user_name || 'System'],
              ['Table',     selected.table_affected],
              ['Record ID', selected.record_id || '—'],
              ['IP Address', selected.ip_address],
              ['Timestamp', new Date(selected.timestamp).toLocaleString('en-KE')],
              ['Description', selected.description],
            ].map(([label, val]) => (
              <div key={label} style={{ marginBottom: 14 }}>
                <div style={{ fontSize: 11, textTransform: 'uppercase', letterSpacing: '.07em', color: 'var(--text-muted)', marginBottom: 4 }}>{label}</div>
                <div style={{ fontSize: 13.5, color: 'var(--text-primary)' }}>{val}</div>
              </div>
            ))}

            {selected.old_values && (
              <div style={{ marginBottom: 14 }}>
                <div style={{ fontSize: 11, textTransform: 'uppercase', letterSpacing: '.07em', color: 'var(--text-muted)', marginBottom: 6 }}>Previous Values</div>
                <pre style={{ background: 'var(--bg-raised)', border: '1px solid var(--border)', borderRadius: 8, padding: 12, fontSize: 12, color: 'var(--text-secondary)', overflow: 'auto' }}>
                  {JSON.stringify(selected.old_values, null, 2)}
                </pre>
              </div>
            )}
            {selected.new_values && (
              <div>
                <div style={{ fontSize: 11, textTransform: 'uppercase', letterSpacing: '.07em', color: 'var(--text-muted)', marginBottom: 6 }}>New Values</div>
                <pre style={{ background: 'var(--bg-raised)', border: '1px solid var(--border)', borderRadius: 8, padding: 12, fontSize: 12, color: 'var(--text-secondary)', overflow: 'auto' }}>
                  {JSON.stringify(selected.new_values, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  )
}