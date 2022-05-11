from django.db import models
from core.models import BaseModel
# Create your models here.

class Book(BaseModel):
    author = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    date_of_publication = models.DateField()
    is_in_library = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.author}"


class BookTracking(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.username}"