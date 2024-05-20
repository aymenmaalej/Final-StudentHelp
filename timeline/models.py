from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from transport.models import TransportPost,CustomUser
from internship.models import Stage
from marketplace.models import Produit
from logement.models import Accommodation
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,AbstractUser
# Ensure that all authentication-related imports use your CustomUser model
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
User = get_user_model()  

class Post(models.Model):
    CATEGORY_CHOICES = (
        ('transport', 'Transport'),
        ('marketplace', 'Marketplace'),
        ('accommodations', 'Accommodations'),
        ('job_offers', 'Job Offers'),
        ('job_requests', 'Job Requests'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    image = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return f"{self.created_at} - {self.category.capitalize()}"

    class Meta:
        verbose_name_plural = 'Posts'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('message', 'Message'),
        ('friend_request', 'Friend Request'),
        ('comment', 'Comment'),
        ('like', 'Like'),
        # Add more types as needed
    )
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE,default=None)
    recipient = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE, default=None)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.name} -> {self.recipient.name}: {self.message}'

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"

@receiver(post_save, sender=TransportPost)
def create_transport_post(sender, instance, created, **kwargs):
    if created:
        Post.objects.create(
            user=instance.user,  # Assuming TransportPost has a 'user' field
            description=instance.destination,  # Adjust field if necessary
            category='transport',
            image=None  # Adjust field if necessary
            
        )


@receiver(post_save, sender=Stage)
def create_stage_post(sender, instance, created, **kwargs):
    if created:
        category = 'job_offers' if instance.typeStg == 3 else 'job_requests'
        Post.objects.create(
            user=instance.user,
            description=instance.sujet,
            category=category,
            image=instance.user.photo  # Assuming CustomUser has a 'photo' field
        )


@receiver(post_save, sender=Produit)
def create_produit_post(sender, instance, created, **kwargs):
    if created:
        Post.objects.create(
            user=instance.fournisseur,  # Assuming Produit has a 'user' field
            description=instance.description,  # Adjust field if necessary
            category='marketplace',
            image=instance.Img  # Adjust field if necessary
        )


@receiver(post_save, sender=Accommodation)
def create_accommodation_post(sender, instance, created, **kwargs):
    if created:
        Post.objects.create(
            user=instance.landlord,  # Assuming Accommodation has a 'landlord' field
            description=instance.description,  # Adjust field if necessary
            category='accommodations',
            image=instance.image  # Adjust field if necessary
        )
# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, password, **extra_fields)

# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     name = models.CharField(max_length=50)
#     surname = models.CharField(max_length=50)
#     phone_number = models.CharField(max_length=15)
#     id_number = models.CharField(max_length=20, unique=True)
#     photo = models.ImageField(upload_to='profile_photos', null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name', 'surname', 'phone_number', 'id_number']

#     def __str__(self):
#         return self.email
