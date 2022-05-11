import uuid
from django.db import models

class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, blank=True
    )
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        "accounts.User",
        limit_choices_to={"is_active": True},
        blank=True,
        null=True,
        related_name="creator_%(class)s_objects",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

