from rest_framework import serializers
from .models import Cliente, Auto, AutoReparacion, Venta

class AutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auto
        fields = '__all__'

class AutoReparacionSerializer(serializers.ModelSerializer):
    vehiculo = serializers.PrimaryKeyRelatedField(queryset=Auto.objects.all())

    class Meta:
        model = AutoReparacion
        fields = '__all__'

    def update(self, instance, validated_data):
        if validated_data.get('estado') == 'COMPLETADO' and instance.estado != 'COMPLETADO':
            auto = validated_data.get('vehiculo', instance.vehiculo)
            precio_reparacion = validated_data.get('precio_reparacion', instance.precio_reparacion)
            auto.precio += precio_reparacion  # Ajusta el precio del auto sumando el costo de la reparación
            auto.estado = 'DISPONIBLE'  # Cambia el estado del auto a disponible
            auto.save()

        return super().update(instance, validated_data)

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    vehiculo = serializers.PrimaryKeyRelatedField(queryset=Auto.objects.all())
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())

    class Meta:
        model = Venta
        fields = '__all__'

    def validate(self, data):
        vehiculo = data.get('vehiculo')
        if vehiculo.estado != 'DISPONIBLE':
            raise serializers.ValidationError("El vehículo seleccionado no está disponible para la venta.")
        return data

    def create(self, validated_data):
        vehiculo = validated_data['vehiculo']

        validated_data['precio_venta'] = vehiculo.precio

        venta = super().create(validated_data)
        vehiculo.estado = 'VENDIDO'
        vehiculo.save()

        return venta