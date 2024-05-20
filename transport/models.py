from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils.crypto import get_random_string


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='profile_photos', null=True, blank=True)
    id_number = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone_number', 'id_number']

    def __str__(self):
        return self.email

class Friendship(models.Model):
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendships1')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendships2')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name='unique_friendship')
        ]

    def __str__(self):
        return f"{self.user1.email} - {self.user2.email}"



class TransportPost(models.Model):
    TYPE_CHOICES = (
        ('offer', 'Offer'),
        ('request', 'Request'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transport_posts',default=None)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.CharField(max_length=50)
    seats_available = models.IntegerField()
    contact_info = models.CharField(max_length=100)
    type_choice = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.type_choice}: {self.departure} to {self.destination}"
    
    def get_post_type(self):
        return 'Transport'