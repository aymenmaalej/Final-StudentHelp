from django.urls import path
from . import views

urlpatterns = [
    path('marketplace/main', views.index, name='marketplace/main'),
    path('marketplace/fournisseur', views.indexFrs, name='fournisseur'),
    path('marketplace/vitrine', views.indexVtr, name='vitrine'),
    path('marketplace/majprod', views.majProd, name='majprod'),
    path('marketplace/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('marketplace/add_product/', views.register_product, name='add_product'),
    path('marketplace/cart/', views.view_cart, name='cart'),
    path('marketplace/decrease_quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('marketplace/remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('marketplace/generate_pdf/', views.generate_pdf, name='generate_pdf'), 
    
]
