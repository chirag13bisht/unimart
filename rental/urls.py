from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_listings, name="rental_home"),
    path("product/<int:id>", views.product, name="rental_product"),
    path("search", views.search, name="rental_search"),
    path("category/<str:category>", views.category, name="rental_category"),
    path("college/<str:college>", views.college, name="rental_college"),
    path("condition/<str:condition>", views.condition, name="rental_condition"),
    path("create_product", views.add_listing, name="rental_add_listing"),
    # path("add_listing_submit", views.add_listing_submit, name="rental_add_listing_submit"),
    path("edit_listing/<int:id>", views.edit_listing, name="rental_edit_listing"),
    path("rented_product/<int:id>", views.rented_product, name="rental_rented_product"),
    # path("edit_listing_submit/<int:id>", views.edit_listing_submit, name="rental_edit_listing_submit"),
    # path("delete_listing/<int:id>", views.delete_listing, name="rental_delete_listing"),
    # path("delete_listing_submit/<int:id>", views.delete_listing_submit, name="rental_delete_listing_submit"),

]