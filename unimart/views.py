from django.shortcuts import render
from users.models import waitlist
from django.http import HttpResponse
from mart.models import Listing
from rental.models import Rental_Listing
from django.contrib.auth.decorators import login_required
from community.models import SuggestedStudyGroup

# --- Import the recommender service ---
from recommender.service import get_recommendations_for_user, parse_and_fetch_items

# --- 1. REVERTED HOME VIEW ---
# This is back to its original, simple state.
def home(request):
    return render(request, "home.html")

# --- 2. NEW RECOMMENDATIONS VIEW ---
@login_required
def recommendations_page(request):
    context = {} 
    
    try:
        # 1. Get the list of recommended item IDs
        recommended_ids = get_recommendations_for_user(request.user.id, num_recs=10)
        
        # 2. Fetch the actual product/rental objects
        recommended_items = parse_and_fetch_items(recommended_ids)
        
        # 3. Tag each item with its type so the template can make links
        for item in recommended_items:
            if isinstance(item, Listing):
                item.model_type = 'mart'
            elif isinstance(item, Rental_Listing):
                item.model_type = 'rental'

        # 4. Add the items to the context
        context['recommended_items'] = recommended_items
        
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        context['recommended_items'] = []
            
    # 5. Render the new template
    return render(request, "recommendations.html", context)
# ---------------------------------

def waitlist_v(request):
    try:
        if request.user.waitlist:
            return HttpResponse("You have already submitted the waitlist")
    except:
        return render(request, "waitlist.html")

def waitlist_submit(request):
    if request.method == "POST":
        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        roll_number = request.POST.get('roll_number')
        image = request.FILES.get('id_card')
        university = request.POST.get('university')
        waitlist_obj = waitlist.objects.create(user=user, name=name, email=email, enrollment_number=roll_number, id_card=image, university=university)
        waitlist_obj.save()
        return HttpResponse("Waitlist submitted successfully")
    
def about(request):
    return render(request, "about.html")


@login_required
def profile(request):
    all_products = Listing.objects.filter(user=request.user).filter(status="Active")
    all_rentals = Rental_Listing.objects.filter(user=request.user).filter(status="Active")
    study_groups = SuggestedStudyGroup.objects.filter(members=request.user)
    context = {
        'products': all_products, 
        'rentals': all_rentals,
        'study_groups': study_groups  # <-- ADD THIS
    }
    return render(request, "profile.html", context)
