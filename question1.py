# models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import time

class MyModel(models.Model):
    name = models.CharField(max_length=100)

# Signal handler
@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print("Signal handler started")
    time.sleep(5)  
    print("Signal handler completed")


from myapp.models import MyModel
import time

print("Creating a MyModel instance")
start_time = time.time()
my_instance = MyModel.objects.create(name="Test")
end_time = time.time()
print(f"Time taken for model save with signal handling: {end_time - start_time} seconds")

# By default, Django signals are executed synchronously. It means that when a signal is triggered, all connected signal handlers run immediately in the same thread as the request or the function that triggered the signal. This behavior can potentially slow down execution if the handlers are time-consuming, as they block the flow until completion.