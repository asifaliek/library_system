import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, blank=True
    )
    is_librarian = models.BooleanField(default=False)
    customer_id = models.CharField(max_length=128,blank=True,null=True)
    photo = models.FileField(blank=True,null=True)

    def __str__(self):
        return str(self.username)
