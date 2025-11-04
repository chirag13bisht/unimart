from django.db import models
from django.dispatch import receiver
from users.models import User
from allauth.account.signals import user_signed_up

# --- ADD THESE IMPORTS ---
from community.models import SuggestedStudyGroup
# -------------------------

# Create your models here.
class Listing(models.Model):
    # (Your Listing model code is here, no changes needed)
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
    )
    CATEGORY_CHOICES = [
        ("Accessories", "Accessories"),
        ("Electronics", "Electronics"),
        ("Stationery", "Stationery"),
        ("Books", "Books"),
        ("Others", "Others")
    ]
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='listings/', blank=True)
    category = models.CharField(max_length=64, null=True, blank=True, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    date = models.DateTimeField(auto_now_add=True)
    college = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processing')
    condition = models.CharField(max_length=64, default="New", blank=True, choices=[
        ("New", "New"),
        ("Almost New", "Almost New"),
        ("Used", "Used"),
        ("Very Used", "Very Used"),
        ("Okayish", "Okayish")])
    contact = models.BigIntegerField()

    def __str__(self):
        if self.name:
            return f"{self.name}"
        return f"Processing Listing {self.id}"
    

# --- THIS FUNCTION IS UPDATED ---
@receiver(user_signed_up)
def user_signed_up_signal_handler(request, user, **kwargs):
    """
    Runs right after a new user signs up.
    It will find or create a study group for them.
    """
    
    # The user object was already saved by your CustomSignupForm,
    # so user.university and user.course are already set.
    
    # We remove the old logic that set university from email,
    # as the form now handles that.
    
    if not user.university or not user.course:
        # User didn't fill out the fields, so we can't group them.
        print(f"User {user.username} signed up without course/university. Skipping group.")
        return

    university = user.university
    course = user.course

    # 1. Check if a group for this course@university already exists
    try:
        existing_group = SuggestedStudyGroup.objects.get(
            university_name=university,
            course_name=course
        )
        # If YES: Add this new user to the existing group.
        existing_group.members.add(user)
        print(f"Added user {user.username} to existing group for {course}")
    
    except SuggestedStudyGroup.DoesNotExist:
        # If NO: Find all other users with the same criteria.
        other_users = User.objects.filter(
            university=university,
            course=course
        ).exclude(id=user.id) # Exclude the new user

        # We only create a new group if this new user makes at least 2 people
        if other_users.exists():
            # Create the new group
            new_group = SuggestedStudyGroup.objects.create(
                university_name=university,
                course_name=course
            )
            # Add all matching members
            new_group.members.add(user)
            new_group.members.add(*other_users)
            print(f"Created new group for {course} with {len(other_users) + 1} members")
        else:
            # This is the first user for this course, do nothing.
             print(f"User {user.username} is the first for {course}. Waiting for more members.")