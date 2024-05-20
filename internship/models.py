from django.db import models
from django.contrib.auth import get_user_model
from transport.models import CustomUser
# User = get_user_model()  
class Stage(models.Model):
    TYPE_CHOICES = (
        (1, 'Ouvrier'),
        (2, 'Technicien'),
        (3, 'PFE'),
    )
    #user = models.ForeignKey(CustomUser, related_name='recruiter', on_delete=models.CASCADE,)
    typeStg = models.IntegerField(choices=TYPE_CHOICES)
    societe = models.CharField(max_length=100)
    duree = models.IntegerField()
    sujet = models.CharField(max_length=200)
    contactInfo = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sujet} - {self.societe}"