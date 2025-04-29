from django import forms
from .models import Produit
CATEGORIES_CHOICES = [
        ('cosmetics', 'Cosmetics'),
        ('makeup', 'Makeup'),
        ('powder', 'Powder'),
        ('lotions', 'Lotions'),
        ('lipstick', 'Lipstick'),
        ('mascara', 'Mascara'),
]
class ProduitForm(forms.ModelForm):
    categorie = forms.ChoiceField(choices=CATEGORIES_CHOICES)

    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'image', 'categorie']
