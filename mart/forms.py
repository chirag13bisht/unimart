from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        # These are the ONLY fields the user will be asked to fill in.
        # The AI will handle the rest.
        fields = ['image', 'price', 'condition', 'contact']