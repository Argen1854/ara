from django.forms import ValidationError
from rest_framework import serializers
from user.models import User
from business_accounts.models import SalonReview, Staff, SalonService, Records, BusinessAccount, StaffReview, StaffTimetable



class SalonReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalonReview
        fields = "__all__"


class StaffReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffReview
        fields = "__all__"

class StaffTimetableSerializers(serializers.ModelSerializer):
    class Meta:
        model = StaffTimetable
        fields = "__all__"

class BusinessAccountStaffSerializers(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"


class BusinessAccountServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = SalonService
        fields = "__all__"

class StaffSerializers(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"


class BusinessAccountAPIViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = BusinessAccount
        fields = 'id admin title start_time end_time address phone_number email avatar'.split()

class ListUserRecordsAPIViewSerializers(serializers.ModelSerializer):
    businessaccount = BusinessAccountAPIViewSerializers()
    class Meta:
        model = Records
        fields = 'businessaccount id id data time price promo_code status discount staff_info'.split()

class RecordsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = 'id data time price promo_code status salon staff_info service_info discount'.split()


class CreateRecordsAPIViewSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    data = serializers.DateField()
    time = serializers.TimeField()
    staff_id = serializers.IntegerField()
    service_id = serializers.IntegerField()

    def validate_user_id(self, id):
        try:
            User.objects.get(id=id)
        except:
            raise ValidationError(f'ID Error')
        return id
    
    def validate_staff_id(self, id):
        try:
            Staff.objects.get(id=id)
        except:
            raise ValidationError(f'ID Error')
        return id

    def validate_service_id(self, id):
        try:
            SalonService.objects.get(id=id)
        except:
            raise ValidationError(f'ID Error')
        return id


class SraffAPIViewSerializer(serializers.Serializer):
    data = serializers.DateField()
        