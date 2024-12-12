from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'phone_number', 
            'is_verified', 
            'verification_status',
            'first_name',
            'last_name'
        ]
        read_only_fields = ['is_verified', 'verification_status']

class UserIdentityVerificationSerializer(serializers.ModelSerializer):
    front_id_image = serializers.ImageField(
        validators=[],  # You can add validators here if needed
        required=True
    )
    back_id_image = serializers.ImageField(
        validators=[],  # You can add validators here if needed
        required=True
    )

    class Meta:
        model = User
        fields = ['front_id_image', 'back_id_image']

    def validate(self, data):
        max_file_size = 5 * 1024 * 1024  # 5MB
        for image_field in ['front_id_image', 'back_id_image']:
            if data.get(image_field):
                if data[image_field].size > max_file_size:
                    raise serializers.ValidationError({
                        image_field: "File size must be under 5MB."
                    })
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'},
        error_messages={'required': 'Password is required.'}
    )
    password_confirm = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'username', 
            'password', 
            'password_confirm', 
            'email', 
            'first_name', 
            'last_name', 
            'phone_number'
        )
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': False}
        }

    def validate(self, data):
        # Validate password match
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        # Check if username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})
        
        # Check if email already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        
        return data

    def create(self, validated_data):
        # Create user with hashed password
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', '')
        )
        # Set password using custom method
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is deactivated.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials.")
        
        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        return user