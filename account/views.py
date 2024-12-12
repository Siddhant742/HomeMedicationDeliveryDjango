from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserIdentityVerificationSerializer
)

def create_response(success=True, data=None, message=None, errors=None, status_code=status.HTTP_200_OK):
    """
    Create a standardized JSON response
    """
    response_data = {
        'success': success,
        'data': data or {},
        'message': message or '',
        'errors': errors or {}
    }
    return Response(response_data, status=status_code)

class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def list(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        
        refresh = RefreshToken.for_user(user)
        
        return create_response(
            data={
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'verification_status': user.verification_status
            },
            message='User profile retrieved successfully',
            status_code=status.HTTP_200_OK
        )

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['PUT'], serializer_class=UserIdentityVerificationSerializer)
    def upload_identity_docs(self, request):
        try:
            user = request.user
            serializer = self.get_serializer(user, data=request.data)

            if serializer.is_valid():
                user.front_id_image = serializer.validated_data.get('front_id_image')
                user.back_id_image = serializer.validated_data.get('back_id_image')
                user.verification_status = 'pending'
                user.save()

                return create_response(
                    data={'verification_status': 'pending'},
                    message='Identity documents uploaded successfully. Awaiting verification.',
                    status_code=status.HTTP_200_OK
                )

            return create_response(
                success=False,
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return create_response(
                success=False,
                errors={'detail': str(e)},
                message='An unexpected error occurred during document upload.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['GET'])
    def verification_status(self, request):
        user = request.user
        return create_response(
            data={'verification_status': user.verification_status},
            status_code=status.HTTP_200_OK
        )

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                
                return create_response(
                    data={
                        'tokens': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token)
                        },
                        'user': {
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name
                        }
                    },
                    message='User registered successfully.',
                    status_code=status.HTTP_201_CREATED
                )
            
            except Exception as e:
                return create_response(
                    success=False,
                    errors={'detail': str(e)},
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        
        return create_response(
            success=False,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            
            return create_response(
                data={
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    },
                    'user': {
                        'user_id'   : user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'verification_status': user.verification_status
                    }
                },
                message='Login successful',
                status_code=status.HTTP_200_OK
            )
        
        return create_response(
            success=False,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )