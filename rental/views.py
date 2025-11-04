from django.shortcuts import render, redirect
from .models import Rental_Listing
from django.contrib.auth.decorators import login_required

# --- NEW IMPORTS ---
from .forms import RentalListingForm
from .tasks import process_rental_image

from recommender.models import UserEvent
from django.contrib.contenttypes.models import ContentType

@login_required
def all_listings(request):
    # Added filter for status='Active' to hide processing items
    listings = Rental_Listing.objects.all().filter(college=request.user.university, status='Active')
    context = {
        "products": listings
    }
    return render(request, "rental/all_products.html", context)


@login_required
def product(request, id):
    listing = Rental_Listing.objects.get(id=id)

    # --- START NEW CODE ---
    # Log the "view" event for the recommender system
    UserEvent.objects.create(
        user=request.user,
        event_type='view',
        content_object=listing  # This links to the Rental_Listing object
    )
    # --- END NEW CODE ---

    context = {
        "product": listing
    }
    return render(request, "rental/product.html", context)


@login_required
def search(request):
    if request.method == "POST":
        query = request.POST.get("search")
        # Added filter for status='Active'
        listings = Rental_Listing.objects.filter(name__icontains=query, college=request.user.university, status='Active')
        context = {
            "listings": listings
        }
        return render(request, "search.html", context)
    else:
        return render(request, "search.html")
    

@login_required
def category(request, category):
    # Added filter for status='Active'
    listings = Rental_Listing.objects.filter(category=category, college=request.user.university, status='Active')
    context = {
        "products": listings
    }
    return render(request, "rental/all_products.html", context)

@login_required
def college(request, college):
    # Added filter for status='Active'
    listings = Rental_Listing.objects.filter(college=college, status='Active')
    context = {
        "listings": listings
    }
    return render(request, "college.html", context)


@login_required
def condition(request, condition):
    # Added filter for status='Active'
    listings = Rental_Listing.objects.filter(condition=condition, college=request.user.university, status='Active')
    context = {
        "products": listings
    }
    # Changed template to all_products.html to match other filter views
    return render(request, "rental/all_products.html", context)   


# --- THIS VIEW IS COMPLETELY UPDATED ---
@login_required
def add_listing(request):
    if request.method == "POST":
        # 1. Use the new RentalListingForm
        form = RentalListingForm(request.POST, request.FILES)
        if form.is_valid():
            # 2. Save the form but don't commit to DB yet
            listing = form.save(commit=False)
            
            # 3. Add the data the form didn't have
            listing.user = request.user
            listing.college = request.user.university
            # The status will be 'processing' by default from your model
            
            # 4. Now save to get an ID
            listing.save()
            
            # 5. --- CALL THE AI TASK ---
            # Send the new listing's ID to your Celery worker
            process_rental_image.delay(listing.id)
            
            # 6. Redirect to the profile
            return redirect("profile")
    else:
        # For a GET request, just show the blank form
        form = RentalListingForm()
        
    return render(request, "rental/new_listing.html", {"form": form})
    

@login_required
def edit_listing(request, id):
    listing = Rental_Listing.objects.get(id=id)
    if request.user == listing.user:
        if request.method == "POST":
            listing = Rental_Listing.objects.get(id=id)
            listing.name = request.POST.get("name")
            listing.description = request.POST.get("description")
            listing.price = request.POST.get("price")
            listing.category = request.POST.get("category")
            listing.condition = request.POST.get("condition")
            listing.contact = request.POST.get("contact")
            if request.FILES.get("image"):
                listing.image = request.FILES.get("image")
            listing.save()
            return render(request, "rental/product.html", {"product": listing})
        else:
            listing = Rental_Listing.objects.get(id=id)
            return render(request, "rental/edit_listing.html", {"product": listing})
    else:
        return render(request, "rental/product.html", {"product": listing})

@login_required
def rented_product(request, id):
    listing = Rental_Listing.objects.get(id=id)
    if request.user == listing.user:
        listing.status = "Rented"
        listing.save()
    return redirect("profile")