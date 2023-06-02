from django.shortcuts import render, redirect
from .models import Rental_Listing
from django.contrib.auth.decorators import login_required

@login_required
def all_listings(request):
    listings = Rental_Listing.objects.all().filter(college=request.user.university)
    context = {
        "products": listings
    }
    return render(request, "rental/all_products.html", context)


@login_required
def product(request, id):
    listing = Rental_Listing.objects.get(id=id)
    context = {
        "product": listing
    }
    return render(request, "rental/product.html", context)


@login_required
def search(request):
    if request.method == "POST":
        query = request.POST.get("search")
        listings = Rental_Listing.objects.filter(name__icontains=query)
        context = {
            "listings": listings
        }
        return render(request, "search.html", context)
    else:
        return render(request, "search.html")
    

@login_required
def category(request, category):
    listings = Rental_Listing.objects.filter(category=category).filter(college=request.user.university)
    context = {
        "products": listings
    }
    return render(request, "rental/all_products.html", context)

@login_required
def college(request, college):
    listings = Rental_Listing.objects.filter(college=college)
    context = {
        "listings": listings
    }
    return render(request, "college.html", context)


@login_required
def condition(request, condition):
    listings = Rental_Listing.objects.filter(condition=condition).filter(college=request.user.university)
    context = {
        "products": listings
    }
    return render(request, "rental/product.html", context)   


@login_required
def add_listing(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")
        category = request.POST.get("category")
        condition = request.POST.get("condition")
        contact = request.POST.get("contact")
        college = request.user.university
        listing = Rental_Listing.objects.create(name=name, description=description, price=price, image=image, category=category, condition=condition, contact=contact, college=college, user=request.user)
        listing.save()
        return render(request, "rental/product.html", {"product": listing})
    else:
        return render(request, "rental/new_listing.html")
    

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