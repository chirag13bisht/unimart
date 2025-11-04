from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from mart.models import Listing
from rental.models import Rental_Listing
from .models import UserEvent

@login_required
def log_inquiry(request, model_type, product_id):
    try:
        # Find which model (mart or rental) we're logging
        if model_type == 'mart':
            product_model = ContentType.objects.get_for_model(Listing)
            product = Listing.objects.get(id=product_id)
        elif model_type == 'rental':
            product_model = ContentType.objects.get_for_model(Rental_Listing)
            product = Rental_Listing.objects.get(id=product_id)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid model type'}, status=400)

        # Create the "inquire" event
        UserEvent.objects.create(
            user=request.user,
            event_type='inquire',
            content_type=product_model,
            object_id=product.id
        )

        # Send back the contact info
        return JsonResponse({'status': 'success', 'contact': product.contact})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)