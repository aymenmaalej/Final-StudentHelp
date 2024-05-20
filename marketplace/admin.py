from django.contrib import admin
from .models import Produit,Categorie,Fournisseur, Commande , ProduitNC

# Register your models here.
admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Fournisseur)
admin.site.register(Commande)
admin.site.register(ProduitNC)