from django.db import models

# Create your models here.
class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='listings/', blank=True)
    category = models.CharField(max_length=64, blank=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="listings")
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=64, default="Active", blank=True, options=[("Active", "Active"), ("Sold", "Sold"), ("Expired", "Expired")])

    def __str__(self):
        return f"{self.title}"