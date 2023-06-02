from django.db import models
from users.models import User
# Create your models here.
class Rental_Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.CharField(max_length=64)
    image = models.ImageField(upload_to='listings/', blank=True)
    category = models.CharField(max_length=64, blank=True, choices=[
        ("Accessories", "Accessories"),
        ("Electronics", "Electronics"),
        ("Stationery", "Stationery"),
        ("Others", "Others")])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rental")
    date = models.DateTimeField(auto_now_add=True)
    college = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=64, default="Active", blank=True, choices=[("Active", "Active"), ("Rented", "Rented"), ("Expired", "Expired")])
    condition = models.CharField(max_length=64, default="New", blank=True, choices=[
        ("New", "New"),
        ("Almost New", "Almost New"),
        ("Used", "Used"),
        ("Very Used", "Very Used"),
        ("Okayish", "Okayish")])
    contact = models.BigIntegerField()

    def __str__(self):
        return f"{self.name}"