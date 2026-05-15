# AfyaBoraHMIS — Level 5 Hospital Management Information System

> **"Afya Bora"** — Swahili for *"Better Health"*

A comprehensive, cloud-ready HMIS built for **Level 5 hospitals** and **multi-branch pharmacy chains** in Kenya.  
Designed to comply with Ministry of Health standards, NHIF/SHA integration, KRA eTIMS, and the Kenya Health Policy 2014–2030.

---

## 🏥 System Overview

AfyaBoraHMIS is a full-stack electronic health record and hospital operations platform that covers the complete patient journey — from **reception triage** through **consultation**, **pharmacy**, **laboratory**, **inpatient care**, and **billing** — while maintaining a longitudinal patient record accessible across all connected facilities (hospitals and chemists).

---

## 🌐 Multi-Facility Architecture

```
AfyaBoraHMIS Cloud
      │
      ├── Level 5 Hospital (Main)
      │     ├── OPD / Triage / Emergency
      │     ├── Inpatient / Wards / ICU
      │     ├── Laboratory & Radiology
      │     ├── Pharmacy
      │     └── Billing / Insurance
      │
      ├── Branch Pharmacy 1 (Nairobi CBD)
      ├── Branch Pharmacy 2 (Westlands)
      └── Branch Pharmacy N (...)
```

Patients are identified by a **national ID or phone number**. Their records (prescriptions, diagnoses, allergies, chronic conditions) are accessible at any connected facility.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.x + Django REST Framework |
| Database | PostgreSQL 15+ |
| Cache / Queues | Redis + Celery |
| Auth | JWT (SimpleJWT) + 2FA |
| File Storage | AWS S3 / MinIO |
| Frontend | React 18 + Vite |
| HTTP Client | Axios |
| UI | Tailwind CSS + Ant Design |
| Real-time | Django Channels (WebSocket) |
| Deployment | Docker + Nginx + Gunicorn |

---

## 📦 Modules

| Module | Description |
|--------|-------------|
| **Authentication** | Login, 2FA, account lock, session tracking |
| **Patient Registry** | Unified patient records across all facilities |
| **Reception & Queue** | Walk-in registration, triage queue, appointment booking |
| **Triage** | ESI colour-coded triage, vital signs, nurse assessment |
| **OPD Consultation** | Doctor consultations, ICD-10 diagnoses, prescriptions |
| **Emergency / Casualty** | Trauma, RTA, emergency beds, police cases, emergency billing |
| **Maternity** | Labor & delivery, antenatal, MCH baby clinic |
| **Inpatient** | Wards, beds, daily charges, medication administration |
| **Pharmacy** | Dispensing, OTC sales, stock management, insurance claims |
| **Laboratory** | Lab orders, results, imaging/radiology, equipment |
| **Procurement** | Purchase requests, POs, GRN, supplier management |
| **Insurance / Claims** | SHA, Jubilee, AAR, Britam — multi-workflow claims |
| **SHA Integration** | SHA member verification, claim submission |
| **KRA eTIMS** | Electronic tax invoicing for all transactions |
| **HR & Attendance** | QR code attendance, leave management, payroll-ready |
| **Assets** | Hospital asset tracking, maintenance logs |
| **Audit & Security** | Full audit trail, threat detection, session monitoring |
| **Notifications** | Real-time in-app notifications via WebSocket |

---

## 🗂️ Project Structure

```
AfyaBoraHMIS/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── afyabora/               # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── core/                   # Main application
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── admin.py
│       ├── permissions.py
│       └── migrations/
│
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── utils/
│       │   └── api.js
│       ├── components/
│       │   ├── Navbar.jsx
│       │   └── Sidebar.jsx
│       ├── styles/
│       │   └── main.css
│       └── pages/
│           ├── admin/
│           │   ├── Dashboard.jsx
│           │   ├── Users.jsx
│           │   ├── Settings.jsx
│           │   └── AuditLogs.jsx
│           ├── Login.jsx
│           └── UnderDevelopment.jsx
│
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Quick Start

### 1. Clone & Configure

```bash
git clone https://github.com/yourorg/AfyaBoraHMIS.git
cd AfyaBoraHMIS
cp backend/.env.example backend/.env
# Edit .env with your database credentials, secret key, etc.
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 4. Docker (Recommended for Production)

