from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Prescription, Order
from .serializers import PrescriptionSerializer, OrderSerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PrescriptionSerializer
    
    def get_queryset(self):
        return Prescription.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['GET'])
    def order_status(self, request, pk=None):
        try:
            prescription = self.get_object()
            order = Order.objects.filter(prescription=prescription).first()
            
            if not order:
                return Response({
                    'message': 'No associated order found.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'order_status': order.status
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'An error occurred while fetching order status.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related('prescription').order_by('-created_at')
    
    def perform_create(self, serializer):
        prescription_image = self.request.data.get('prescription_image')
        latitude = self.request.data.get('latitude')
        longitude = self.request.data.get('longitude')
        serializer.save(prescription_image=prescription_image, latitude=latitude, longitude=longitude)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        return Response({
            'message': 'Order Created Successfully',
            'order_id': order.id
        }, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)








# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Prescription, Order
# from .serializers import PrescriptionSerializer, OrderSerializer

# class PrescriptionViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PrescriptionSerializer

#     def get_queryset(self):
#         return Prescription.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     @action(detail=True, methods=['GET'])
#     def order_status(self, request, pk=None):
#         try:
#             prescription = self.get_object()
#             order = Order.objects.filter(prescription=prescription).first()
#             if not order:
#                 return Response({
#                     'message': 'No associated order found.'
#                 }, status=status.HTTP_404_NOT_FOUND)
#             return Response({
#                 'order_status': order.status
#             }, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({
#                 'error': 'An error occurred while fetching order status.',
#                 'details': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class OrderViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user).select_related('prescription').order_by('-created_at')

#     def perform_create(self, serializer):
#         prescription_image = self.request.data.get('prescription_image')
#         latitude = self.request.data.get('latitude')
#         longitude = self.request.data.get('longitude')
#         serializer.save(prescription_image=prescription_image, latitude=latitude, longitude=longitude)
        
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

