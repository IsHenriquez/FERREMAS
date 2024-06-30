from django.urls import path
from .views import ProductoList, ProductoDetalleView, CrearProducto, ProductoUpdateView, ProductoDeleteView

urlpatterns = [
    path('productos/', ProductoList.as_view(), name='producto-list'),
    path('productos/<codigo_producto>/', ProductoDetalleView.as_view(), name='producto-detail'),
    path('productos/admin/create/', CrearProducto.as_view(), name='crear-producto'),
    path('productos/<codigo_producto>/admin/edit/', ProductoUpdateView.as_view(), name='producto-update'),
    path('productos/<codigo_producto>/admin/delete/', ProductoDeleteView.as_view(), name='producto-delete'),
]
