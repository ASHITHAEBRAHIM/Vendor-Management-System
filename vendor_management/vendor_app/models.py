from django.db import models
from django.utils import timezone
from django.db.models import Sum, Avg, Count
from django.db.models import F, ExpressionWrapper, fields

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=125)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20,unique=True)

    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time =models.FloatField()
    fulfilment_rate = models.FloatField()

    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now())
            self.on_time_delivery_rate = (on_time_deliveries.count() / total_completed_pos) * 100
        else:
            self.on_time_delivery_rate = 0.0

    def calculate_quality_rating_avg(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        quality_ratings = completed_pos.aggregate(models.Avg('quality_rating'))['quality_rating__avg']
        self.quality_rating_avg = quality_ratings or 0.0

    def calculate_average_response_time(self):
        acknowledged_pos = self.purchaseorder_set.exclude(acknowledgement_date__isnull=True)
        response_times = acknowledged_pos.annotate(response_time=ExpressionWrapper(F('acknowledgement_date') - F('issue_date'),output_field=fields.DurationField())).aggregate(Avg('response_time'))['response_time__avg']
        self.average_response_time = response_times.total_seconds() / 3600 if response_times else 0.0

    def calculate_fulfilment_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        total_pos = self.purchaseorder_set.count()

        if total_pos > 0:
            successful_fulfillments = completed_pos.filter(quality_rating__isnull=True)
            self.fulfilment_rate = (successful_fulfillments.count() / total_pos) * 100
        else:
            self.fulfilment_rate = 0.0
    def calculate_metrics(self):
        self.calculate_on_time_delivery_rate()
        self.calculate_quality_rating_avg()
        self.calculate_average_response_time()
        self.calculate_fulfilment_rate()
        self.save()

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True,blank=True)
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.po_number

class VendorPerformance(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_average = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.date}"
