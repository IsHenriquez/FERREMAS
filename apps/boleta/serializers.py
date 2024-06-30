from rest_framework import serializers
from .models import Boleta

class BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleta
        fields = '__all__'
