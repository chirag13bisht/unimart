from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        # Get all unread notifications, newest first
        unread_notifications = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).order_by('-created_at')

        # Get the count
        unread_count = unread_notifications.count()

        return {
            'unread_notifications': unread_notifications,
            'unread_count': unread_count
        }

    # If user is not logged in, return empty values
    return {
        'unread_notifications': [],
        'unread_count': 0
    }