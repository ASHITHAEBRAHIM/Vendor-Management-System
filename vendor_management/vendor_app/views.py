from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import Vendor
from .serializer import VendorSerializer, UserSerializer

from .models import PurchaseOrder
from .serializer import PurchaseOrderSerializer

from .models import VendorPerformance
from .serializer import VendorPerformanceSerializer

from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import get_user_model
# Create your views here.
class VendorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=['GET'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        vendor.calculate_metrics()  # Ensure metrics are up-to-date
        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfilment_rate': vendor.fulfilment_rate,
        }
        serializer = VendorPerformanceSerializer(data=performance_data)
        serializer.is_valid()
        return Response(serializer.validated_data)

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    @action(detail=True, methods=['POST'])
    def acknowledge(self, request, pk=None):
        vendor = self.get_object()
        po_id = request.data.get('po_id')

        if po_id:
            try:
                purchase_order = PurchaseOrder.objects.get(pk=po_id)
                purchase_order.acknowledgement_date = timezone.now()
                purchase_order.save()
                vendor.calculate_metrics()
                return Response({'detail': 'Acknowledgment successful.'})
            except PurchaseOrder.DoesNotExist:
                return Response({'detail': 'Purchase Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'Missing po_id parameter.'}, status=status.HTTP_400_BAD_REQUEST)


class VendorPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'pk'

class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


