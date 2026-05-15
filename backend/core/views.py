"""
AfyaBoraHMIS — views.py
Django REST Framework ViewSets for all models.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.shortcuts import get_object_or_404

from .models import (
    User, LoginAttempt, AccountLock, TwoFactorCode, UserSession,
    Patient, Doctor, Nurse,
    InsuranceProvider, SpecializedService, Disease, ClinicSettings,
    TriageCategory, PatientVisit, TriageAssessment, QueueManagement,
    Appointment, Consultation, PatientMedicalHistory,
    ICD10Category, ICD10Code, ConsultationDiagnosis,
    MedicineCategory, Medicine, StockMovement, Prescription,
    MedicineSale, SoldMedicine, OverTheCounterSale, OverTheCounterSaleItem,
    LabTestCategory, LabTest, LabOrder, LabOrderItem, LabResult, ImagingStudy,
    Ward, Bed, InpatientAdmission, InpatientDailyCharge, InpatientVitals,
    EmergencyBed, EmergencyVisit, EmergencyCharge, EmergencyPayment,
    MaternityVisit, MCHVisit,
    InpatientMedicineRequest,
    Supplier, PurchaseRequest, PurchaseRequestItem,
    PurchaseOrder, PurchaseOrderItem,
    GoodsReceivedNote, GoodsReceivedNoteItem,
    ConsultationInsuranceClaim, PharmacyInsuranceClaim, InpatientInsuranceClaim,
    SHAMember, SHAClaim,
    PaymentAuditLog, CashierSession, MPesaDuplicateCheck,
    eTIMSConfiguration, eTIMSInvoice, eTIMSInvoiceItem,
    HospitalWiFiNetwork, AttendanceQRCode, Attendance, LeaveType, LeaveApplication,
    HospitalAsset, AssetMaintenanceLog,
    AuditLog, SecurityThreat, Notification, Conversation, Message,
)
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    LoginAttemptSerializer, AccountLockSerializer,
    TwoFactorCodeSerializer, UserSessionSerializer,
    PatientSerializer, PatientListSerializer,
    DoctorSerializer, DoctorListSerializer,
    NurseSerializer, NurseListSerializer,
    InsuranceProviderSerializer, SpecializedServiceSerializer,
    DiseaseSerializer, ClinicSettingsSerializer,
    TriageCategorySerializer, PatientVisitSerializer, PatientVisitListSerializer,
    TriageAssessmentSerializer, QueueManagementSerializer,
    AppointmentSerializer, AppointmentListSerializer,
    ConsultationSerializer, PatientMedicalHistorySerializer,
    ICD10CategorySerializer, ICD10CodeSerializer, ICD10CodeListSerializer,
    ConsultationDiagnosisSerializer,
    MedicineCategorySerializer, MedicineSerializer, MedicineListSerializer,
    StockMovementSerializer, PrescriptionSerializer,
    MedicineSaleSerializer, SoldMedicineSerializer,
    OverTheCounterSaleSerializer, OverTheCounterSaleItemSerializer,
    LabTestCategorySerializer, LabTestSerializer, LabTestListSerializer,
    LabOrderSerializer, LabOrderListSerializer, LabOrderItemSerializer,
    LabResultSerializer, ImagingStudySerializer,
    WardSerializer, BedSerializer, BedListSerializer,
    InpatientAdmissionSerializer, InpatientAdmissionListSerializer,
    InpatientDailyChargeSerializer, InpatientVitalsSerializer,
    EmergencyBedSerializer, EmergencyVisitSerializer, EmergencyVisitListSerializer,
    EmergencyChargeSerializer, EmergencyPaymentSerializer,
    MaternityVisitSerializer, MCHVisitSerializer,
    InpatientMedicineRequestSerializer,
    SupplierSerializer, SupplierListSerializer,
    PurchaseRequestSerializer, PurchaseRequestListSerializer,
    PurchaseRequestItemSerializer,
    PurchaseOrderSerializer, PurchaseOrderListSerializer, PurchaseOrderItemSerializer,
    GoodsReceivedNoteSerializer, GoodsReceivedNoteItemSerializer,
    ConsultationInsuranceClaimSerializer, PharmacyInsuranceClaimSerializer,
    InpatientInsuranceClaimSerializer,
    SHAMemberSerializer, SHAClaimSerializer,
    PaymentAuditLogSerializer, CashierSessionSerializer, MPesaDuplicateCheckSerializer,
    eTIMSConfigurationSerializer, eTIMSInvoiceSerializer, eTIMSInvoiceListSerializer,
    eTIMSInvoiceItemSerializer,
    HospitalWiFiNetworkSerializer, AttendanceQRCodeSerializer,
    AttendanceSerializer, AttendanceListSerializer,
    LeaveTypeSerializer, LeaveApplicationSerializer, LeaveApplicationListSerializer,
    HospitalAssetSerializer, HospitalAssetListSerializer,
    AssetMaintenanceLogSerializer,
    AuditLogSerializer, SecurityThreatSerializer,
    NotificationSerializer, ConversationSerializer, ConversationListSerializer,
    MessageSerializer,
)


# ============================================================
# BASE MIXIN
# ============================================================

class ListDetailSerializerMixin:
    """Use a lightweight serializer for list actions, full one for detail."""
    list_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'list' and self.list_serializer_class:
            return self.list_serializer_class
        return super().get_serializer_class()


# ============================================================
# AUTH & USERS
# ============================================================

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_type', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    ordering_fields = ['date_joined', 'last_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Return the currently authenticated user's profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-type/(?P<user_type>[^/.]+)')
    def by_type(self, request, user_type=None):
        qs = self.get_queryset().filter(user_type=user_type.upper())
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response({'detail': 'User deactivated.'})

    @action(detail=True, methods=['post'], url_path='activate')
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save(update_fields=['is_active'])
        return Response({'detail': 'User activated.'})


class LoginAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LoginAttempt.objects.all()
    serializer_class = LoginAttemptSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['username', 'success', 'ip_address']
    ordering_fields = ['timestamp']


class AccountLockViewSet(viewsets.ModelViewSet):
    queryset = AccountLock.objects.select_related('user').all()
    serializer_class = AccountLockSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_locked', 'user']

    @action(detail=True, methods=['post'], url_path='unlock')
    def unlock(self, request, pk=None):
        lock = self.get_object()
        lock.is_locked = False
        lock.failed_attempts = 0
        lock.save()
        return Response({'detail': 'Account unlocked.'})


class TwoFactorCodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TwoFactorCode.objects.all()
    serializer_class = TwoFactorCodeSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'used']


class UserSessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserSession.objects.select_related('user').all()
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'is_active']
    ordering_fields = ['last_activity', 'login_time']

    @action(detail=False, methods=['get'], url_path='my-sessions')
    def my_sessions(self, request):
        qs = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


# ============================================================
# CORE CLINICAL
# ============================================================

class PatientViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    list_serializer_class = PatientListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'blood_type']
    search_fields = ['first_name', 'last_name', 'phone_number', 'id_number', 'email']
    ordering_fields = ['created_at', 'last_name']

    @action(detail=True, methods=['get'], url_path='history')
    def medical_history(self, request, pk=None):
        patient = self.get_object()
        history = PatientMedicalHistory.objects.filter(patient=patient).order_by('-date_recorded')
        serializer = PatientMedicalHistorySerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='visits')
    def visits(self, request, pk=None):
        patient = self.get_object()
        qs = PatientVisit.objects.filter(patient=patient)
        serializer = PatientVisitListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='admissions')
    def admissions(self, request, pk=None):
        patient = self.get_object()
        qs = InpatientAdmission.objects.filter(patient=patient)
        serializer = InpatientAdmissionListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='lab-orders')
    def lab_orders(self, request, pk=None):
        patient = self.get_object()
        qs = LabOrder.objects.filter(patient=patient)
        serializer = LabOrderListSerializer(qs, many=True)
        return Response(serializer.data)


class DoctorViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    list_serializer_class = DoctorListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialization', 'is_active', 'department']
    search_fields = ['first_name', 'last_name', 'license_number', 'id_number']
    ordering_fields = ['created_at', 'last_name']

    @action(detail=True, methods=['get'], url_path='visits')
    def patient_visits(self, request, pk=None):
        doctor = self.get_object()
        qs = PatientVisit.objects.filter(assigned_doctor=doctor)
        serializer = PatientVisitListSerializer(qs, many=True)
        return Response(serializer.data)


class NurseViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer
    list_serializer_class = NurseListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nurse_type', 'department', 'is_active', 'is_charge_nurse']
    search_fields = ['first_name', 'last_name', 'nurse_id', 'license_number']
    ordering_fields = ['created_at', 'last_name']


# ============================================================
# FACILITY & LOOKUP
# ============================================================

class InsuranceProviderViewSet(viewsets.ModelViewSet):
    queryset = InsuranceProvider.objects.all()
    serializer_class = InsuranceProviderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class SpecializedServiceViewSet(viewsets.ModelViewSet):
    queryset = SpecializedService.objects.all()
    serializer_class = SpecializedServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class DiseaseViewSet(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'icd_code']


class ClinicSettingsViewSet(viewsets.ModelViewSet):
    queryset = ClinicSettings.objects.all()
    serializer_class = ClinicSettingsSerializer
    permission_classes = [IsAdminUser]


# ============================================================
# VISITS, TRIAGE & QUEUE
# ============================================================

class TriageCategoryViewSet(viewsets.ModelViewSet):
    queryset = TriageCategory.objects.all()
    serializer_class = TriageCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'priority_level']


class PatientVisitViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = PatientVisit.objects.select_related('patient', 'assigned_doctor', 'assigned_nurse').all()
    serializer_class = PatientVisitSerializer
    list_serializer_class = PatientVisitListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['visit_type', 'status', 'assigned_doctor', 'assigned_nurse', 'patient']
    search_fields = ['visit_number', 'patient__first_name', 'patient__last_name', 'chief_complaint']
    ordering_fields = ['arrival_time', 'created_at']

    @action(detail=False, methods=['get'], url_path='today')
    def today(self, request):
        qs = self.get_queryset().filter(created_at__date=timezone.now().date())
        serializer = PatientVisitListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='active')
    def active(self, request):
        active_statuses = ['REGISTERED', 'TRIAGED', 'WAITING', 'IN_CONSULTATION', 'IN_TREATMENT']
        qs = self.get_queryset().filter(status__in=active_statuses)
        serializer = PatientVisitListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        visit = self.get_object()
        new_status = request.data.get('status')
        if not new_status:
            return Response({'error': 'status field required.'}, status=status.HTTP_400_BAD_REQUEST)
        visit.status = new_status
        visit.save(update_fields=['status'])
        return Response(PatientVisitSerializer(visit).data)


class TriageAssessmentViewSet(viewsets.ModelViewSet):
    queryset = TriageAssessment.objects.select_related('visit', 'category', 'assessed_by').all()
    serializer_class = TriageAssessmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['visit', 'category', 'requires_immediate_attention']
    ordering_fields = ['assessment_time']

    @action(detail=False, methods=['get'], url_path='immediate')
    def immediate_attention(self, request):
        qs = self.get_queryset().filter(requires_immediate_attention=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class QueueManagementViewSet(viewsets.ModelViewSet):
    queryset = QueueManagement.objects.select_related('visit').all()
    serializer_class = QueueManagementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['department', 'is_active', 'is_serving', 'is_completed']
    ordering_fields = ['queue_number', 'joined_queue']

    @action(detail=False, methods=['get'], url_path='department/(?P<dept>[^/.]+)')
    def by_department(self, request, dept=None):
        qs = self.get_queryset().filter(department=dept.upper(), is_active=True, is_completed=False)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='call')
    def call_patient(self, request, pk=None):
        q = self.get_object()
        q.called_time = timezone.now()
        q.is_serving = True
        q.service_start = timezone.now()
        q.save(update_fields=['called_time', 'is_serving', 'service_start'])
        return Response(self.get_serializer(q).data)

    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        q = self.get_object()
        q.service_end = timezone.now()
        q.is_active = False
        q.is_completed = True
        q.save(update_fields=['service_end', 'is_active', 'is_completed'])
        return Response(self.get_serializer(q).data)


# ============================================================
# CONSULTATIONS & DIAGNOSES
# ============================================================

class AppointmentViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('patient', 'doctor').all()
    serializer_class = AppointmentSerializer
    list_serializer_class = AppointmentListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'status']
    search_fields = ['patient__first_name', 'patient__last_name', 'reason']
    ordering_fields = ['scheduled_time']

    @action(detail=False, methods=['get'], url_path='today')
    def today(self, request):
        qs = self.get_queryset().filter(scheduled_time__date=timezone.now().date())
        serializer = AppointmentListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming(self, request):
        qs = self.get_queryset().filter(
            scheduled_time__gte=timezone.now(),
            status='SCHEDULED'
        ).order_by('scheduled_time')[:20]
        serializer = AppointmentListSerializer(qs, many=True)
        return Response(serializer.data)


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.select_related('appointment').all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['appointment__patient', 'appointment__doctor']
    search_fields = ['consultation_code', 'diagnosis']

    @action(detail=True, methods=['get'], url_path='diagnoses')
    def diagnoses(self, request, pk=None):
        consultation = self.get_object()
        qs = ConsultationDiagnosis.objects.filter(consultation=consultation)
        serializer = ConsultationDiagnosisSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='prescriptions')
    def prescriptions(self, request, pk=None):
        consultation = self.get_object()
        qs = Prescription.objects.filter(consultation=consultation)
        serializer = PrescriptionSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='lab-orders')
    def lab_orders(self, request, pk=None):
        consultation = self.get_object()
        qs = LabOrder.objects.filter(consultation=consultation)
        serializer = LabOrderListSerializer(qs, many=True)
        return Response(serializer.data)


class PatientMedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = PatientMedicalHistory.objects.all()
    serializer_class = PatientMedicalHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['patient', 'record_type']
    search_fields = ['description', 'record_type']


class ICD10CategoryViewSet(viewsets.ModelViewSet):
    queryset = ICD10Category.objects.all()
    serializer_class = ICD10CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['category_name', 'code_range', 'chapter_number']


class ICD10CodeViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = ICD10Code.objects.select_related('category').all()
    serializer_class = ICD10CodeSerializer
    list_serializer_class = ICD10CodeListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active', 'is_common', 'nhif_eligible', 'sha_covered', 'is_notifiable']
    search_fields = ['code', 'short_description', 'description', 'local_name']
    ordering_fields = ['code', 'usage_count']

    @action(detail=False, methods=['get'], url_path='common')
    def common(self, request):
        qs = self.get_queryset().filter(is_common=True, is_active=True)
        serializer = ICD10CodeListSerializer(qs, many=True)
        return Response(serializer.data)


class ConsultationDiagnosisViewSet(viewsets.ModelViewSet):
    queryset = ConsultationDiagnosis.objects.select_related('consultation', 'icd10_code').all()
    serializer_class = ConsultationDiagnosisSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['consultation', 'diagnosis_type', 'certainty', 'submitted_to_nhif']


# ============================================================
# PHARMACY & MEDICINES
# ============================================================

class MedicineCategoryViewSet(viewsets.ModelViewSet):
    queryset = MedicineCategory.objects.all()
    serializer_class = MedicineCategorySerializer
    permission_classes = [IsAuthenticated]


class MedicineViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Medicine.objects.select_related('category').all()
    serializer_class = MedicineSerializer
    list_serializer_class = MedicineListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'unit_type']
    search_fields = ['name', 'manufacturer', 'batch_number']
    ordering_fields = ['name', 'quantity_in_stock', 'expiry_date']

    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        from django.db.models import F
        qs = self.get_queryset().filter(quantity_in_stock__lte=F('reorder_level'))
        serializer = MedicineListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='expiring')
    def expiring_soon(self, request):
        """Medicines expiring within 90 days."""
        cutoff = timezone.now().date() + timezone.timedelta(days=90)
        qs = self.get_queryset().filter(expiry_date__lte=cutoff, expiry_date__gte=timezone.now().date())
        serializer = MedicineListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='stock-movements')
    def stock_movements(self, request, pk=None):
        medicine = self.get_object()
        qs = StockMovement.objects.filter(medicine=medicine)
        serializer = StockMovementSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='adjust-stock')
    def adjust_stock(self, request, pk=None):
        medicine = self.get_object()
        quantity = request.data.get('quantity')
        reason = request.data.get('reason', 'Manual adjustment')
        if quantity is None:
            return Response({'error': 'quantity required'}, status=status.HTTP_400_BAD_REQUEST)
        quantity = int(quantity)
        prev = medicine.quantity_in_stock
        medicine.quantity_in_stock += quantity
        if medicine.quantity_in_stock < 0:
            return Response({'error': 'Stock cannot go negative.'}, status=status.HTTP_400_BAD_REQUEST)
        medicine.save(update_fields=['quantity_in_stock'])
        StockMovement.objects.create(
            medicine=medicine, movement_type='ADJUSTMENT',
            quantity=quantity, previous_quantity=prev,
            new_quantity=medicine.quantity_in_stock,
            reason=reason, performed_by=request.user
        )
        return Response(MedicineSerializer(medicine).data)


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovement.objects.select_related('medicine').all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['medicine', 'movement_type']
    ordering_fields = ['created_at']


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related('consultation', 'medicine').all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['consultation', 'medicine', 'is_dispensed', 'is_insured']
    ordering_fields = ['prescribed_at']

    @action(detail=True, methods=['post'], url_path='dispense')
    def dispense(self, request, pk=None):
        prescription = self.get_object()
        if prescription.is_dispensed:
            return Response({'error': 'Already dispensed.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            prescription.dispense(request.user)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(PrescriptionSerializer(prescription).data)

    @action(detail=False, methods=['get'], url_path='pending')
    def pending(self, request):
        qs = self.get_queryset().filter(is_dispensed=False)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class MedicineSaleViewSet(viewsets.ModelViewSet):
    queryset = MedicineSale.objects.all()
    serializer_class = MedicineSaleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['payment_method', 'patient']
    ordering_fields = ['sale_date']

    @action(detail=False, methods=['get'], url_path='today')
    def today(self, request):
        qs = self.get_queryset().filter(sale_date__date=timezone.now().date())
        total = qs.aggregate(total=Sum('total_amount'))
        serializer = self.get_serializer(qs, many=True)
        return Response({'sales': serializer.data, 'total_amount': total['total'] or 0})


class OverTheCounterSaleViewSet(viewsets.ModelViewSet):
    queryset = OverTheCounterSale.objects.prefetch_related('items').all()
    serializer_class = OverTheCounterSaleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_status', 'is_dispensed', 'cashier']
    search_fields = ['sale_id', 'customer_name', 'mpesa_code']
    ordering_fields = ['created_at']

    @action(detail=True, methods=['post'], url_path='mark-dispensed')
    def mark_dispensed(self, request, pk=None):
        sale = self.get_object()
        sale.is_dispensed = True
        sale.dispensed_at = timezone.now()
        sale.dispensed_by = request.user
        sale.save(update_fields=['is_dispensed', 'dispensed_at', 'dispensed_by'])
        return Response(self.get_serializer(sale).data)


# ============================================================
# LABORATORY & IMAGING
# ============================================================

class LabTestCategoryViewSet(viewsets.ModelViewSet):
    queryset = LabTestCategory.objects.all()
    serializer_class = LabTestCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category_type', 'is_active']
    search_fields = ['name']


class LabTestViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = LabTest.objects.select_related('category').all()
    serializer_class = LabTestSerializer
    list_serializer_class = LabTestListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'sample_type', 'is_active', 'nhif_covered', 'sha_covered']
    search_fields = ['test_code', 'test_name']
    ordering_fields = ['test_name', 'usage_count']


class LabOrderViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = LabOrder.objects.select_related('patient', 'ordered_by').prefetch_related('test_items').all()
    serializer_class = LabOrderSerializer
    list_serializer_class = LabOrderListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'status', 'priority', 'paid', 'assigned_to']
    search_fields = ['order_number', 'patient__first_name', 'patient__last_name']
    ordering_fields = ['ordered_at', 'created_at']

    @action(detail=False, methods=['get'], url_path='pending')
    def pending(self, request):
        qs = self.get_queryset().filter(status__in=['PENDING', 'SAMPLE_COLLECTED', 'IN_PROGRESS'])
        serializer = LabOrderListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if not new_status:
            return Response({'error': 'status required'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        if new_status == 'SAMPLE_COLLECTED':
            order.sample_collected_at = timezone.now()
        elif new_status == 'COMPLETED':
            order.completed_at = timezone.now()
        elif new_status == 'REPORTED':
            order.reported_at = timezone.now()
        order.save()
        return Response(LabOrderSerializer(order).data)


class LabResultViewSet(viewsets.ModelViewSet):
    queryset = LabResult.objects.select_related('lab_order').all()
    serializer_class = LabResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_critical', 'quality_control_passed', 'patient_notified']

    @action(detail=False, methods=['get'], url_path='critical')
    def critical(self, request):
        qs = self.get_queryset().filter(is_critical=True, critical_value_notified=False)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class ImagingStudyViewSet(viewsets.ModelViewSet):
    queryset = ImagingStudy.objects.select_related('patient').all()
    serializer_class = ImagingStudySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['modality', 'status', 'is_urgent', 'patient']
    search_fields = ['study_description', 'body_part']
    ordering_fields = ['ordered_at', 'created_at']


# ============================================================
# INPATIENT
# ============================================================

class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.prefetch_related('beds').all()
    serializer_class = WardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ward_type', 'is_active']
    search_fields = ['ward_code', 'ward_name']

    @action(detail=True, methods=['get'], url_path='beds')
    def beds(self, request, pk=None):
        ward = self.get_object()
        qs = Bed.objects.filter(ward=ward)
        serializer = BedListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='occupancy')
    def occupancy(self, request):
        wards = self.get_queryset()
        data = []
        for ward in wards:
            data.append({
                'ward_id': ward.id,
                'ward_name': ward.ward_name,
                'ward_type': ward.ward_type,
                'total_beds': ward.total_beds,
                'occupied': ward.occupied_beds_count,
                'available': ward.available_beds_count,
            })
        return Response(data)


class BedViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Bed.objects.select_related('ward').all()
    serializer_class = BedSerializer
    list_serializer_class = BedListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ward', 'status', 'bed_type', 'is_active']
    search_fields = ['bed_number']

    @action(detail=False, methods=['get'], url_path='available')
    def available(self, request):
        qs = self.get_queryset().filter(status='AVAILABLE', is_active=True)
        serializer = BedListSerializer(qs, many=True)
        return Response(serializer.data)


class InpatientAdmissionViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = InpatientAdmission.objects.select_related('patient', 'bed', 'admitting_doctor').all()
    serializer_class = InpatientAdmissionSerializer
    list_serializer_class = InpatientAdmissionListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'admission_type', 'is_critical', 'is_insured', 'patient']
    search_fields = ['admission_number', 'patient__first_name', 'patient__last_name']
    ordering_fields = ['admission_datetime']

    @action(detail=False, methods=['get'], url_path='active')
    def active(self, request):
        qs = self.get_queryset().filter(status='ACTIVE')
        serializer = InpatientAdmissionListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='discharge')
    def discharge(self, request, pk=None):
        admission = self.get_object()
        if admission.status != 'ACTIVE':
            return Response({'error': 'Admission is not active.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            return Response({'error': 'Only doctors can discharge patients.'}, status=status.HTTP_403_FORBIDDEN)
        summary = request.data.get('discharge_summary', '')
        diagnosis = request.data.get('discharge_diagnosis', '')
        admission.discharge(doctor, summary, diagnosis)
        return Response(InpatientAdmissionSerializer(admission).data)

    @action(detail=True, methods=['get'], url_path='charges')
    def charges(self, request, pk=None):
        admission = self.get_object()
        qs = InpatientDailyCharge.objects.filter(admission=admission)
        serializer = InpatientDailyChargeSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='vitals')
    def vitals(self, request, pk=None):
        admission = self.get_object()
        qs = InpatientVitals.objects.filter(admission=admission)
        serializer = InpatientVitalsSerializer(qs, many=True)
        return Response(serializer.data)


class InpatientDailyChargeViewSet(viewsets.ModelViewSet):
    queryset = InpatientDailyCharge.objects.all()
    serializer_class = InpatientDailyChargeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['admission', 'charge_type', 'is_billed', 'is_paid']
    ordering_fields = ['charge_date', 'created_at']


class InpatientVitalsViewSet(viewsets.ModelViewSet):
    queryset = InpatientVitals.objects.all()
    serializer_class = InpatientVitalsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['admission']
    ordering_fields = ['recorded_at']


# ============================================================
# EMERGENCY
# ============================================================

class EmergencyBedViewSet(viewsets.ModelViewSet):
    queryset = EmergencyBed.objects.all()
    serializer_class = EmergencyBedSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'is_active']

    @action(detail=False, methods=['get'], url_path='available')
    def available(self, request):
        qs = self.get_queryset().filter(status='AVAILABLE', is_active=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class EmergencyVisitViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = EmergencyVisit.objects.select_related('visit').prefetch_related('charges', 'payments').all()
    serializer_class = EmergencyVisitSerializer
    list_serializer_class = EmergencyVisitListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['triage_level', 'treatment_status', 'payment_status', 'police_case']
    search_fields = ['visit__visit_number', 'ob_number']
    ordering_fields = ['created_at']

    @action(detail=False, methods=['get'], url_path='active')
    def active(self, request):
        qs = self.get_queryset().filter(treatment_status='IN_EMERGENCY')
        serializer = EmergencyVisitListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='critical')
    def critical(self, request):
        qs = self.get_queryset().filter(triage_level='RED')
        serializer = EmergencyVisitListSerializer(qs, many=True)
        return Response(serializer.data)


class EmergencyChargeViewSet(viewsets.ModelViewSet):
    queryset = EmergencyCharge.objects.all()
    serializer_class = EmergencyChargeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['emergency_visit', 'charge_type']


class EmergencyPaymentViewSet(viewsets.ModelViewSet):
    queryset = EmergencyPayment.objects.all()
    serializer_class = EmergencyPaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['emergency_visit', 'payment_method']


# ============================================================
# MATERNITY & MCH
# ============================================================

class MaternityVisitViewSet(viewsets.ModelViewSet):
    queryset = MaternityVisit.objects.select_related('visit').all()
    serializer_class = MaternityVisitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['visit_purpose', 'is_in_labor', 'is_high_risk', 'needs_csection']
    ordering_fields = ['created_at']

    @action(detail=False, methods=['get'], url_path='in-labor')
    def in_labor(self, request):
        qs = self.get_queryset().filter(is_in_labor=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='high-risk')
    def high_risk(self, request):
        qs = self.get_queryset().filter(is_high_risk=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class MCHVisitViewSet(viewsets.ModelViewSet):
    queryset = MCHVisit.objects.select_related('visit').all()
    serializer_class = MCHVisitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['visit_type', 'immunization_due', 'has_danger_signs', 'needs_doctor_consultation']


# ============================================================
# INPATIENT MEDICINE REQUESTS
# ============================================================

class InpatientMedicineRequestViewSet(viewsets.ModelViewSet):
    queryset = InpatientMedicineRequest.objects.select_related('admission', 'medicine').all()
    serializer_class = InpatientMedicineRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['admission', 'status', 'priority', 'medicine']
    search_fields = ['request_number', 'medicine__name']
    ordering_fields = ['requested_at']

    @action(detail=False, methods=['get'], url_path='pending')
    def pending(self, request):
        qs = self.get_queryset().filter(status='PENDING')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        req = self.get_object()
        qty = request.data.get('quantity_approved', req.quantity_requested)
        req.status = 'APPROVED'
        req.approved_by = request.user
        req.approved_at = timezone.now()
        req.quantity_approved = qty
        req.save(update_fields=['status', 'approved_by', 'approved_at', 'quantity_approved'])
        return Response(self.get_serializer(req).data)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        req = self.get_object()
        reason = request.data.get('rejection_reason', '')
        req.status = 'REJECTED'
        req.rejection_reason = reason
        req.save(update_fields=['status', 'rejection_reason'])
        return Response(self.get_serializer(req).data)


# ============================================================
# PROCUREMENT
# ============================================================

class SupplierViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    list_serializer_class = SupplierListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['supplier_type', 'status', 'city', 'county']
    search_fields = ['supplier_name', 'contact_person', 'phone_number', 'email', 'pin_number']
    ordering_fields = ['created_at', 'supplier_name']


class PurchaseRequestViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = PurchaseRequest.objects.prefetch_related('items').all()
    serializer_class = PurchaseRequestSerializer
    list_serializer_class = PurchaseRequestListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['requesting_department', 'status', 'urgency']
    search_fields = ['request_number', 'purpose']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='approve-hod')
    def approve_hod(self, request, pk=None):
        pr = self.get_object()
        pr.status = 'APPROVED'
        pr.hod_approved_by = request.user
        pr.hod_approved_at = timezone.now()
        pr.hod_comments = request.data.get('comments', '')
        pr.save(update_fields=['status', 'hod_approved_by', 'hod_approved_at', 'hod_comments'])
        return Response(PurchaseRequestSerializer(pr).data)

    @action(detail=True, methods=['post'], url_path='approve-accountant')
    def approve_accountant(self, request, pk=None):
        pr = self.get_object()
        pr.status = 'APPROVED_ACCOUNTANT'
        pr.accountant_approved_by = request.user
        pr.accountant_approved_at = timezone.now()
        pr.save(update_fields=['status', 'accountant_approved_by', 'accountant_approved_at'])
        return Response(PurchaseRequestSerializer(pr).data)

    @action(detail=True, methods=['post'], url_path='approve-procurement')
    def approve_procurement(self, request, pk=None):
        pr = self.get_object()
        pr.status = 'APPROVED_PROCUREMENT'
        pr.procurement_approved_by = request.user
        pr.procurement_approved_at = timezone.now()
        pr.save(update_fields=['status', 'procurement_approved_by', 'procurement_approved_at'])
        return Response(PurchaseRequestSerializer(pr).data)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        pr = self.get_object()
        pr.status = 'REJECTED'
        pr.rejected_by = request.user
        pr.rejected_at = timezone.now()
        pr.rejection_reason = request.data.get('rejection_reason', '')
        pr.save(update_fields=['status', 'rejected_by', 'rejected_at', 'rejection_reason'])
        return Response(PurchaseRequestSerializer(pr).data)


class PurchaseOrderViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.select_related('supplier').prefetch_related('items').all()
    serializer_class = PurchaseOrderSerializer
    list_serializer_class = PurchaseOrderListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['supplier', 'status']
    search_fields = ['po_number']
    ordering_fields = ['po_date', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class GoodsReceivedNoteViewSet(viewsets.ModelViewSet):
    queryset = GoodsReceivedNote.objects.prefetch_related('items').all()
    serializer_class = GoodsReceivedNoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['purchase_order', 'status', 'has_quality_issues']
    ordering_fields = ['delivery_date', 'created_at']

    def perform_create(self, serializer):
        serializer.save(received_by=self.request.user)


# ============================================================
# INSURANCE CLAIMS
# ============================================================

class ConsultationInsuranceClaimViewSet(viewsets.ModelViewSet):
    queryset = ConsultationInsuranceClaim.objects.all()
    serializer_class = ConsultationInsuranceClaimSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'insurance_provider', 'patient', 'claims_officer_approved']
    search_fields = ['claim_number', 'member_number']
    ordering_fields = ['created_at']

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        claim = self.get_object()
        claim.status = 'APPROVED'
        claim.claims_officer_approved = True
        claim.claims_officer = request.user
        claim.claims_officer_approved_at = timezone.now()
        claim.claims_officer_comments = request.data.get('comments', '')
        claim.save()
        return Response(self.get_serializer(claim).data)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        claim = self.get_object()
        claim.status = 'REJECTED'
        claim.rejected_by = request.user
        claim.rejected_at = timezone.now()
        claim.rejection_reason = request.data.get('rejection_reason', '')
        claim.save()
        return Response(self.get_serializer(claim).data)


class PharmacyInsuranceClaimViewSet(viewsets.ModelViewSet):
    queryset = PharmacyInsuranceClaim.objects.all()
    serializer_class = PharmacyInsuranceClaimSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'insurance_provider', 'claim_type', 'patient']
    search_fields = ['claim_number', 'member_number', 'member_name']
    ordering_fields = ['created_at']

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        claim = self.get_object()
        claim.status = 'APPROVED'
        claim.claims_officer_approved = True
        claim.claims_officer = request.user
        claim.claims_approved_at = timezone.now()
        claim.save()
        return Response(self.get_serializer(claim).data)


class InpatientInsuranceClaimViewSet(viewsets.ModelViewSet):
    queryset = InpatientInsuranceClaim.objects.all()
    serializer_class = InpatientInsuranceClaimSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'insurance_provider']
    search_fields = ['claim_number', 'member_number']
    ordering_fields = ['created_at']


# ============================================================
# SHA
# ============================================================

class SHAMemberViewSet(viewsets.ModelViewSet):
    queryset = SHAMember.objects.select_related('patient').all()
    serializer_class = SHAMemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['sha_number', 'patient__first_name', 'patient__last_name']

    @action(detail=True, methods=['get'], url_path='claims')
    def claims(self, request, pk=None):
        member = self.get_object()
        qs = SHAClaim.objects.filter(sha_member=member)
        serializer = SHAClaimSerializer(qs, many=True)
        return Response(serializer.data)


class SHAClaimViewSet(viewsets.ModelViewSet):
    queryset = SHAClaim.objects.all()
    serializer_class = SHAClaimSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'claim_type', 'sha_member']
    search_fields = ['claim_number', 'sha_reference']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)


# ============================================================
# PAYMENT & BILLING
# ============================================================

class PaymentAuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentAuditLog.objects.all()
    serializer_class = PaymentAuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'status', 'payment_method', 'patient']
    search_fields = ['transaction_id', 'mpesa_code', 'mpesa_phone']
    ordering_fields = ['created_at']

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        today = timezone.now().date()
        qs = self.get_queryset().filter(created_at__date=today)
        total = qs.aggregate(total=Sum('amount'))
        by_method = qs.values('payment_method').annotate(subtotal=Sum('amount'), count=Count('id'))
        return Response({
            'date': str(today),
            'total_amount': total['total'] or 0,
            'by_payment_method': list(by_method),
        })


class CashierSessionViewSet(viewsets.ModelViewSet):
    queryset = CashierSession.objects.all()
    serializer_class = CashierSessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['cashier', 'status']
    ordering_fields = ['opened_at']

    @action(detail=True, methods=['post'], url_path='close')
    def close_session(self, request, pk=None):
        session = self.get_object()
        session.status = 'CLOSED'
        session.closed_at = timezone.now()
        session.actual_cash = request.data.get('actual_cash', 0)
        session.cash_variance = float(session.actual_cash) - float(session.expected_cash)
        session.save()
        return Response(self.get_serializer(session).data)


class MPesaDuplicateCheckViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MPesaDuplicateCheck.objects.all()
    serializer_class = MPesaDuplicateCheckSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['mpesa_code']


# ============================================================
# eTIMS
# ============================================================

class eTIMSConfigurationViewSet(viewsets.ModelViewSet):
    queryset = eTIMSConfiguration.objects.all()
    serializer_class = eTIMSConfigurationSerializer
    permission_classes = [IsAdminUser]


class eTIMSInvoiceViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = eTIMSInvoice.objects.prefetch_related('items').all()
    serializer_class = eTIMSInvoiceSerializer
    list_serializer_class = eTIMSInvoiceListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['invoice_type', 'status', 'payment_status', 'submitted_to_etims']
    search_fields = ['invoice_number', 'customer_name', 'mpesa_code', 'etims_invoice_number']
    ordering_fields = ['invoice_date', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='submit')
    def submit_to_etims(self, request, pk=None):
        invoice = self.get_object()
        # Placeholder: integrate with KRA eTIMS API here
        invoice.submitted_to_etims = True
        invoice.submitted_at = timezone.now()
        invoice.status = 'SUBMITTED'
        invoice.save(update_fields=['submitted_to_etims', 'submitted_at', 'status'])
        return Response(eTIMSInvoiceSerializer(invoice).data)

    @action(detail=False, methods=['get'], url_path='unsubmitted')
    def unsubmitted(self, request):
        qs = self.get_queryset().filter(submitted_to_etims=False, status='DRAFT')
        serializer = eTIMSInvoiceListSerializer(qs, many=True)
        return Response(serializer.data)


# ============================================================
# HR — ATTENDANCE & LEAVE
# ============================================================

class HospitalWiFiNetworkViewSet(viewsets.ModelViewSet):
    queryset = HospitalWiFiNetwork.objects.all()
    serializer_class = HospitalWiFiNetworkSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']


class AttendanceQRCodeViewSet(viewsets.ModelViewSet):
    queryset = AttendanceQRCode.objects.all()
    serializer_class = AttendanceQRCodeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['qr_type', 'is_active', 'attendance_date']
    ordering_fields = ['created_at']

    @action(detail=False, methods=['get'], url_path='today')
    def today(self, request):
        qs = self.get_queryset().filter(attendance_date=timezone.now().date(), is_active=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class AttendanceViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('user').all()
    serializer_class = AttendanceSerializer
    list_serializer_class = AttendanceListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'status', 'date', 'is_manual']
    search_fields = ['user__first_name', 'user__last_name']
    ordering_fields = ['date']

    @action(detail=False, methods=['get'], url_path='today')
    def today(self, request):
        qs = self.get_queryset().filter(date=timezone.now().date())
        serializer = AttendanceListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='my-attendance')
    def my_attendance(self, request):
        qs = self.get_queryset().filter(user=request.user).order_by('-date')
        serializer = AttendanceListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='check-in')
    def check_in(self, request, pk=None):
        attendance = self.get_object()
        if attendance.check_in_time:
            return Response({'error': 'Already checked in.'}, status=status.HTTP_400_BAD_REQUEST)
        attendance.check_in_time = timezone.now()
        attendance.status = 'PRESENT'
        attendance.check_in_ip = request.META.get('REMOTE_ADDR')
        attendance.save(update_fields=['check_in_time', 'status', 'check_in_ip'])
        return Response(AttendanceSerializer(attendance).data)

    @action(detail=True, methods=['post'], url_path='check-out')
    def check_out(self, request, pk=None):
        attendance = self.get_object()
        if not attendance.check_in_time:
            return Response({'error': 'Not checked in yet.'}, status=status.HTTP_400_BAD_REQUEST)
        if attendance.check_out_time:
            return Response({'error': 'Already checked out.'}, status=status.HTTP_400_BAD_REQUEST)
        attendance.check_out_time = timezone.now()
        attendance.check_out_ip = request.META.get('REMOTE_ADDR')
        attendance.save(update_fields=['check_out_time', 'check_out_ip'])
        attendance.calculate_hours()
        return Response(AttendanceSerializer(attendance).data)


class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'is_paid', 'requires_hr_approval']


class LeaveApplicationViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = LeaveApplication.objects.select_related('user', 'leave_type').all()
    serializer_class = LeaveApplicationSerializer
    list_serializer_class = LeaveApplicationListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'leave_type', 'status']
    search_fields = ['application_number', 'user__first_name', 'user__last_name']
    ordering_fields = ['created_at', 'start_date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='my-applications')
    def my_applications(self, request):
        qs = self.get_queryset().filter(user=request.user)
        serializer = LeaveApplicationListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='approve-supervisor')
    def approve_supervisor(self, request, pk=None):
        app = self.get_object()
        app.supervisor_approved = True
        app.supervisor_approved_by = request.user
        app.supervisor_approved_at = timezone.now()
        app.supervisor_comments = request.data.get('comments', '')
        app.status = 'SUPERVISOR_APPROVED'
        app.save()
        return Response(LeaveApplicationSerializer(app).data)

    @action(detail=True, methods=['post'], url_path='approve-hr')
    def approve_hr(self, request, pk=None):
        app = self.get_object()
        app.hr_approved = True
        app.hr_approved_by = request.user
        app.hr_approved_at = timezone.now()
        app.hr_comments = request.data.get('comments', '')
        app.status = 'APPROVED'
        app.save()
        return Response(LeaveApplicationSerializer(app).data)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        app = self.get_object()
        app.status = 'REJECTED'
        app.rejected_by = request.user
        app.rejected_at = timezone.now()
        app.rejection_reason = request.data.get('rejection_reason', '')
        app.save()
        return Response(LeaveApplicationSerializer(app).data)


# ============================================================
# ASSETS
# ============================================================

class HospitalAssetViewSet(ListDetailSerializerMixin, viewsets.ModelViewSet):
    queryset = HospitalAsset.objects.all()
    serializer_class = HospitalAssetSerializer
    list_serializer_class = HospitalAssetListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'condition', 'needs_replacement', 'requires_maintenance', 'location']
    search_fields = ['asset_id', 'asset_name', 'serial_number', 'model_number']
    ordering_fields = ['created_at', 'next_maintenance_date']

    @action(detail=False, methods=['get'], url_path='maintenance-due')
    def maintenance_due(self, request):
        today = timezone.now().date()
        qs = self.get_queryset().filter(next_maintenance_date__lte=today, status='OPERATIONAL')
        serializer = HospitalAssetListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='needs-replacement')
    def needs_replacement(self, request):
        qs = self.get_queryset().filter(needs_replacement=True)
        serializer = HospitalAssetListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='maintenance-logs')
    def maintenance_logs(self, request, pk=None):
        asset = self.get_object()
        qs = AssetMaintenanceLog.objects.filter(asset=asset)
        serializer = AssetMaintenanceLogSerializer(qs, many=True)
        return Response(serializer.data)


class AssetMaintenanceLogViewSet(viewsets.ModelViewSet):
    queryset = AssetMaintenanceLog.objects.select_related('asset').all()
    serializer_class = AssetMaintenanceLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['asset', 'maintenance_type', 'is_completed']
    ordering_fields = ['maintenance_date', 'created_at']

    def perform_create(self, serializer):
        serializer.save(logged_by=self.request.user)


# ============================================================
# AUDIT, SECURITY & NOTIFICATIONS
# ============================================================

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'action', 'table_affected']
    search_fields = ['description', 'record_id']
    ordering_fields = ['timestamp']


class SecurityThreatViewSet(viewsets.ModelViewSet):
    queryset = SecurityThreat.objects.all()
    serializer_class = SecurityThreatSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['threat_type', 'severity', 'blocked', 'resolved']
    ordering_fields = ['detected_at']

    @action(detail=True, methods=['post'], url_path='resolve')
    def resolve(self, request, pk=None):
        threat = self.get_object()
        threat.resolved = True
        threat.resolved_by = request.user
        threat.resolved_at = timezone.now()
        threat.resolution_notes = request.data.get('notes', '')
        threat.save()
        return Response(self.get_serializer(threat).data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['recipient', 'notification_type', 'is_read', 'is_urgent']
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Regular users only see their own notifications
        user = self.request.user
        if user.user_type == 'ADMIN':
            return super().get_queryset()
        return super().get_queryset().filter(recipient=user)

    @action(detail=False, methods=['get'], url_path='unread')
    def unread(self, request):
        qs = self.get_queryset().filter(is_read=False, recipient=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response({'count': qs.count(), 'notifications': serializer.data})

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'detail': 'Marked as read.'})

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        self.get_queryset().filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({'detail': 'All notifications marked as read.'})


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participant1', 'participant2', 'patient']

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(
            Q(participant1=user) | Q(participant2=user)
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer

    @action(detail=True, methods=['get'], url_path='messages')
    def messages(self, request, pk=None):
        conversation = self.get_object()
        # Mark incoming messages as read
        conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
        qs = conversation.messages.all()
        serializer = MessageSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='send')
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        content = request.data.get('content')
        if not content:
            return Response({'error': 'content required'}, status=status.HTTP_400_BAD_REQUEST)
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conversation', 'sender', 'is_read']
    ordering_fields = ['timestamp']

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


# ============================================================
# DASHBOARD / ANALYTICS
# ============================================================

from rest_framework.views import APIView


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        data = {
            'today': {
                'visits': PatientVisit.objects.filter(created_at__date=today).count(),
                'appointments': Appointment.objects.filter(scheduled_time__date=today).count(),
                'lab_orders': LabOrder.objects.filter(created_at__date=today).count(),
                'admissions': InpatientAdmission.objects.filter(created_at__date=today).count(),
                'emergency_visits': EmergencyVisit.objects.filter(created_at__date=today).count(),
            },
            'active': {
                'inpatients': InpatientAdmission.objects.filter(status='ACTIVE').count(),
                'emergency': EmergencyVisit.objects.filter(treatment_status='IN_EMERGENCY').count(),
                'pending_lab_orders': LabOrder.objects.filter(status__in=['PENDING', 'IN_PROGRESS']).count(),
                'pending_prescriptions': Prescription.objects.filter(is_dispensed=False).count(),
            },
            'inventory': {
                'low_stock_medicines': Medicine.objects.filter(
                    quantity_in_stock__lte=Medicine._meta.get_field('reorder_level').default
                ).count(),
                'total_medicines': Medicine.objects.count(),
            },
            'beds': {
                'total': Bed.objects.filter(is_active=True).count(),
                'available': Bed.objects.filter(status='AVAILABLE', is_active=True).count(),
                'occupied': Bed.objects.filter(status='OCCUPIED').count(),
            },
            'claims': {
                'pending_consultation': ConsultationInsuranceClaim.objects.filter(status='PENDING').count(),
                'pending_pharmacy': PharmacyInsuranceClaim.objects.filter(status='PENDING').count(),
                'pending_inpatient': InpatientInsuranceClaim.objects.filter(status__in=['DRAFT', 'SUBMITTED']).count(),
                'pending_sha': SHAClaim.objects.filter(status__in=['DRAFT', 'SUBMITTED']).count(),
            },
        }
        return Response(data)