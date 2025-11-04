from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Notification
from mart.models import Listing
from rental.models import Rental_Listing

@shared_task
def find_old_listings_nudge():
    """
    Finds all active listings older than 30 days and sends a 
    notification to the seller to "nudge" them.
    """
    print("Running daily nudge task...")
    
    # 1. Define how old an "old" listing is
    cutoff_date = timezone.now() - timedelta(days=30)
    
    # 2. Find old "mart" listings
    # We use 'status__iexact' for a case-insensitive match on "Active"
    old_mart_listings = Listing.objects.filter(
        status__iexact='active',
        date__lt=cutoff_date 
    )
    
    # 3. Find old "rental" listings
    old_rental_listings = Rental_Listing.objects.filter(
        status__iexact='Active',
        date__lt=cutoff_date
    )
    
    # 4. Create notifications for each old item
    notification_count = 0
    for item in old_mart_listings:
        # Create a notification for the item's owner
        Notification.objects.get_or_create(
            user=item.user,
            message=f"Your product '{item.name}' has been listed for over 30 days. Try lowering the price to sell it faster!"
        )
        notification_count += 1
        
    for item in old_rental_listings:
        Notification.objects.get_or_create(
            user=item.user,
            message=f"Your rental item '{item.name}' has been listed for over 30 days. Try lowering the rental price!"
        )
        notification_count += 1
        
    print(f"Daily nudge task complete. Sent {notification_count} notifications.")
    return f"Sent {notification_count} notifications."