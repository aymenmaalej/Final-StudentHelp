from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import OfferForm,CustomUserCreationForm,TransportPostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required # import login function
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout  # Add this import
from .models import CustomUser,TransportPost
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model
from django.db import models
def logout_view(request):
    django_logout(request)  
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            auth_login(request, user)
            return redirect('')  # Redirect to the appropriate URL after login
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def search(request):
    query = request.GET.get('q', '')
    if query:
        users = CustomUser.objects.filter(models.Q(name__icontains=query) | models.Q(surname__icontains=query))
        results = [{'email':user.email,'name': user.name,'surname':user.surname,'img':user.photo.url} for user in users]
    else:
        results = []
    return JsonResponse(results, safe=False)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Search for a CustomUser instance with the provided email
        user = CustomUser.objects.filter(email=email).first()

        # Authenticate the user if found and the password is correct
        if user is not None and user.check_password(password):
            auth_login(request, user)  # Login the user
            return redirect('')    # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')



@login_required
def transport_selection(request):
    return render(request, 'transport_selection.html')

def offer_transport(request):
    if request.method == 'POST':
        form = TransportPostForm(request.POST)
        if form.is_valid():
            transport_post = form.save(commit=False)  # Create the instance but don't save to the database yet
            transport_post.user = request.user       # Set the user to the current logged-in user
            transport_post.save()                    # Now save it to the database
            return redirect('transport_offers')        # Redirect to some success page
    else:
        form = TransportPostForm()
    return render(request, 'offer_form.html', {'form': form})


def transport_offers(request):
    all_offers = TransportPost.objects.all()
    paginator = Paginator(all_offers, 5)

    page_number = request.GET.get('page')
    try:
        offers = paginator.page(page_number)
    except PageNotAnInteger: 
        offers = paginator.page(1)
    except EmptyPage: 
        offers = paginator.page(paginator.num_pages)

    return render(request, 'transport_offers.html', {'offers': offers})

def book_transport(request, offer_id):
    offer = get_object_or_404(TransportPost, pk=offer_id)
    if offer.seats_available > 0:
        offer.seats_available -= 1
        if offer.seats_available == 0: 
            offer.delete()
        else:
            offer.save() 
        return redirect('transport_offers') 