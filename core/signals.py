from django.db.models.signals import pre_delete
from django.utils import timezone
from django.dispatch import receiver
from core.models import Point

@receiver(pre_delete, sender=Point)
def pre_delete_group(sender, instance, **kwargs):
    year = int(timezone.now().strftime('%Y'))
    month = int(timezone.now().strftime('%m'))
    
    if year == instance.year and month == instance.month:
        instance.head.point += instance.value
        instance.head.save()