from django import forms
from django.forms import Form # Import the correct base class
from allauth.account.adapter import get_adapter

# We don't need the other allauth form imports

class CustomSignupForm(Form): # <-- Inherit from Form

    # --- These are the default allauth fields we must re-create ---
    username = forms.CharField(
        label="Username",
        min_length=3,
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"placeholder": "E-mail"}),
        required=True,
    )

    # --- This is YOUR university field ---
    university = forms.CharField(
        max_length=100, 
        label='University', 
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "University"}),
    )

    # --- THIS IS THE NEW FIELD ---
    course = forms.CharField(
        max_length=100, 
        label='Course', 
        required=False, # Make it optional for now
        widget=forms.TextInput(attrs={"placeholder": "Your Course (e.g., 'Computer Science')"}),
    )

    # --- This is the init method (NOW FIXED) ---
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs) 
        # We removed the broken 'get_username_case_sensitivity' check

    # --- This 'signup' method is required by allauth ---
    def signup(self, request, user):
        # This is where we save our custom fields
        user.university = self.cleaned_data['university']
        user.course = self.cleaned_data.get('course')
        user.save() # Save the user object to store the new data
        return user