from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from Vehiculos.models import Cliente, Auto, AutoReparacion, Venta

from Vehiculos.serializers import (
    AutoSerializer,
    VentaSerializer,
    AutoReparacionSerializer,
    ClienteSerializer,
)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'email', 'identidad']
    ordering_fields = ['nombre', 'identidad']
    def create(self, request):
        informacion = request.POST.pop("Lista Autos:")
        serializer = self.get_serializer(request.POST)
        if serializer.is_valid(raise_exception=True):
            info = serializer.save()
        
        for dato in informacion:
            dato["modelo"] = info.id
            serializer_dato = AutoSerializer(data=dato)
            if serializer_dato.is_valid(raise_exception=True):
                serializer_dato.save
            
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class AutoViewSet(viewsets.ModelViewSet):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['marca', 'modelo', 'numero_serie']
    ordering_fields = ['marca', 'modelo', 'año', 'precio']

class AutoReparacionViewSet(viewsets.ModelViewSet):
    queryset = AutoReparacion.objects.all()
    serializer_class = AutoReparacionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['vehiculo__marca', 'vehiculo__modelo', 'descripcion']
    ordering_fields = ['fecha', 'estado']

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['vehiculo__marca', 'vehiculo__modelo', 'cliente__nombre']
    ordering_fields = ['fecha', 'estado', 'precio_venta']
