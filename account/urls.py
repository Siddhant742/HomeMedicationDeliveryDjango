from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView, 
    UserLoginView, 
    UserProfileViewSet
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    # Basic authentication routes
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    
    # JWT token routes
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Include ViewSet routes
    path('', include(router.urls)),
]
