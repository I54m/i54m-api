from django.utils.crypto import get_random_string
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random, string

API_KEY_LENGTH = 64
APP_ID_PREFIX_LENGTH = 8

def generate_random_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class ApiUser(AbstractUser):
    pass

class ApiKey(models.Model):
    
    api_user = models.ForeignKey(ApiUser, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now, null=False, editable=False)
    last_accessed = models.DateTimeField(null=True)
    last_accessed_ip = models.GenericIPAddressField(null=True)

    app_id = models.CharField(max_length=128, blank=True, null=False)
    app_description = models.TextField(max_length=1024, blank=True, null=True)
    api_secret = models.CharField(max_length=255, editable=False, unique=True, blank=True, null=True)

    def has_valid_api_secret(self, secret_key: str) -> bool:
        return self.api_secret is secret_key

    def __str__(self) -> str:
        return self.app_id
    
@receiver(post_save, sender=ApiKey)
def post_save_hook(instance: ApiKey, created, *args, **kwargs):
    if created:
        instance.api_secret =  get_random_string(API_KEY_LENGTH)
        instance.created = timezone.now()
        instance.save()




