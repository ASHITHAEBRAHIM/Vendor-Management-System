# your_app_name/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_metrics(sender, instance, **kwargs):
    if instance.status == 'completed':
        instance.vendor.calculate_metrics()
