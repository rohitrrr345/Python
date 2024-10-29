# Yes, by default, Django signals run in the same database transaction as the caller. To demonstrate this, we can use a signal receiver to make a database change and then deliberately raise an exception in the caller after triggering the signal
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from myapp.models import MyModel, SignalTestModel

class SignalTestModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def signal_receiver(sender, instance, **kwargs):
    SignalTestModel.objects.create(name="Signal created this")

def my_view(request):
    instance = MyModel.objects.create(name="Test Instance")
    
    try:
        with transaction.atomic():
            instance.save()
            raise Exception("Triggering rollback")
    except Exception as e:
        print(f"Exception: {e}")
    
    if SignalTestModel.objects.exists():
        return HttpResponse("Signal data was saved, transaction was separate")
    else:
        return HttpResponse("Signal data rolled back, transaction was shared")
# By default, Django signals will share the transaction, so we expect the former response.






