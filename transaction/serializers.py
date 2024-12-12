from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Prescription, Order
from django.core.validators import MinValueValidator, MaxValueValidator


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id', 'prescription_image', 'status', 'verified_at', 'created_at']
        read_only_fields = ['status', 'id', 'verified_at', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    prescription = PrescriptionSerializer(read_only=True)
    prescription_image = serializers.ImageField(write_only=True)
    payment_slip = serializers.ImageField(required=True)
    delivery_address = serializers.CharField(required=True)
    medicines = serializers.CharField(required=True)  # New field for medicines
    duration = serializers.CharField(required=True)  # New field for duration
    latitude = serializers.FloatField(
        required=True,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)]
    )
    longitude = serializers.FloatField(
        required=True,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)]
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'prescription', 'prescription_image', 'status', 'delivery_address',
                 'payment_slip', 'latitude', 'longitude', 'medicines', 'duration',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        if data['latitude'] < -90.0 or data['latitude'] > 90.0:
            raise serializers.ValidationError({'latitude': 'Latitude must be between -90 and 90 degrees.'})
        if data['longitude'] < -180.0 or data['longitude'] > 180.0:
            raise serializers.ValidationError({'longitude': 'Longitude must be between -180 and 180 degrees.'})
        return data

    def validate_payment_slip(self, value):
        max_file_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_file_size:
            raise serializers.ValidationError("Payment slip file size must be under 10MB.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        prescription_image = validated_data.pop('prescription_image')
        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')
        
        prescription = Prescription.objects.create(user=user, prescription_image=prescription_image)
        order = Order.objects.create(
            prescription=prescription, 
            user=user,
            latitude=latitude, 
            longitude=longitude, 
            **validated_data
        )
        return order









# from rest_framework import serializers
# from .models import Prescription, Order
# from django.core.validators import MinValueValidator, MaxValueValidator

# class PrescriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Prescription
#         fields = ['id', 'prescription_image', 'status', 'verified_at', 'created_at']
#         read_only_fields = ['status', 'id', 'verified_at', 'created_at']

# class OrderSerializer(serializers.ModelSerializer):
#     prescription = PrescriptionSerializer(read_only=True)
#     prescription_image = serializers.ImageField(write_only=True)
#     payment_slip = serializers.ImageField(required=True)
#     delivery_address = serializers.CharField(required=True)
#     latitude = serializers.FloatField(
#         required=True,
#         validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)]
#     )
#     longitude = serializers.FloatField(
#         required=True,
#         validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)]
#     )
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

#     class Meta:
#         model = Order
#         fields = ['id', 'prescription', 'prescription_image', 'status', 'delivery_address',
#                  'payment_slip', 'latitude', 'longitude', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'created_at', 'updated_at']

#     def validate(self, data):
#         if data['latitude'] < -90.0 or data['latitude'] > 90.0:
#             raise serializers.ValidationError({'latitude': 'Latitude must be between -90 and 90 degrees.'})
#         if data['longitude'] < -180.0 or data['longitude'] > 180.0:
#             raise serializers.ValidationError({'longitude': 'Longitude must be between -180 and 180 degrees.'})
#         return data

#     def validate_payment_slip(self, value):
#         max_file_size = 10 * 1024 * 1024  # 10MB
#         if value.size > max_file_size:
#             raise serializers.ValidationError("Payment slip file size must be under 10MB.")
#         return value

#     def create(self, validated_data):
#         user = self.context['request'].user
#         prescription_image = validated_data.pop('prescription_image')
#         latitude = validated_data.pop('latitude')
#         longitude = validated_data.pop('longitude')
#         prescription = Prescription.objects.create(user=user, prescription_image=prescription_image)
#         order = Order.objects.create(prescription=prescription, user=user,
#                                     latitude=latitude, longitude=longitude, **validated_data)
#         return order
