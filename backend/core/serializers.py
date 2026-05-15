"""
AfyaBoraHMIS — serializers.py
Django REST Framework serializers for all models.
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
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


# ============================================================
# AUTH & USERS
# ============================================================

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'full_name',
            'email', 'user_type', 'phone_number', 'specialization',
            'license_number', 'is_active', 'date_joined',
        ]
        read_only_fields = ['id', 'date_joined']

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'user_type', 'phone_number', 'specialization',
            'license_number', 'password', 'password2',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email',
            'phone_number', 'specialization', 'license_number', 'is_active',
        ]


class LoginAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginAttempt
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']


class AccountLockSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_currently_locked = serializers.SerializerMethodField()

    class Meta:
        model = AccountLock
        fields = '__all__'
        read_only_fields = ['id', 'locked_at']

    def get_is_currently_locked(self, obj):
        return obj.is_account_locked()


class TwoFactorCodeSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = TwoFactorCode
        fields = ['id', 'user', 'code', 'created_at', 'expires_at', 'used', 'is_valid']
        read_only_fields = ['id', 'code', 'created_at', 'expires_at']

    def get_is_valid(self, obj):
        return obj.is_valid()


class UserSessionSerializer(serializers.ModelSerializer):
    user_display = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = UserSession
        fields = '__all__'
        read_only_fields = ['id', 'login_time', 'last_activity']


# ============================================================
# CORE CLINICAL
# ============================================================

class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_age(self, obj):
        today = timezone.now().date()
        dob = obj.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


class PatientListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender',
                  'phone_number', 'id_number', 'blood_type']


class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class DoctorListSerializer(serializers.ModelSerializer):
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'specialization',
                  'specialization_display', 'phone_number', 'department', 'is_active']


class NurseSerializer(serializers.ModelSerializer):
    nurse_type_display = serializers.CharField(source='get_nurse_type_display', read_only=True)
    department_display = serializers.CharField(source='get_department_display', read_only=True)

    class Meta:
        model = Nurse
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class NurseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = ['id', 'first_name', 'last_name', 'nurse_type',
                  'department', 'phone_number', 'is_active', 'is_charge_nurse']


# ============================================================
# FACILITY & LOOKUP
# ============================================================

class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProvider
        fields = '__all__'


class SpecializedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecializedService
        fields = '__all__'


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'


class ClinicSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicSettings
        fields = '__all__'


# ============================================================
# VISITS, TRIAGE & QUEUE
# ============================================================

class TriageCategorySerializer(serializers.ModelSerializer):
    priority_display = serializers.CharField(source='get_priority_level_display', read_only=True)

    class Meta:
        model = TriageCategory
        fields = '__all__'


class PatientVisitSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    nurse_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    visit_type_display = serializers.CharField(source='get_visit_type_display', read_only=True)

    class Meta:
        model = PatientVisit
        fields = '__all__'
        read_only_fields = ['id', 'visit_number', 'created_at', 'updated_at']

    def get_patient_name(self, obj):
        return str(obj.patient)

    def get_doctor_name(self, obj):
        return str(obj.assigned_doctor) if obj.assigned_doctor else None

    def get_nurse_name(self, obj):
        return str(obj.assigned_nurse) if obj.assigned_nurse else None


class PatientVisitListSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PatientVisit
        fields = ['id', 'visit_number', 'patient', 'patient_name',
                  'visit_type', 'status', 'status_display', 'arrival_time']

    def get_patient_name(self, obj):
        return str(obj.patient)


class TriageAssessmentSerializer(serializers.ModelSerializer):
    bmi = serializers.FloatField(read_only=True)
    visit_number = serializers.CharField(source='visit.visit_number', read_only=True)
    assessed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = TriageAssessment
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def get_assessed_by_name(self, obj):
        return str(obj.assessed_by) if obj.assessed_by else None


class QueueManagementSerializer(serializers.ModelSerializer):
    visit_number = serializers.CharField(source='visit.visit_number', read_only=True)
    wait_time_minutes = serializers.SerializerMethodField()

    class Meta:
        model = QueueManagement
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def get_wait_time_minutes(self, obj):
        if obj.joined_queue and obj.service_start:
            delta = obj.service_start - obj.joined_queue
            return int(delta.total_seconds() / 60)
        if obj.joined_queue and obj.is_active:
            delta = timezone.now() - obj.joined_queue
            return int(delta.total_seconds() / 60)
        return None


# ============================================================
# CONSULTATIONS & DIAGNOSES
# ============================================================

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_patient_name(self, obj):
        return str(obj.patient)

    def get_doctor_name(self, obj):
        return obj.doctor.get_full_name()


class AppointmentListSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'patient_name', 'doctor', 'doctor_name',
                  'scheduled_time', 'status', 'reason']

    def get_patient_name(self, obj):
        return str(obj.patient)

    def get_doctor_name(self, obj):
        return obj.doctor.get_full_name()


class ConsultationSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = Consultation
        fields = '__all__'
        read_only_fields = ['id', 'consultation_code', 'created_at', 'updated_at']

    def get_patient_name(self, obj):
        return str(obj.appointment.patient)

    def get_doctor_name(self, obj):
        return obj.appointment.doctor.get_full_name()


class PatientMedicalHistorySerializer(serializers.ModelSerializer):
    recorded_by_name = serializers.CharField(source='recorded_by.get_full_name', read_only=True)

    class Meta:
        model = PatientMedicalHistory
        fields = '__all__'
        read_only_fields = ['id', 'date_recorded']


class ICD10CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ICD10Category
        fields = '__all__'


class ICD10CodeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)

    class Meta:
        model = ICD10Code
        fields = '__all__'
        read_only_fields = ['id', 'usage_count', 'created_at']


class ICD10CodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICD10Code
        fields = ['id', 'code', 'short_description', 'local_name',
                  'is_common', 'nhif_eligible', 'sha_covered']


class ConsultationDiagnosisSerializer(serializers.ModelSerializer):
    icd10_display = serializers.CharField(source='icd10_code.__str__', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = ConsultationDiagnosis
        fields = '__all__'
        read_only_fields = ['id', 'diagnosed_date', 'created_at']


# ============================================================
# PHARMACY & MEDICINES
# ============================================================

class MedicineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCategory
        fields = '__all__'


class MedicineSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.BooleanField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    unit_type_display = serializers.CharField(source='get_unit_type_display', read_only=True)

    class Meta:
        model = Medicine
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class MedicineListSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Medicine
        fields = ['id', 'name', 'unit_type', 'units_per_pack', 'pack_name',
                  'quantity_in_stock', 'reorder_level', 'is_low_stock',
                  'price_per_unit_cash', 'price_per_unit_insurance', 'expiry_date']


class StockMovementSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    performed_by_name = serializers.CharField(source='performed_by.get_full_name', read_only=True)

    class Meta:
        model = StockMovement
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class PrescriptionSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    patient_name = serializers.SerializerMethodField()
    dispensed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = '__all__'
        read_only_fields = ['id', 'unit_price', 'total_price',
                            'is_dispensed', 'dispensed_at', 'dispensed_by', 'prescribed_at']

    def get_patient_name(self, obj):
        return str(obj.consultation.appointment.patient)

    def get_dispensed_by_name(self, obj):
        return obj.dispensed_by.get_full_name() if obj.dispensed_by else None


class MedicineSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineSale
        fields = '__all__'
        read_only_fields = ['id', 'sale_date']


class SoldMedicineSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = SoldMedicine
        fields = '__all__'


class OverTheCounterSaleSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = OverTheCounterSale
        fields = '__all__'
        read_only_fields = ['id', 'sale_id', 'created_at', 'updated_at']

    def get_items(self, obj):
        return OverTheCounterSaleItemSerializer(obj.items.all(), many=True).data


class OverTheCounterSaleItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = OverTheCounterSaleItem
        fields = '__all__'
        read_only_fields = ['id', 'subtotal', 'created_at']


# ============================================================
# LABORATORY & IMAGING
# ============================================================

class LabTestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestCategory
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class LabTestSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = LabTest
        fields = '__all__'
        read_only_fields = ['id', 'usage_count', 'created_at']


class LabTestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ['id', 'test_code', 'test_name', 'sample_type',
                  'cost', 'turnaround_time', 'nhif_covered', 'sha_covered']


class LabOrderItemSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.test_name', read_only=True)
    test_code = serializers.CharField(source='test.test_code', read_only=True)
    performed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = LabOrderItem
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def get_performed_by_name(self, obj):
        return obj.performed_by.get_full_name() if obj.performed_by else None


class LabOrderSerializer(serializers.ModelSerializer):
    test_items = LabOrderItemSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    ordered_by_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = LabOrder
        fields = '__all__'
        read_only_fields = ['id', 'order_number', 'created_at', 'ordered_at']

    def get_ordered_by_name(self, obj):
        return obj.ordered_by.get_full_name() if obj.ordered_by else None


class LabOrderListSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)

    class Meta:
        model = LabOrder
        fields = ['id', 'order_number', 'patient', 'patient_name',
                  'priority', 'status', 'ordered_at', 'total_cost', 'paid']


class LabResultSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='lab_order.order_number', read_only=True)
    result_by_name = serializers.SerializerMethodField()
    verified_by_name = serializers.SerializerMethodField()

    class Meta:
        model = LabResult
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def get_result_by_name(self, obj):
        return obj.result_by.get_full_name() if obj.result_by else None

    def get_verified_by_name(self, obj):
        return obj.verified_by.get_full_name() if obj.verified_by else None


class ImagingStudySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    modality_display = serializers.CharField(source='get_modality_display', read_only=True)
    ordered_by_name = serializers.SerializerMethodField()

    class Meta:
        model = ImagingStudy
        fields = '__all__'
        read_only_fields = ['id', 'ordered_at', 'created_at']

    def get_ordered_by_name(self, obj):
        return obj.ordered_by.get_full_name() if obj.ordered_by else None


# ============================================================
# INPATIENT
# ============================================================

class WardSerializer(serializers.ModelSerializer):
    occupied_beds_count = serializers.IntegerField(read_only=True)
    available_beds_count = serializers.IntegerField(read_only=True)
    ward_type_display = serializers.CharField(source='get_ward_type_display', read_only=True)

    class Meta:
        model = Ward
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class BedSerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source='ward.ward_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Bed
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class BedListSerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source='ward.ward_name', read_only=True)

    class Meta:
        model = Bed
        fields = ['id', 'bed_number', 'ward', 'ward_name', 'bed_type',
                  'status', 'daily_rate', 'has_oxygen', 'has_monitor']


class InpatientAdmissionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    bed_number = serializers.CharField(source='bed.bed_number', read_only=True)
    ward_name = serializers.SerializerMethodField()
    length_of_stay = serializers.IntegerField(read_only=True)
    outstanding_balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = InpatientAdmission
        fields = '__all__'
        read_only_fields = ['id', 'admission_number', 'created_at', 'updated_at']

    def get_ward_name(self, obj):
        return obj.bed.ward.ward_name if obj.bed else None


class InpatientAdmissionListSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    length_of_stay = serializers.IntegerField(read_only=True)

    class Meta:
        model = InpatientAdmission
        fields = ['id', 'admission_number', 'patient', 'patient_name',
                  'status', 'admission_datetime', 'length_of_stay',
                  'total_charges', 'amount_paid']


class InpatientDailyChargeSerializer(serializers.ModelSerializer):
    charge_type_display = serializers.CharField(source='get_charge_type_display', read_only=True)
    rendered_by_name = serializers.SerializerMethodField()

    class Meta:
        model = InpatientDailyCharge
        fields = '__all__'
        read_only_fields = ['id', 'total_amount', 'created_at']

    def get_rendered_by_name(self, obj):
        return obj.rendered_by.get_full_name() if obj.rendered_by else None


class InpatientVitalsSerializer(serializers.ModelSerializer):
    recorded_by_name = serializers.SerializerMethodField()

    class Meta:
        model = InpatientVitals
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def get_recorded_by_name(self, obj):
        return str(obj.recorded_by) if obj.recorded_by else None


# ============================================================
# EMERGENCY
# ============================================================

class EmergencyBedSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyBed
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class EmergencyChargeSerializer(serializers.ModelSerializer):
    charge_type_display = serializers.CharField(source='get_charge_type_display', read_only=True)

    class Meta:
        model = EmergencyCharge
        fields = '__all__'
        read_only_fields = ['id', 'total_amount', 'created_at']


class EmergencyPaymentSerializer(serializers.ModelSerializer):
    processed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = EmergencyPayment
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def get_processed_by_name(self, obj):
        return obj.processed_by.get_full_name() if obj.processed_by else None


class EmergencyVisitSerializer(serializers.ModelSerializer):
    charges = EmergencyChargeSerializer(many=True, read_only=True)
    payments = EmergencyPaymentSerializer(many=True, read_only=True)
    monitoring_hours = serializers.IntegerField(read_only=True)
    triage_level_display = serializers.CharField(source='get_triage_level_display', read_only=True)
    visit_number = serializers.CharField(source='visit.visit_number', read_only=True)

    class Meta:
        model = EmergencyVisit
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmergencyVisitListSerializer(serializers.ModelSerializer):
    visit_number = serializers.CharField(source='visit.visit_number', read_only=True)
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = EmergencyVisit
        fields = ['id', 'visit', 'visit_number', 'patient_name',
                  'triage_level', 'arrival_mode', 'treatment_status',
                  'total_charges', 'payment_status', 'created_at']

    def get_patient_name(self, obj):
        return str(obj.visit.patient)


# ============================================================
# MATERNITY & MCH
# ============================================================

class MaternityVisitSerializer(serializers.ModelSerializer):
    visit_number = serializers.CharField(source='visit.visit_number', read_only=True)
    assessed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = MaternityVisit
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def get_assessed_by_name(self, obj):
        return str(obj.assessed_by) if obj.assessed_by else None


class MCHVisitSerializer(serializers.ModelSerializer):
    visit_number = serializers.CharField(source='visit.visit_number', read_only=True)

    class Meta:
        model = MCHVisit
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


# ============================================================
# INPATIENT MEDICINE REQUESTS
# ============================================================

class InpatientMedicineRequestSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    patient_name = serializers.SerializerMethodField()
    requested_by_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = InpatientMedicineRequest
        fields = '__all__'
        read_only_fields = ['id', 'request_number', 'requested_at', 'updated_at']

    def get_patient_name(self, obj):
        return str(obj.admission.patient)

    def get_requested_by_name(self, obj):
        return str(obj.requested_by) if obj.requested_by else None


# ============================================================
# PROCUREMENT
# ============================================================

class SupplierSerializer(serializers.ModelSerializer):
    supplier_type_display = serializers.CharField(source='get_supplier_type_display', read_only=True)

    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['id', 'supplier_code', 'created_at', 'updated_at']


class SupplierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'supplier_code', 'supplier_name', 'supplier_type',
                  'contact_person', 'phone_number', 'email', 'status']


class PurchaseRequestItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = PurchaseRequestItem
        fields = '__all__'
        read_only_fields = ['id', 'estimated_total', 'created_at']


class PurchaseRequestSerializer(serializers.ModelSerializer):
    items = PurchaseRequestItemSerializer(many=True, read_only=True)
    requested_by_name = serializers.CharField(source='requested_by.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PurchaseRequest
        fields = '__all__'
        read_only_fields = ['id', 'request_number', 'created_at', 'updated_at']


class PurchaseRequestListSerializer(serializers.ModelSerializer):
    requested_by_name = serializers.CharField(source='requested_by.get_full_name', read_only=True)

    class Meta:
        model = PurchaseRequest
        fields = ['id', 'request_number', 'requesting_department',
                  'requested_by', 'requested_by_name', 'urgency',
                  'status', 'estimated_cost', 'created_at']


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    quantity_pending = serializers.IntegerField(read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'
        read_only_fields = ['id', 'total_price', 'created_at']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ['id', 'po_number', 'created_at', 'updated_at']


class PurchaseOrderListSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'supplier', 'supplier_name',
                  'po_date', 'total_amount', 'status']


class GoodsReceivedNoteItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='po_item.item_name', read_only=True)

    class Meta:
        model = GoodsReceivedNoteItem
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class GoodsReceivedNoteSerializer(serializers.ModelSerializer):
    items = GoodsReceivedNoteItemSerializer(many=True, read_only=True)
    po_number = serializers.CharField(source='purchase_order.po_number', read_only=True)
    received_by_name = serializers.SerializerMethodField()

    class Meta:
        model = GoodsReceivedNote
        fields = '__all__'
        read_only_fields = ['id', 'grn_number', 'created_at', 'updated_at']

    def get_received_by_name(self, obj):
        return obj.received_by.get_full_name() if obj.received_by else None


# ============================================================
# INSURANCE CLAIMS
# ============================================================

class ConsultationInsuranceClaimSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    insurance_name = serializers.CharField(source='insurance_provider.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ConsultationInsuranceClaim
        fields = '__all__'
        read_only_fields = ['id', 'claim_number', 'created_at', 'updated_at']


class PharmacyInsuranceClaimSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    insurance_name = serializers.CharField(source='insurance_provider.name', read_only=True)

    class Meta:
        model = PharmacyInsuranceClaim
        fields = '__all__'
        read_only_fields = ['id', 'claim_number', 'created_at', 'updated_at']


class InpatientInsuranceClaimSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    insurance_name = serializers.CharField(source='insurance_provider.name', read_only=True)

    class Meta:
        model = InpatientInsuranceClaim
        fields = '__all__'
        read_only_fields = ['id', 'claim_number', 'created_at', 'updated_at']

    def get_patient_name(self, obj):
        return str(obj.admission.patient)


# ============================================================
# SHA
# ============================================================

class SHAMemberSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    available_balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = SHAMember
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SHAClaimSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    sha_number = serializers.CharField(source='sha_member.sha_number', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = SHAClaim
        fields = '__all__'
        read_only_fields = ['id', 'claim_number', 'created_at', 'updated_at']

    def get_patient_name(self, obj):
        return str(obj.sha_member.patient)


# ============================================================
# PAYMENT & BILLING
# ============================================================

class PaymentAuditLogSerializer(serializers.ModelSerializer):
    processed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = PaymentAuditLog
        fields = '__all__'
        read_only_fields = ['id', 'transaction_id', 'created_at']

    def get_processed_by_name(self, obj):
        return obj.processed_by.get_full_name() if obj.processed_by else None


class CashierSessionSerializer(serializers.ModelSerializer):
    cashier_name = serializers.CharField(source='cashier.get_full_name', read_only=True)

    class Meta:
        model = CashierSession
        fields = '__all__'
        read_only_fields = ['id', 'session_id', 'opened_at']


class MPesaDuplicateCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPesaDuplicateCheck
        fields = '__all__'
        read_only_fields = ['id', 'used_at']


# ============================================================
# eTIMS
# ============================================================

class eTIMSConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = eTIMSConfiguration
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'api_key': {'write_only': True},
        }


class eTIMSInvoiceItemSerializer(serializers.ModelSerializer):
    tax_type_display = serializers.CharField(source='get_tax_type_display', read_only=True)

    class Meta:
        model = eTIMSInvoiceItem
        fields = '__all__'
        read_only_fields = ['id', 'taxable_amount', 'tax_amount', 'total_amount', 'created_at']


class eTIMSInvoiceSerializer(serializers.ModelSerializer):
    items = eTIMSInvoiceItemSerializer(many=True, read_only=True)
    invoice_type_display = serializers.CharField(source='get_invoice_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = eTIMSInvoice
        fields = '__all__'
        read_only_fields = ['id', 'invoice_number', 'created_at', 'updated_at']


class eTIMSInvoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = eTIMSInvoice
        fields = ['id', 'invoice_number', 'invoice_type', 'customer_name',
                  'total_amount', 'payment_status', 'status', 'invoice_date']


# ============================================================
# HR — ATTENDANCE & LEAVE
# ============================================================

class HospitalWiFiNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalWiFiNetwork
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AttendanceQRCodeSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceQRCode
        fields = '__all__'
        read_only_fields = ['id', 'qr_code', 'scan_count', 'created_at']

    def get_is_valid(self, obj):
        return obj.is_valid()


class AttendanceSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_type = serializers.CharField(source='user.user_type', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['id', 'total_hours', 'created_at', 'updated_at']


class AttendanceListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'user', 'user_name', 'date', 'status',
                  'check_in_time', 'check_out_time', 'total_hours']


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class LeaveApplicationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = LeaveApplication
        fields = '__all__'
        read_only_fields = ['id', 'application_number', 'total_days', 'created_at', 'updated_at']

    def validate(self, attrs):
        if attrs.get('start_date') and attrs.get('end_date'):
            if attrs['end_date'] < attrs['start_date']:
                raise serializers.ValidationError({'end_date': 'End date must be after start date.'})
        return attrs


class LeaveApplicationListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)

    class Meta:
        model = LeaveApplication
        fields = ['id', 'application_number', 'user', 'user_name',
                  'leave_type', 'leave_type_name', 'start_date', 'end_date',
                  'total_days', 'status', 'created_at']


# ============================================================
# ASSETS
# ============================================================

class HospitalAssetSerializer(serializers.ModelSerializer):
    is_maintenance_overdue = serializers.BooleanField(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = HospitalAsset
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_assigned_to_name(self, obj):
        return obj.assigned_to.get_full_name() if obj.assigned_to else None


class HospitalAssetListSerializer(serializers.ModelSerializer):
    is_maintenance_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = HospitalAsset
        fields = ['id', 'asset_id', 'asset_name', 'category', 'location',
                  'status', 'condition', 'is_maintenance_overdue',
                  'next_maintenance_date', 'needs_replacement']


class AssetMaintenanceLogSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.asset_name', read_only=True)
    asset_id_code = serializers.CharField(source='asset.asset_id', read_only=True)
    maintenance_type_display = serializers.CharField(source='get_maintenance_type_display', read_only=True)

    class Meta:
        model = AssetMaintenanceLog
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


# ============================================================
# AUDIT, SECURITY & NOTIFICATIONS
# ============================================================

class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']

    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else 'System'


class SecurityThreatSerializer(serializers.ModelSerializer):
    threat_type_display = serializers.CharField(source='get_threat_type_display', read_only=True)
    resolved_by_name = serializers.SerializerMethodField()

    class Meta:
        model = SecurityThreat
        fields = '__all__'
        read_only_fields = ['id', 'detected_at']

    def get_resolved_by_name(self, obj):
        return obj.resolved_by.get_full_name() if obj.resolved_by else None


class NotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participant1_name = serializers.CharField(source='participant1.get_full_name', read_only=True)
    participant2_name = serializers.CharField(source='participant2.get_full_name', read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last = obj.messages.last()
        return MessageSerializer(last).data if last else None


class ConversationListSerializer(serializers.ModelSerializer):
    participant1_name = serializers.CharField(source='participant1.get_full_name', read_only=True)
    participant2_name = serializers.CharField(source='participant2.get_full_name', read_only=True)
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participant1', 'participant1_name',
                  'participant2', 'participant2_name',
                  'patient', 'unread_count', 'updated_at']

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0