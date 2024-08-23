from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Vehiculos.api import (
    ClienteViewSet,
    AutoViewSet,
    AutoReparacionViewSet,
    VentaViewSet,
)

router = DefaultRouter()

router.register(r"Clientes", ClienteViewSet)
router.register(r"Autos", AutoViewSet)
router.register(r"Reparaciones", AutoReparacionViewSet)
router.register(r"Ventas", VentaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]