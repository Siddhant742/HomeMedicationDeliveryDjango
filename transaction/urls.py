from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrescriptionViewSet, OrderViewSet
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'prescription', PrescriptionViewSet, basename='prescription')
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)