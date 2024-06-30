from django.urls import path
from . import views

app_name = 'boleta'

urlpatterns = [
    path('boleta/generar/', views.generar_boleta, name='generar-boleta'),
    path('boleta/<int:cart_id>/', views.obtener_boleta, name='obtener-boleta'),
]