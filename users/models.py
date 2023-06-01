from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    university = models.CharField(max_length=100, null=True, blank=True)



class waitlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="waitlist")
    name = models.CharField(max_length=100, null=True, blank=True)
    enrollment_number = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    university = models.CharField(max_length=100, null=True, blank=True)
    id_card = models.ImageField(upload_to='id_card/', blank=True)
    def __str__(self):
        return f"{self.name} - {self.university}"
    
    def set_approved(self):
        self.user.college = self.university
        self.user.save()
        self.delete()
        return True

    def set_rejected(self):
        self.delete()
        return True