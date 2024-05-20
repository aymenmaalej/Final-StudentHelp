from datetime import date
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

class Categorie(models.Model):
    TYPE_CHOICES = [
        ('Al','Alimentaire'),
        ('Vt','Vetement'),
        ('ACc','Accessoires'),
    ]
    name = models.CharField(max_length=50, default='Accessoires', choices=TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.name}"

class Produit(models.Model):
    libelle = models.CharField(max_length=100)
    description = models.TextField(default="")
    prix = models.DecimalField(max_digits=10, decimal_places=3) 
    Img = models.ImageField(blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)
    fournisseur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.libelle} - {self.description} - {self.prix}"

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()
    telephone = models.CharField(max_length=8)

    def __str__(self):
        return self.nom

class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    totalCde = models.DecimalField(max_digits=10, decimal_places=3)
    produits = models.ManyToManyField(Produit) 
    
    def __str__(self):
        return f"{self.dateCde} - {self.totalCde}"

class ProduitNC(Produit):
    duree_garantie = models.CharField(max_length=100)
    def __str__(self):
        return super().__str__()+" "+self.duree_garantie
        
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.prix * self.quantity
