from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import AccommodationForm, BookingForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .models import Booking, Accommodation
from django.shortcuts import render, get_object_or_404

@login_required
def logement(request):
    # template = loader.get_template('homePage.html')
    return render(request,"homePage.html")
@login_required
def search_results(request):
    location = request.GET.get('location')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    accommodations = Accommodation.objects.all()

    if location:
        accommodations = accommodations.filter(address__icontains=location)
    if min_price:
        accommodations = accommodations.filter(price__gte=min_price)
    if max_price:
        accommodations = accommodations.filter(price__lte=max_price)

    return render(request, 'search_results.html', {'accommodations': accommodations})

@login_required
def register_accommodation(request):
    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES)
        if form.is_valid():
            # Set the current user as the landlord
            accommodation = form.save(commit=False)
            accommodation.landlord = request.user  # Set the landlord to the current user
            accommodation.save()
            # Redirect to a success page or do something else
            return redirect('logement')  # Replace 'success_page' with the URL name of your success page
    else:
        form = AccommodationForm()
    return render(request, 'register_accommodation.html', {'form': form})

@login_required
def book_accommodation(request, accommodation_id):
    accommodation = Accommodation.objects.get(pk=accommodation_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            is_confirmed = request.POST.get('is_confirmed') == 'on'
            booking = Booking.objects.create(
                accommodation=accommodation,
                student=request.user,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                is_confirmed=is_confirmed
            )
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'book_accommodation.html', {'accommodation': accommodation, 'form': form})
@login_required
def booking_confirmation(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})
@login_required
def leave_review(request, accommodation_id):
    accommodation = Accommodation.objects.get(pk=accommodation_id)
    form = ReviewForm()
    return render(request, 'leave_review.html', {'form': form, 'accommodation': accommodation})

@login_required
def submit_review(request, accommodation_id):
    accommodation = Accommodation.objects.get(pk=accommodation_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.accommodation = accommodation
            review.student = request.user  # Assign the current user as the reviewer
            review.save()
            return redirect('accommodation_reviews')
    else:
        form = ReviewForm()

    return render(request, 'submit_review.html', {'form': form, 'accommodation': accommodation})
# @login_required
def accommodation_reviews(request):
    accommodations = Accommodation.objects.all()
    return render(request, 'accommodation_reviews.html', {'accommodations': accommodations})