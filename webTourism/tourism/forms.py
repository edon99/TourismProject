from django import forms
from django.core.validators import MaxValueValidator
from tourism.models import User, Location, Verification, Rating
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    class Meta():
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email')
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class VerificationForm(forms.ModelForm):
    phone_number = forms.CharField(
        label='Phone Number',
        validators=[phone_regex],
        max_length=17,  # Adjust the maximum length based on your needs
        help_text="Enter a valid phone number (e.g., +999999999)"
    )
    class Meta:
        model = Verification
        fields = ['address', 'phone_number','city','idCard']

class LocationForm(forms.ModelForm):
    latitude = forms.FloatField(
        widget=forms.HiddenInput(),
        error_messages={
            'required': 'Please choose a location on the map and click the button to confirm.',
            
        }
        )
    longitude = forms.FloatField(widget=forms.HiddenInput())
    description = forms.CharField(
        widget=forms.Textarea(attrs={'id': 'textArea'})
    )
    class Meta:
        model = Location
        fields = ['title', 'description','summary','city','weather','view','places', 'family_friendly']

class LocationSearchForm(forms.Form):
    city = forms.CharField(required=False)
    weather = forms.ChoiceField(choices=Location.WEATHER_COND, required=False)
    places = forms.MultipleChoiceField(choices=Location.PLACE_CHOICES, required=False)

class LocationRating(forms.ModelForm):
    rating = forms.DecimalField(
        max_digits=2,  # Max digits including decimal places
        decimal_places=1,  # Number of decimal places
        min_value=0,  # Minimum value
        max_value=10,  # Maximum value
        validators=[MaxValueValidator(10.0)],
        widget=forms.NumberInput(attrs={'step': '0.1'})  # Allowing 0.1 steps in HTML5
    )
    class Meta:
        model = Rating
        fields = ['proof','rating', 'comment']
        
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }