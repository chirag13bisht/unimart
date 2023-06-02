from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Listing
from django.contrib.auth.decorators import login_required

@login_required
def all_products(request):
    products = Listing.objects.all().filter(status="Active").filter(college=request.user.university)
    # products = Listing.objects.all().filter(status="Active")
    return render(request, "all_products.html", {"products": products})
    # return JsonResponse({"products": products})

@login_required
def product_detail(request, product_id):
    product = Listing.objects.get(id=product_id)
    return render(request, "product.html", {"product": product})
    # return JsonResponse({"product": product})


@login_required
def search(request):
    query = request.GET.get('query')
    products = Listing.objects.all().filter(name__icontains=query).filter(status="Active").filter(college=request.user.university)
    return render(request, "all_products.html", {"products": products})
    # return JsonResponse({"products": products})


@login_required
def category(request, category):
    products = Listing.objects.all().filter(category=category).filter(status="Active").filter(college=request.user.university)
    return render(request, "all_products.html", {"products": products})
    # return JsonResponse({"products": products})


@login_required
def condition(request, condition):
    products = Listing.objects.all().filter(condition=condition).filter(status="Active").filter(college=request.user.college)
    # return render(request, "all_products.html", {"products": products})
    return JsonResponse({"products": products})


@login_required
def college(request, college):
    products = Listing.objects.all().filter(college=college).filter(status="Active")
    # return render(request, "all_products.html", {"products": products})
    return JsonResponse({"products": products})


@login_required
def my_products(request):
    products = Listing.objects.all().filter(user=request.user)
    # return render(request, "my_products.html", {"products": products})
    return JsonResponse({"products": products})


@login_required
def sold_products(request):
    products = Listing.objects.all().filter(user=request.user).filter(status="Sold")
    # return render(request, "sold_products.html", {"products": products})
    return JsonResponse({"products": products})

def expired_products(request):
    products = Listing.objects.all().filter(user=request.user).filter(status="Expired")
    # return render(request, "expired_products.html", {"products": products})
    return JsonResponse({"products": products})


@login_required
def create_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        condition = request.POST.get('condition')
        college = request.user.university
        contact = request.POST.get('contact')
        product = Listing(name=name, description=description, price=price, image=image, category=category, condition=condition, college=college, user=request.user, contact=contact)
        product.save()
        return render(request, "product.html", {"product": product})
    else:
        return render(request, "new_listing.html")


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