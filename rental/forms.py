from django import forms
from .models import Rental_Listing

class RentalListingForm(forms.ModelForm):
    class Meta:
        model = Rental_Listing
        # These are the ONLY fields the user will be asked to fill in.
        fields = ['image', 'price', 'condition', 'contact']