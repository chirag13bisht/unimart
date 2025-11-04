from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Listing
from django.contrib.auth.decorators import login_required

# --- NEW IMPORTS ---
from .forms import ListingForm  # Import the new form
from .tasks import process_product_image # Import the Celery task

from recommender.models import UserEvent
from django.contrib.contenttypes.models import ContentType

@login_required
def all_products(request):
    products = Listing.objects.all().filter(status="active").filter(college=request.user.university)
    # products = Listing.objects.all().filter(status="Active")
    return render(request, "all_products.html", {"products": products})
    # return JsonResponse({"products": products})

@login_required
def product_detail(request, product_id):
    product = Listing.objects.get(id=product_id)

    # --- START NEW CODE ---
    # Log the "view" event for the recommender system
    UserEvent.objects.create(
        user=request.user,
        event_type='view',
        content_object=product  # This links to the Listing object
    )
    # --- END NEW CODE ---

    return render(request, "product.html", {"product": product})
    # return JsonResponse({"product": product})


@login_required
def search(request):
    query = request.GET.get('query')
    products = Listing.objects.all().filter(name__icontains=query).filter(status="active").filter(college=request.user.university)
    return render(request, "all_products.html", {"products": products})
    # return JsonResponse({"products": products})


@login_required
def category(request, category):
    products = Listing.objects.all().filter(category=category).filter(status="active").filter(college=request.user.university)
    return render(request, "all_products.html", {"products": products})
    # return JsonResponse({"products": products})


@login_required
def condition(request, condition):
    # --- BUG FIX ---
    # Changed request.user.college to request.user.university to match your other views
    products = Listing.objects.all().filter(condition=condition).filter(status="active").filter(college=request.user.university)
    # return render(request, "all_products.html", {"products": products})
    return JsonResponse({"products": products})


@login_required
def college(request, college):
    products = Listing.objects.all().filter(college=college).filter(status="active")
    # return render(request, "all_products.html", {"products": products})
    return JsonResponse({"products": products})


@login_required
def my_products(request):
    products = Listing.objects.all().filter(user=request.user)
    # return render(request, "my_products.html", {"products": products})
    return JsonResponse({"products": products})


@login_required
def sold_products(request):
    products = Listing.objects.all().filter(user=request.user).filter(status="sold")
    # return render(request, "sold_products.html", {"products": products})
    return JsonResponse({"products": products})

def expired_products(request):
    products = Listing.objects.all().filter(user=request.user).filter(status="expired")
    # return render(request, "expired_products.html", {"products": products})
    return JsonResponse({"products": products})


# --- THIS VIEW IS COMPLETELY UPDATED ---
@login_required
def create_product(request):
    if request.method == "POST":
        # 1. Use the new ListingForm
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            # 2. Save the form but don't commit to DB yet
            product = form.save(commit=False)
            
            # 3. Add the data the form didn't have
            product.user = request.user
            product.college = request.user.university
            # The status will be 'processing' by default from your model
            
            # 4. Now save to get an ID
            product.save()
            
            # 5. --- CALL THE AI TASK ---
            # Send the new product's ID to your Celery worker
            process_product_image.delay(product.id)
            
            # 6. Redirect to the profile/my_products page
            # The user can watch for the product to appear
            return redirect("profile") # 'profile' is used in your mark_as_sold view
    else:
        # For a GET request, just show the blank form
        form = ListingForm()
        
    return render(request, "new_listing.html", {"form": form})


@login_required
def edit_product(request, product_id):
    product = Listing.objects.get(id=product_id)
    if request.method == "POST":
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.category = request.POST.get('category')
        product.condition = request.POST.get('condition')
        product.save()
        return render(request, "product.html", {"product": product})
    else:
        product=Listing.objects.get(id=product_id)
        if product.user == request.user:
            return render(request, "edit_listing.html", {"product": product})
        else:
            return redirect("all_products")

@login_required
def delete_product(request, product_id):
    product = Listing.objects.get(id=product_id)
    product.delete()
    products = Listing.objects.all().filter(user=request.user)
    return render(request, "my_products.html", {"products": products})

@login_required
def sold_product(request, product_id):
    product = Listing.objects.get(id=product_id)
    product.status = "Sold"
    product.save()
    products = Listing.objects.all().filter(user=request.user)
    return render(request, "my_products.html", {"products": products})


@login_required
def expired_product(request, product_id):
    product = Listing.objects.get(id=product_id)
    product.status = "Expired"
    product.save()
    products = Listing.objects.all().filter(user=request.user)
    return render(request, "my_products.html", {"products": products})


@login_required
def active_product(request, product_id):
    product = Listing.objects.get(id=product_id)
    product.status = "Active"
    product.save()
    products = Listing.objects.all().filter(user=request.user)
    return render(request, "my_products.html", {"products": products})


@login_required
def mark_as_sold(request, product_id):
    product = Listing.objects.get(id=product_id)
    if product.user != request.user:
        return redirect("all_products")
    product.status="Sold"
    product.save()
    return redirect("profile")