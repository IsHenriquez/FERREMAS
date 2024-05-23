# apps/addproductos/urls.py
from django.urls import path
from . import views

app_name = 'addproductos'

urlpatterns = [
    path('carrito/', views.add_to_cart, name='carrito'),
]
