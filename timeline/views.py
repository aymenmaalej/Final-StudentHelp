from asyncio.log import logger
from pyexpat.errors import messages
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from logement.models import Accommodation
from transport.models import TransportPost,Friendship
from .models import Post,Like,Notification,Message
from random import shuffle
from django.contrib.auth import get_user_model,authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Exists,OuterRef,Q
from django.template.defaultfilters import date as _date
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def home(request):
    user = request.user
    User = get_user_model()
    # Get the email addresses of the current user's friends using Friendship model
    friend_emails = Friendship.objects.filter(Q(user1=user) | Q(user2=user)).values_list(
        'user1__email', 'user2__email'
    ).distinct()
    
    # Flatten the list of email addresses
    friend_emails = set(sum(friend_emails, ()))

    # Retrieve CustomUser objects for the friend emails
    friends = User.objects.filter(email__in=friend_emails)

    # Annotate posts with like count
    posts = Post.objects.annotate(like_count=Count('like'))

    # Shuffle posts
    shuffled_posts = list(posts)
    shuffle(shuffled_posts)

    return render(request, 'home.html', {'posts': shuffled_posts, 'friends': friends})


def send_friend_request(request):
    if request.method == 'POST':
        User = get_user_model()
        recipient_email = request.POST.get('recipient_email')
        try:
            recipient = User.objects.get(email=recipient_email)  # Get the recipient user object
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Recipient user does not exist'}, status=400)
        sender = request.user
        # Create a new friend request notification
        notification = Notification.objects.create(
            sender=sender,
            recipient=recipient,
            message=f'{sender.name} {sender.surname} sent you a friend request.',
            notification_type='friend_request'
        )
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    

def fetch_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user)
        serialized_notifications = []
        for notification in notifications:
            if notification.notification_type == 'friend_request':
                sender_name = f"{notification.sender.name} {notification.sender.surname}"
                sender_photo = notification.sender.photo.url if notification.sender.photo else None
                message = f"Friend request from {sender_name}"
                serialized_notification = {
                    'sender': sender_name,
                    'sender_photo': sender_photo,
                    'message': message,
                    'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'accept_button': f'<button class="btn btn-sm btn-info mb-2 btn-accept-friend-request" data-sender-email="{notification.sender.email}">Accept</button>',
                    'deny_button': f'<button class="btn btn-sm btn-danger mb-2 btn-deny-friend-request" data-sender-email="{notification.sender.email}">Deny</button>',
                }
            else:
                serialized_notification = {
                    'sender': "System",
                    'sender_photo': None,
                    'message': notification.message,
                    'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'accept_button': '',
                    'deny_button': '',
                }
            serialized_notifications.append(serialized_notification)
        return JsonResponse({'notifications': serialized_notifications})
    else:
        return JsonResponse({'notifications': []})
    
@csrf_exempt
def handle_friend_request(request):
    if request.method == 'POST' and request.user.is_authenticated:
        action = request.POST.get('action')
        sender_email = request.POST.get('sender_email')
        User = get_user_model()
        try:
            sender = User.objects.get(email=sender_email)
            notification = Notification.objects.get(sender=sender, recipient=request.user, notification_type='friend_request')
            if action == 'accept':
                # Create friendship between sender and recipient
                Friendship.objects.create(user1=request.user, user2=sender)
                notification.delete()
                return JsonResponse({'status': 'success', 'message': 'Friend request accepted.'})

            elif action == 'deny':
                # Delete the friendship request
                Friendship.objects.filter(user1=sender, user2=request.user).delete()
                notification.delete()
                return JsonResponse({'status': 'success', 'message': 'Friend request denied.'})

            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid action.'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sender does not exist.'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)
@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        User = get_user_model()
        recipient_email = request.POST.get('recipient_email')
        content = request.POST.get('content')
        try:
            recipient = User.objects.get(email=recipient_email)
            message = Message.objects.create(sender=request.user, recipient=recipient, content=content)
            return JsonResponse({'status': 'success', 'message': 'Message sent successfully.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Recipient does not exist.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

@login_required
def fetch_messages(request, friend_email):
    try:
        User = get_user_model()
        friend = User.objects.get(email=friend_email)
        # Retrieve messages between the current user and the friend
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient=friend)) | (Q(sender=friend) & Q(recipient=request.user))
        ).order_by('timestamp')
        serialized_messages = [
            {
                'sender': message.sender.name + ' ' + message.sender.surname,  # Corrected concatenation
                'recipient': message.recipient.name + ' ' + message.recipient.surname,  # Corrected concatenation
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            } for message in messages
        ]
        return JsonResponse({'messages': serialized_messages})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Friend does not exist.'}, status=400)


def profile_view(request, email):
    User = get_user_model()
    profile_user = get_object_or_404(User, email=email)
    posts = Post.objects.filter(user=profile_user).annotate(like_count=Count('like'))
    
    # Check if the profile user is a friend of the logged-in user
    is_friend = False
    if request.user.is_authenticated:
        if Friendship.objects.filter(user1=request.user, user2=profile_user).exists() or Friendship.objects.filter(user1=profile_user, user2=request.user).exists():
            is_friend = True
    
    for post in posts:
        post.created_at = post.created_at.strftime("%A, %B %d, %Y").split(", ")
    
    return render(request, 'profile.html', {'profile_user': profile_user, 'posts': posts, 'is_friend': is_friend})
@csrf_exempt
def accept_friend_request(request):
    if request.method == 'POST' and request.is_ajax():
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Authentication required'}, status=401)

        # Validate input: ensure sender_email is provided
        sender_email = request.POST.get('sender_email')
        if not sender_email:
            return JsonResponse({'status': 'error', 'message': 'Sender email is required'}, status=400)

        User = get_user_model()
        # Get sender object or return 404 if not found
        sender = get_object_or_404(User, email=sender_email)

        # Check if the sender is already a friend
        if Friendship.objects.filter(user1=request.user, user2=sender).exists():
            return JsonResponse({'status': 'error', 'message': 'Sender is already a friend'}, status=400)

        try:
            # Create friendship between sender and recipient
            Friendship.objects.create(user1=request.user, user2=sender)

            logger.info(f"Friend request accepted: {sender_email} added to {request.user.email}'s friends list")
            return JsonResponse({'status': 'success', 'message': 'Friend request accepted'})
        except Exception as e:
            logger.error(f"Error accepting friend request: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Failed to accept friend request'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def like_post(request, post_id):
    if request.method == 'POST':
        user = request.user
        post = Post.objects.get(pk=post_id)
        
        # Check if the user has already liked the post
        if Like.objects.filter(user=user, post=post).exists():
            # User has already liked the post, so unlike it
            Like.objects.filter(user=user, post=post).delete()
            liked = False
        else:
            # User has not liked the post, so like it
            Like.objects.create(user=user, post=post)
            liked = True
        
        # Return JSON response indicating whether the post was liked or unliked
        return JsonResponse({'liked': liked})
    else:
        # Method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def check_like(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.filter(pk=post_id).first()
        if post:
            user_liked = Like.objects.filter(user=request.user, post=post).exists()
            return JsonResponse({'liked': user_liked})
    return JsonResponse({'liked': False}) 