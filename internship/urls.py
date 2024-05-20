from django.urls import path
from . import views

urlpatterns = [
    path('internship', views.internship_selection, name='internship'),
    path('new_internship_proposal/', views.new_internship_proposal, name='new_internship_proposal'),
    path('view_internship_offers/', views.view_internship_offers, name='view_internship_offers'), 
]