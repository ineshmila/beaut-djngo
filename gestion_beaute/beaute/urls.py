from django.urls import path

from . import views

urlpatterns = [
  
    path('ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('modifier/<int:id>/', views.modifier_produit, name='modifier_produit'),
    path('supprimer/<int:id>/', views.supprimer_produit, name='supprimer_produit'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),  
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('liste_produits/', views.liste_produits, name='liste_produits'),
    path('featured_products/', views.featured_products, name='featured_products'),
    path('modifier_produit/<int:produit_id>/', views.modifier_produit, name='modifier_produit'),
    path('produits/modifier/<int:produit_id>/', views.modifier_produit, name='modifier_produit'),
    path('supprimer-produit-ajax/<int:produit_id>/', views.supprimer_produit_ajax, name='supprimer_produit_ajax'),
    path('categorie/<str:nom_categorie>/', views.produits_par_categorie, name='produits_par_categorie'),
    path('test/', views.test, name='test'),
    path('ajouter_au_panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/', views.panier, name='panier'),
    path('logout/', views.logout, name='logout'),

]
