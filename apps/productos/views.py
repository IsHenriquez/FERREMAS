from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions, generics
from .models import Producto
from .serializers import ProductoSerializer

class ProductoList(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class ProductoDetalleView(RetrieveAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'codigo_producto'
    permission_classes = [permissions.AllowAny]

