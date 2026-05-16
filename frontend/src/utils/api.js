import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

// ── Attach access token on every request ──────────────────────
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// ── Auto-refresh on 401 ───────────────────────────────────────
let isRefreshing = false
let queue = []

const processQueue = (error, token = null) => {
  queue.forEach((p) => (error ? p.reject(error) : p.resolve(token)))
  queue = []
}

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config
    if (err.response?.status === 401 && !original._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          queue.push({ resolve, reject })
        }).then((token) => {
          original.headers.Authorization = `Bearer ${token}`
          return api(original)
        })
      }
      original._retry = true
      isRefreshing = true
      const refresh = localStorage.getItem('refresh_token')
      if (!refresh) {
        logout()
        return Promise.reject(err)
      }
      try {
        const { data } = await axios.post(`${BASE_URL}/auth/token/refresh/`, { refresh })
        localStorage.setItem('access_token', data.access)
        api.defaults.headers.common.Authorization = `Bearer ${data.access}`
        processQueue(null, data.access)
        return api(original)
      } catch (refreshErr) {
        processQueue(refreshErr, null)
        logout()
        return Promise.reject(refreshErr)
      } finally {
        isRefreshing = false
      }
    }
    return Promise.reject(err)
  }
)

export const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  window.location.href = '/login'
}

// ── Auth ─────────────────────────────────────────────────────
export const authApi = {
  login: (credentials) => api.post('/auth/token/', credentials),
  refresh: (refresh) => api.post('/auth/token/refresh/', { refresh }),
  me: () => api.get('/users/me/'),
}

// ── Dashboard ─────────────────────────────────────────────────
export const dashboardApi = {
  stats: () => api.get('/dashboard/stats/'),
}

// ── Users ─────────────────────────────────────────────────────
export const usersApi = {
  list: (params) => api.get('/users/', { params }),
  get: (id) => api.get(`/users/${id}/`),
  create: (data) => api.post('/users/', data),
  update: (id, data) => api.patch(`/users/${id}/`, data),
  deactivate: (id) => api.post(`/users/${id}/deactivate/`),
  activate: (id) => api.post(`/users/${id}/activate/`),
  byType: (type) => api.get(`/users/by-type/${type}/`),
}

// ── Patients ──────────────────────────────────────────────────
export const patientsApi = {
  list: (params) => api.get('/patients/', { params }),
  get: (id) => api.get(`/patients/${id}/`),
  create: (data) => api.post('/patients/', data),
  update: (id, data) => api.patch(`/patients/${id}/`, data),
  history: (id) => api.get(`/patients/${id}/history/`),
  visits: (id) => api.get(`/patients/${id}/visits/`),
}

// ── Visits ────────────────────────────────────────────────────
export const visitsApi = {
  list: (params) => api.get('/patient-visits/', { params }),
  get: (id) => api.get(`/patient-visits/${id}/`),
  create: (data) => api.post('/patient-visits/', data),
  today: () => api.get('/patient-visits/today/'),
  active: () => api.get('/patient-visits/active/'),
  updateStatus: (id, status) => api.patch(`/patient-visits/${id}/update-status/`, { status }),
}

// ── Appointments ──────────────────────────────────────────────
export const appointmentsApi = {
  list: (params) => api.get('/appointments/', { params }),
  get: (id) => api.get(`/appointments/${id}/`),
  create: (data) => api.post('/appointments/', data),
  update: (id, data) => api.patch(`/appointments/${id}/`, data),
  today: () => api.get('/appointments/today/'),
  upcoming: () => api.get('/appointments/upcoming/'),
}

// ── Medicines ─────────────────────────────────────────────────
export const medicinesApi = {
  list: (params) => api.get('/medicines/', { params }),
  get: (id) => api.get(`/medicines/${id}/`),
  lowStock: () => api.get('/medicines/low-stock/'),
  expiring: () => api.get('/medicines/expiring/'),
  adjustStock: (id, data) => api.post(`/medicines/${id}/adjust-stock/`, data),
}

