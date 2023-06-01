from django.db import models
from django.dispatch import receiver
from users.models import User
from allauth.account.signals import user_signed_up


# Create your models here.
class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='listings/', blank=True)
    category = models.CharField(max_length=64, blank=True, choices=[
        ("Books", "Books"),
        ("Electronics", "Electronics"),
        ("Stationery", "Stationery"),
        ("Others", "Others")])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    date = models.DateTimeField(auto_now_add=True)
    college = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=64, default="Active", blank=True, choices=[("Active", "Active"), ("Sold", "Sold"), ("Expired", "Expired")])
    condition = models.CharField(max_length=64, default="New", blank=True, choices=[
        ("New", "New"),
        ("Almost New", "Almost New"),
        ("Used", "Used"),
        ("Very Used", "Very Used"),
        ("Okayish", "Okayish")])

    def __str__(self):
        return f"{self.name}"
    

@receiver(user_signed_up)
def user_signed_up_signal_handler(request, user, **kwargs):
    user_email = user.email
    user_college_domain = user_email.split("@")[1].split(".")[0]
    if user_college_domain in ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']:
        user_college_domain = "Other"
    user.college = user_college_domain
    user.save()