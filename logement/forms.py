from django import forms
from .models import Accommodation,Booking,Review

class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['title', 'description', 'address', 'price', 'bedrooms', 'bathrooms', 'is_furnished', 'available_from', 'available_to', 'image']
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']