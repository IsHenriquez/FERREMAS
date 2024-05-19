from django.urls import path
from .views import ProductoList, ProductoDetalleView

urlpatterns = [
    path('productos/', ProductoList.as_view(), name='producto-list'),
    path('productos/<str:codigo_producto>/', ProductoDetalleView.as_view(), name='detalle-producto'),
]
