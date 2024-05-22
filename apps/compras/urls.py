from django.urls import path
from . import views

urlpatterns = [
    path('finalizar_compra/<int:cart_id>/', views.finalizar_compra, name='finalizar_compra'),
]