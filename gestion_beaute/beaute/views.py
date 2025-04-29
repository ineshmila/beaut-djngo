from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit
from .forms import ProduitForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import PanierItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
def liste_produits(request):
    query = request.GET.get('q')
    if query:
        produits_list = Produit.objects.filter(nom__icontains=query)
    else:
        produits_list = Produit.objects.all()

    paginator = Paginator(produits_list, 6)
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)
    
    return render(request, 'produits/liste.html', {'produits': produits})

@login_required
def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm()
    return render(request, 'produits/formulaire.html', {'form': form})

@login_required
def modifier_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'produit/formulaire.html', {'form': form})

@login_required
def supprimer_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        produit.delete()
        return redirect('liste_produits')
    return render(request, 'produits/confirmer_suppression.html', {'produit': produit})
 
from django.shortcuts import redirect

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)

                # Vérifie si c'est l'admin
                if username == 'ines12' and password == 'ines123':
                    return redirect('liste_produits')  # admin → liste_produits
                else:
                    return redirect('featured_products')  # user → featured_products
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Nom d\'utilisateur ou mot de passe invalide'})
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Informations incorrectes'})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        # Vérification des données
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Le nom d\'utilisateur existe déjà.')
            return redirect('signup')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, 'Utilisateur créé avec succès.')
            return redirect('login')  # Redirige l'utilisateur vers la page de connexion après l'inscription

    return render(request, 'signup.html')
def logout(request):
    auth_logout(request)  # Cette ligne déconnecte l'utilisateur
    return redirect('home')
def home(request):
    produits = Produit.objects.all()
    return render(request, 'home.html', {'produits': produits})
def test(request):
    return render(request, 'test.html')
def featured_products(request):
    produits = Produit.objects.all()
    return render(request, 'featured_products.html',{'produits': produits})
def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm()
    return render(request, 'ajouter_produit.html', {'form': form})

def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'liste_produits.html', {'produits': produits})
from django.shortcuts import render, get_object_or_404, redirect
from .models import Produit
from .forms import ProduitForm

def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')  # redirection après modification
    else:
        form = ProduitForm(instance=produit)

    return render(request, 'modifier_produit.html', {'form': form, 'produit': produit})
@require_POST
def supprimer_produit_ajax(request, produit_id):
    try:
        produit = Produit.objects.get(id=produit_id)
        produit.delete()
        return JsonResponse({'success': True})
    except Produit.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Produit non trouvé'})
def produits_par_categorie(request, nom_categorie):
    produits = Produit.objects.filter(categorie=nom_categorie)
    return render(request, 'produits_par_categorie.html', {
        'produits': produits,
        'categorie': nom_categorie
    })


@login_required
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    panier_item, created = PanierItem.objects.get_or_create(utilisateur=request.user, produit=produit)

    if not created:
        panier_item.quantite += 1
        panier_item.save()

    return redirect('featured_products')
@login_required
def panier(request):
    # Récupère tous les produits dans le panier de l'utilisateur connecté
    panier_items = PanierItem.objects.filter(utilisateur=request.user)
    total = sum([item.produit.prix * item.quantite for item in panier_items])
    
    return render(request, 'panier.html', {'panier_items': panier_items, 'total': total})