// ── Lab Orders ────────────────────────────────────────────────
export const labApi = {
  orders: (params) => api.get('/lab-orders/', { params }),
  getOrder: (id) => api.get(`/lab-orders/${id}/`),
  createOrder: (data) => api.post('/lab-orders/', data),
  pending: () => api.get('/lab-orders/pending/'),
  updateStatus: (id, status) => api.patch(`/lab-orders/${id}/update-status/`, { status }),
  results: (params) => api.get('/lab-results/', { params }),
  critical: () => api.get('/lab-results/critical/'),
}

// ── Inpatient ─────────────────────────────────────────────────
export const inpatientApi = {
  admissions: (params) => api.get('/admissions/', { params }),
  getAdmission: (id) => api.get(`/admissions/${id}/`),
  active: () => api.get('/admissions/active/'),
  discharge: (id, data) => api.post(`/admissions/${id}/discharge/`, data),
  charges: (id) => api.get(`/admissions/${id}/charges/`),
  vitals: (id) => api.get(`/admissions/${id}/vitals/`),
  wards: (params) => api.get('/wards/', { params }),
  beds: (params) => api.get('/beds/', { params }),
  availableBeds: () => api.get('/beds/available/'),
  occupancy: () => api.get('/wards/occupancy/'),
}

// ── Emergency ─────────────────────────────────────────────────
export const emergencyApi = {
  list: (params) => api.get('/emergency-visits/', { params }),
  active: () => api.get('/emergency-visits/active/'),
  critical: () => api.get('/emergency-visits/critical/'),
  beds: () => api.get('/emergency-beds/available/'),
}

// ── Insurance & Claims ────────────────────────────────────────
export const claimsApi = {
  consultation: (params) => api.get('/claims/consultation/', { params }),
  pharmacy: (params) => api.get('/claims/pharmacy/', { params }),
  inpatient: (params) => api.get('/claims/inpatient/', { params }),
  sha: (params) => api.get('/sha/claims/', { params }),
  approveClaim: (type, id, data) => api.post(`/claims/${type}/${id}/approve/`, data),
}

// ── Procurement ───────────────────────────────────────────────
export const procurementApi = {
  suppliers: (params) => api.get('/suppliers/', { params }),
  purchaseRequests: (params) => api.get('/purchase-requests/', { params }),
  purchaseOrders: (params) => api.get('/purchase-orders/', { params }),
  grns: (params) => api.get('/goods-received-notes/', { params }),
}

// ── HR ────────────────────────────────────────────────────────
export const hrApi = {
  attendance: (params) => api.get('/hr/attendance/', { params }),
  myAttendance: () => api.get('/hr/attendance/my-attendance/'),
  todayAttendance: () => api.get('/hr/attendance/today/'),
  leaveApplications: (params) => api.get('/hr/leave-applications/', { params }),
  myLeaves: () => api.get('/hr/leave-applications/my-applications/'),
  applyLeave: (data) => api.post('/hr/leave-applications/', data),
}

// ── Audit ─────────────────────────────────────────────────────
export const auditApi = {
  logs: (params) => api.get('/audit-logs/', { params }),
  threats: (params) => api.get('/security-threats/', { params }),
}

// ── Notifications ─────────────────────────────────────────────
export const notificationsApi = {
  list: () => api.get('/notifications/'),
  unread: () => api.get('/notifications/unread/'),
  markRead: (id) => api.post(`/notifications/${id}/mark-read/`),
  markAllRead: () => api.post('/notifications/mark-all-read/'),
}

// ── Settings ──────────────────────────────────────────────────
export const settingsApi = {
  clinic: () => api.get('/clinic-settings/'),
  updateClinic: (id, data) => api.patch(`/clinic-settings/${id}/`, data),
  etims: () => api.get('/etims/config/'),
}

export default api