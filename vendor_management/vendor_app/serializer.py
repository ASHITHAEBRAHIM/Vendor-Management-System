from .models import Vendor
from .models import VendorPerformance
from .models import PurchaseOrder
from rest_framework import serializers
from django.contrib.auth import get_user_model

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'on_time_delivery_rate',
            'quality_rating_avg',
            'average_response_time',
            'fulfilment_rate',
        ]
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    def create(self,validated_data):
        user = get_user_model().objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model = get_user_model()
        fields = ('username','password')