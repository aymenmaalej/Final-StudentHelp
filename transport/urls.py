from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import forms

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),  
    path('transport/', views.transport_selection, name='transport_selection'),
    path('userSearch/', views.search, name='userSearch'),
    # path('transport/offers/', views.offer_transport, name='offer_transport'),
    path('transport/offertransport/', views.offer_transport, name='offer_transport'),
    path('transport/transportoffers/', views.transport_offers, name='transport_offers'),
    path('book-transport/<int:offer_id>/', views.book_transport, name='book_transport'),
]