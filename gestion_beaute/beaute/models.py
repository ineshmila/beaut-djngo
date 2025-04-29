from django.db import models
from django.contrib.auth.models import User


class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    categorie = models.CharField(max_length=50, choices=[
        ('cosmetics', 'Cosmetics'),
        ('makeup', 'Makeup'),
        ('powder', 'Powder'),
        ('lotions', 'Lotions'),
        ('lipstick', 'Lipstick'),
        ('mascara', 'Mascara'),
    ])


class PanierItem(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"
