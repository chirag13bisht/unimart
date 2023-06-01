from django.shortcuts import render
from django.http import JsonResponse
from .models import Listing

# Create your views here.
def all_products(request):
    products = Listing.objects.all().filter(status="Active").filter(college=request.user.college)
    return render(request, "all_products.html", {"products": products})
    # return JsonResponse({"products": products})


def product_detail(request, product_id):
    product = Listing.objects.get(id=product_id)
    # return render(request, "product_detail.html", {"product": product})
    return JsonResponse({"product": product})

def search(request):
    query = request.GET.get('query')
    products = Listing.objects.all().filter(name__icontains=query).filter(status="Active").filter(college=request.user.college)
    # return render(request, "all_products.html", {"products": products})
    return JsonResponse({"products": products})

def category(request, category):
    products = Listing.objects.all().filter(category=category).filter(status="Active").filter(college=request.user.college)
    # return render(request, "all_products.html", {"products": products})
    return JsonResponse({"products": products})

def condition(request, condition):
    products = Listing.objects.all().filter(condition=condition).filter(status="Active").filter(college=request.user.college)
    # return render(request, "all_products.html", {"products": products})
    return JsonResponse({"products": products})

def college(request, college):
    products = Listing.objects.all().filter(college=college).filter(status="Active")
    # return render(request, "all_products.html", {"products": products})
    return JsonResponse({"products": products})

def my_products(request):
    products = Listing.objects.all().filter(user=request.user)
    # return render(request, "my_products.html", {"products": products})
    return JsonResponse({"products": products})

def sold_products(request):
    products = Listing.objects.all().filter(user=request.user).filter(status="Sold")
    # return render(request, "sold_products.html", {"products": products})
    return JsonResponse({"products": products})

def expired_products(request):
    products = Listing.objects.all().filter(user=request.user).filter(status="Expired")
    # return render(request, "expired_products.html", {"products": products})
    return JsonResponse({"products": products})

def create_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        condition = request.POST.get('condition')
        college = request.POST.get('college')
        product = Listing(name=name, description=description, price=price, image=image, category=category, condition=condition, college=college, user=request.user)
        product.save()
        return render(request, "product_detail.html", {"product": product})
    else:
        return render(request, "create_product.html")

def edit_product(request, product_id):
    product = Listing.objects.get(id=product_id)
    if request.method == "POST":
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.image = request.FILES.get('image')
        product.category = request.POST.get('category')
        product.condition = request.POST.get('condition')
        product.college = request.POST.get('college')
        product.save()
        return render(request, "product_detail.html", {"product": product})
    else:
        return render(request, "edit_product.html", {"product": product})
    
def delete_product(request, product_id):
    product = Listing.objects.get(id=product_id)
    product.delete()
    products = Listing.objects.all().filter(user=request.user)
    return render(request, "my_products.html", {"products": products})

def sold_product(request, product_id):
    product = Listing.objects.get(id=product_id)
    product.status = "Sold"
    product.save()
    products = Listing.objects.all().filter(user=request.user)
    return render(request, "my_products.html", {"products": products})

def expired_product(request, product_id):
    product = Listing.objects.get(id=product_id)
    product.status = "Expired"
    product.save()
    products = Listing.objects.all().filter(user=request.user)
    return render(request, "my_products.html", {"products": products})

def active_product(request, product_id):
    product = Listing.objects.get(id=product_id)
    product.status = "Active"
    product.save()
    products = Listing.objects.all().filter(user=request.user)
    return render(request, "my_products.html", {"products": products})