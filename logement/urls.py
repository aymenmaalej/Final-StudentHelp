from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('logement/', views.logement, name='logement'),
    path('search/', views.search_results, name='search_results'),
    path('register/', views.register_accommodation, name='register_accommodation'),
    path('book/<int:accommodation_id>/', views.book_accommodation, name='book_accommodation'),
    path('booking_confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('leave_review/<int:accommodation_id>/', views.leave_review, name='leave_review'),
    path('submit_review/<int:accommodation_id>/', views.submit_review, name='submit_review'),
    path('accommodation_reviews/', views.accommodation_reviews, name='accommodation_reviews'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)