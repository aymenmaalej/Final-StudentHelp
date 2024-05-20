from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from . import forms
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name=''),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('profile/<str:email>/', views.profile_view, name='profile'),
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('check_like/<int:post_id>/', views.check_like, name='check_like'),
    path('fetch_notifications/', views.fetch_notifications, name='fetch_notifications'),
    path('handle_friend_request/', views.handle_friend_request, name='handle_friend_request'),
    path('send_message/', views.send_message, name='send_message'),
    path('fetch_messages/<str:friend_email>/', views.fetch_messages, name='fetch_messages'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)