```bash
docker-compose up --build
```

---

## 🔑 Environment Variables (`.env.example`)

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=afyabora
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (for 2FA)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=yourpassword

# AWS S3 (optional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

# KRA eTIMS
ETIMS_API_URL=https://etims-api.kra.go.ke
ETIMS_TIN=

# JWT
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

---

## 👥 User Roles & Permissions

| Role | Access |
|------|--------|
| `ADMIN` | Full system access, user management, settings |
| `DOCTOR` | Consultations, prescriptions, lab orders, imaging |
| `NURSE` | Triage, vitals, medication administration, inpatient care |
| `RECEPTIONIST` | Patient registration, appointments, queue management |
| `PHARMACIST` | Dispensing, stock management, OTC sales |
| `LAB_TECH` | Lab orders, results entry, equipment management |
| `CASHIER` | Payments, receipts, cashier sessions, eTIMS invoices |
| `INSURANCE` | Claims approval, insurance verification |
| `PROCUREMENT` | Purchase requests, POs, GRN, suppliers |
| `ACCOUNTANT` | Financial reports, budget approvals |
| `HR` | Staff management, attendance, leave |

---

## 🔗 API Overview

Base URL: `http://localhost:8000/api/`

| Endpoint Group | Path |
|----------------|------|
| Authentication | `/api/auth/` |
| Patients | `/api/patients/` |
| Visits | `/api/visits/` |
| Consultations | `/api/consultations/` |
| Prescriptions | `/api/prescriptions/` |
| Medicines | `/api/medicines/` |
| Lab Orders | `/api/lab/` |
| Inpatient | `/api/inpatient/` |
| Emergency | `/api/emergency/` |
| Insurance Claims | `/api/claims/` |
| SHA | `/api/sha/` |
| eTIMS | `/api/etims/` |
| HR / Attendance | `/api/hr/` |
| Procurement | `/api/procurement/` |
| Assets | `/api/assets/` |
| Admin | `/api/admin/` |
| Notifications | `/api/notifications/` |

Full API docs available at `/api/docs/` (Swagger) and `/api/redoc/`.

---

## 🏗️ Kenya-Specific Compliance

- ✅ **MoH DHIS2** — Notifiable disease reporting, disease statistics
- ✅ **SHA/NHIF** — Member verification, claim submission, package mapping
- ✅ **KRA eTIMS** — Electronic tax invoicing, credit notes, VAT handling
- ✅ **ICD-10** — Full ICD-10 code database with Kenyan common conditions
- ✅ **Kenya Public Health Act** — Notifiable disease tracking
- ✅ **Data Protection Act 2019** — Patient data anonymization for tax submissions

---

## 🔒 Security Features

- JWT authentication with refresh token rotation
- Two-factor authentication (email OTP)
- Account lockout after failed attempts
- Full audit trail for all actions
- SQL injection / XSS / path traversal detection
- Cashier session management with cash variance tracking
- M-Pesa duplicate payment prevention

---

## 📊 Reporting

- Daily/weekly/monthly revenue reports
- Attendance and leave reports
- Disease statistics for MoH reporting
- Insurance claims reconciliation
- eTIMS daily summaries
- Lab turnaround time reports
- Stock movement and expiry reports

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add your feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 📞 Support

- 📧 support@afyaborahmis.co.ke
- 🌐 https://afyaborahmis.co.ke
- 📱 WhatsApp: +254 700 000 000

---

*Built with ❤️ for Kenya's healthcare system*