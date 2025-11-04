from django.db import models
from users.models import User

# Create your models here.
class Rental_Listing(models.Model):
    
    # --- STATUS CHOICES (Updated) ---
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('Active', 'Active'),
        ('Rented', 'Rented'),
        ('Expired', 'Expired')
    )
    
    # --- CATEGORY CHOICES (Updated) ---
    CATEGORY_CHOICES = [
        ("Accessories", "Accessories"),
        ("Electronics", "Electronics"),
        ("Stationery", "Stationery"),
        ("Books", "Books"), # Added Books
        ("Others", "Others")
    ]
    
    # --- MODEL FIELDS (Updated) ---
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=64) # This is a CharField, which is fine for "per day", etc.
    image = models.ImageField(upload_to='listings/', blank=True)
    category = models.CharField(max_length=64, null=True, blank=True, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rental")
    date = models.DateTimeField(auto_now_add=True)
    college = models.CharField(max_length=64, blank=True)
    
    # Status field is now 'processing' by default
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processing')
    
    condition = models.CharField(max_length=64, default="New", blank=True, choices=[
        ("New", "New"),
        ("Almost New", "Almost New"),
        ("Used", "Used"),
        ("Very Used", "Very Used"),
        ("Okayish", "Okayish")])
    contact = models.BigIntegerField()

    def __str__(self):
        # Handle cases where the name might be empty during processing
        if self.name:
            return f"{self.name}"
        return f"Processing Rental {self.id}"