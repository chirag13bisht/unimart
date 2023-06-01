from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name="all_products"),
    path('product/<int:product_id>', views.product_detail, name="product_detail"),
    path('search/', views.search, name="search"),
    path('category/<str:category>', views.category, name="category"),
    path('condition/<str:condition>', views.condition, name="condition"),
    path('college/<str:college>', views.college, name="college"),
    path('my_products/', views.my_products, name="my_products"),
    path('sold_products/', views.sold_products, name="sold_products"),
    path('expired_products/', views.expired_products, name="expired_products"),
    path('create_product/', views.create_product, name="create_product"),
    path('edit_product/<int:product_id>', views.edit_product, name="edit_product"),
    path('delete_product/<int:product_id>', views.delete_product, name="delete_product"),
    path('new_listing/', views.create_product, name="new_listing"),
    path('edit_listing/<int:product_id>', views.edit_product, name="edit_listing"),
]