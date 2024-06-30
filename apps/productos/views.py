from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Producto
from .serializers import ProductoSerializer

class ProductoList(ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoDetalleView(RetrieveAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'codigo_producto'
    permission_classes = [permissions.AllowAny]


class CrearProducto(CreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoUpdateView(UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'codigo_producto'
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            if partial:
                return Response({'message': 'Producto parcialmente actualizado exitosamente', 'data': serializer.data})
            else:
                return Response({'message': 'Producto completamente actualizado exitosamente', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoDeleteView(DestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'codigo_producto'
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'Producto eliminado exitosamente'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': f'Error al eliminar el producto: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.delete()





