"""
AfyaBoraHMIS — urls.py  (app-level)
All API routes registered through DRF DefaultRouter.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    # Auth & Users
    UserViewSet, LoginAttemptViewSet, AccountLockViewSet,
    TwoFactorCodeViewSet, UserSessionViewSet,

    # Core Clinical
    PatientViewSet, DoctorViewSet, NurseViewSet,

    # Facility & Lookup
    InsuranceProviderViewSet, SpecializedServiceViewSet,
    DiseaseViewSet, ClinicSettingsViewSet,

    # Visits, Triage & Queue
    TriageCategoryViewSet, PatientVisitViewSet,
    TriageAssessmentViewSet, QueueManagementViewSet,

    # Consultations & Diagnoses
    AppointmentViewSet, ConsultationViewSet, PatientMedicalHistoryViewSet,
    ICD10CategoryViewSet, ICD10CodeViewSet, ConsultationDiagnosisViewSet,

    # Pharmacy & Medicines
    MedicineCategoryViewSet, MedicineViewSet, StockMovementViewSet,
    PrescriptionViewSet, MedicineSaleViewSet,
    OverTheCounterSaleViewSet,

    # Laboratory & Imaging
    LabTestCategoryViewSet, LabTestViewSet, LabOrderViewSet,
    LabResultViewSet, ImagingStudyViewSet,

    # Inpatient
    WardViewSet, BedViewSet, InpatientAdmissionViewSet,
    InpatientDailyChargeViewSet, InpatientVitalsViewSet,

    # Emergency
    EmergencyBedViewSet, EmergencyVisitViewSet,
    EmergencyChargeViewSet, EmergencyPaymentViewSet,

    # Maternity & MCH
    MaternityVisitViewSet, MCHVisitViewSet,

    # Inpatient Medicine Requests
    InpatientMedicineRequestViewSet,

    # Procurement
    SupplierViewSet, PurchaseRequestViewSet, PurchaseOrderViewSet,
    GoodsReceivedNoteViewSet,

    # Insurance Claims
    ConsultationInsuranceClaimViewSet, PharmacyInsuranceClaimViewSet,
    InpatientInsuranceClaimViewSet,

    # SHA
    SHAMemberViewSet, SHAClaimViewSet,

    # Payment & Billing
    PaymentAuditLogViewSet, CashierSessionViewSet, MPesaDuplicateCheckViewSet,

    # eTIMS
    eTIMSConfigurationViewSet, eTIMSInvoiceViewSet,

    # HR
    HospitalWiFiNetworkViewSet, AttendanceQRCodeViewSet,
    AttendanceViewSet, LeaveTypeViewSet, LeaveApplicationViewSet,

    # Assets
    HospitalAssetViewSet, AssetMaintenanceLogViewSet,

    # Audit, Security & Notifications
    AuditLogViewSet, SecurityThreatViewSet,
    NotificationViewSet, ConversationViewSet, MessageViewSet,

    # Dashboard
    DashboardStatsView,
)

router = DefaultRouter()

# ── Auth & Users ──────────────────────────────────────────────
router.register(r'users', UserViewSet, basename='user')
router.register(r'login-attempts', LoginAttemptViewSet, basename='loginattempt')
router.register(r'account-locks', AccountLockViewSet, basename='accountlock')
router.register(r'two-factor-codes', TwoFactorCodeViewSet, basename='twofactorcode')
router.register(r'user-sessions', UserSessionViewSet, basename='usersession')

# ── Core Clinical ─────────────────────────────────────────────
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'nurses', NurseViewSet, basename='nurse')

# ── Facility & Lookup ─────────────────────────────────────────
router.register(r'insurance-providers', InsuranceProviderViewSet, basename='insuranceprovider')
router.register(r'specialized-services', SpecializedServiceViewSet, basename='specializedservice')
router.register(r'diseases', DiseaseViewSet, basename='disease')
router.register(r'clinic-settings', ClinicSettingsViewSet, basename='clinicsettings')

# ── Visits, Triage & Queue ────────────────────────────────────
router.register(r'triage-categories', TriageCategoryViewSet, basename='triagecategory')
router.register(r'patient-visits', PatientVisitViewSet, basename='patientvisit')
router.register(r'triage-assessments', TriageAssessmentViewSet, basename='triageassessment')
router.register(r'queue', QueueManagementViewSet, basename='queue')

# ── Consultations & Diagnoses ─────────────────────────────────
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'consultations', ConsultationViewSet, basename='consultation')
router.register(r'medical-history', PatientMedicalHistoryViewSet, basename='medicalhistory')
router.register(r'icd10-categories', ICD10CategoryViewSet, basename='icd10category')
router.register(r'icd10-codes', ICD10CodeViewSet, basename='icd10code')
router.register(r'consultation-diagnoses', ConsultationDiagnosisViewSet, basename='consultationdiagnosis')

# ── Pharmacy & Medicines ──────────────────────────────────────
router.register(r'medicine-categories', MedicineCategoryViewSet, basename='medicinecategory')
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'stock-movements', StockMovementViewSet, basename='stockmovement')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')
router.register(r'medicine-sales', MedicineSaleViewSet, basename='medicinesale')
router.register(r'otc-sales', OverTheCounterSaleViewSet, basename='otcsale')

# ── Laboratory & Imaging ──────────────────────────────────────
router.register(r'lab-test-categories', LabTestCategoryViewSet, basename='labtestcategory')
router.register(r'lab-tests', LabTestViewSet, basename='labtest')
router.register(r'lab-orders', LabOrderViewSet, basename='laborder')
router.register(r'lab-results', LabResultViewSet, basename='labresult')
router.register(r'imaging-studies', ImagingStudyViewSet, basename='imagingstudy')

# ── Inpatient ─────────────────────────────────────────────────
router.register(r'wards', WardViewSet, basename='ward')
router.register(r'beds', BedViewSet, basename='bed')
router.register(r'admissions', InpatientAdmissionViewSet, basename='admission')
router.register(r'inpatient-charges', InpatientDailyChargeViewSet, basename='inpatientcharge')
router.register(r'inpatient-vitals', InpatientVitalsViewSet, basename='inpatientvitals')

# ── Emergency ─────────────────────────────────────────────────
router.register(r'emergency-beds', EmergencyBedViewSet, basename='emergencybed')
router.register(r'emergency-visits', EmergencyVisitViewSet, basename='emergencyvisit')
router.register(r'emergency-charges', EmergencyChargeViewSet, basename='emergencycharge')
router.register(r'emergency-payments', EmergencyPaymentViewSet, basename='emergencypayment')

# ── Maternity & MCH ───────────────────────────────────────────
router.register(r'maternity-visits', MaternityVisitViewSet, basename='maternityvisit')
router.register(r'mch-visits', MCHVisitViewSet, basename='mchvisit')

# ── Inpatient Medicine Requests ───────────────────────────────
router.register(r'inpatient-medicine-requests', InpatientMedicineRequestViewSet, basename='inpatientmedicinerequest')

# ── Procurement ───────────────────────────────────────────────
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'purchase-requests', PurchaseRequestViewSet, basename='purchaserequest')
router.register(r'purchase-orders', PurchaseOrderViewSet, basename='purchaseorder')
router.register(r'goods-received-notes', GoodsReceivedNoteViewSet, basename='goodsreceivednote')

# ── Insurance Claims ──────────────────────────────────────────
router.register(r'claims/consultation', ConsultationInsuranceClaimViewSet, basename='consultationclaim')
router.register(r'claims/pharmacy', PharmacyInsuranceClaimViewSet, basename='pharmacyclaim')
router.register(r'claims/inpatient', InpatientInsuranceClaimViewSet, basename='inpatientclaim')

# ── SHA ───────────────────────────────────────────────────────
router.register(r'sha/members', SHAMemberViewSet, basename='shamember')
router.register(r'sha/claims', SHAClaimViewSet, basename='shaclaim')

# ── Payment & Billing ─────────────────────────────────────────
router.register(r'payment-audit-logs', PaymentAuditLogViewSet, basename='paymentauditlog')
router.register(r'cashier-sessions', CashierSessionViewSet, basename='cashiersession')
router.register(r'mpesa-duplicate-checks', MPesaDuplicateCheckViewSet, basename='mpesaduplicatecheck')

# ── eTIMS ─────────────────────────────────────────────────────
router.register(r'etims/config', eTIMSConfigurationViewSet, basename='etimsconfig')
router.register(r'etims/invoices', eTIMSInvoiceViewSet, basename='etimsinvoice')

# ── HR ────────────────────────────────────────────────────────
router.register(r'hr/wifi-networks', HospitalWiFiNetworkViewSet, basename='wifinetwork')
router.register(r'hr/attendance-qr-codes', AttendanceQRCodeViewSet, basename='attendanceqrcode')
router.register(r'hr/attendance', AttendanceViewSet, basename='attendance')
router.register(r'hr/leave-types', LeaveTypeViewSet, basename='leavetype')
router.register(r'hr/leave-applications', LeaveApplicationViewSet, basename='leaveapplication')

# ── Assets ────────────────────────────────────────────────────
router.register(r'assets', HospitalAssetViewSet, basename='hospitalasset')
router.register(r'asset-maintenance-logs', AssetMaintenanceLogViewSet, basename='assetmaintenancelog')

# ── Audit, Security & Notifications ──────────────────────────
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')
router.register(r'security-threats', SecurityThreatViewSet, basename='securitythreat')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')


urlpatterns = [
    # JWT Auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Dashboard
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),

    # All router-registered ViewSets
    path('', include(router.urls)),
]