from django.db import models
from users.models import User
from mart.models import Listing
from rental.models import Rental_Listing
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class UserEvent(models.Model):
    EVENT_CHOICES = (
        ('view', 'View'),
        ('inquire', 'Inquire'), # This is our key event
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=10, choices=EVENT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    # --- Generic Relation ---
    # This allows us to point to EITHER a Listing OR a Rental_Listing
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user} - {self.event_type} - {self.content_object}"