from django.contrib import admin
from .models import TransportPost,CustomUser,Friendship

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(TransportPost)
admin.site.register(Friendship)


