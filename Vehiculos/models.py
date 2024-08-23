from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Modelo de clientes
class Cliente(models.Model):
    identidad = models.CharField("Identidad", max_length=15, unique=True)
    nombre = models.CharField("Nombre Completo", max_length=60)
    direccion = models.TextField("Dirección")
    telefono = models.CharField("Telefono", max_length=20)
    email = models.EmailField("Email", unique=True)

    def __str__(self):
        return f"{self.nombre} - {self.identidad}"

    class Meta:
        verbose_name_plural = "Clientes"
        verbose_name = "Cliente"

# Modelo de autos
class Auto(models.Model):
    ESTADO_AUTO = [
        ('DISPONIBLE', 'Disponible'),
        ('VENDIDO', 'Vendido'),
        ('REPARACION', 'En Mantenimiento'),
    ]
    
    marca = models.CharField("Marca", max_length=50)
    modelo = models.CharField("Modelo", max_length=50)
    año = models.IntegerField("Año")
    precio = models.DecimalField("Precio", max_digits=10, decimal_places=2)
    estado = models.CharField("Estado", max_length=15, choices=ESTADO_AUTO, default='DISPONIBLE')
    numero_serie = models.CharField("Número de Serie", max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.año}) - {self.numero_serie}"

    class Meta:
        verbose_name_plural = "Autos"
        verbose_name = "Auto"

# Modelo de reparaciones
class AutoReparacion(models.Model):
    ESTADO_REPARACION = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
    ]
    
    vehiculo = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name='reparaciones')
    descripcion = models.TextField("Descripción")
    fecha = models.DateField("Fecha")
    precio_reparacion = models.DecimalField("Precio de Reparación", max_digits=10, decimal_places=2)
    estado = models.CharField("Estado", max_length=15, choices=ESTADO_REPARACION, default='PENDIENTE')
    
    def __str__(self):
        return f"Reparación de {self.vehiculo} - {self.fecha}"

    class Meta:
        verbose_name_plural = "Reparaciones"
        verbose_name = "Reparación"

@receiver(post_save, sender=AutoReparacion)
def actualizar_precio_auto(sender, instance, **kwargs):
    if instance.estado == 'COMPLETADO':
        auto = instance.vehiculo
        auto.precio += instance.precio_reparacion
        auto.estado = 'DISPONIBLE'
        auto.save()

# Modelo de ventas
class Venta(models.Model):
    ESTADO_VENTA = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('FALLIDO', 'Fallido'),
    ]
    
    vehiculo = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name='ventas')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ventas')
    fecha = models.DateField("Fecha")
    precio_venta = models.DecimalField("Precio de Venta", max_digits=10, decimal_places=2)
    estado = models.CharField("Estado", max_length=15, choices=ESTADO_VENTA, default='PENDIENTE')
    
    def __str__(self):
        return f"Venta de {self.vehiculo} a {self.cliente} - {self.fecha}"

    class Meta:
        verbose_name_plural = "Ventas"
        verbose_name = "Venta"

@receiver(pre_save, sender=Venta)
def asignar_precio_venta(sender, instance, **kwargs):
    if not instance.pk:  # Si es una nueva venta
        instance.precio_venta = instance.vehiculo.precio

@receiver(post_save, sender=Venta)
def actualizar_estado_auto(sender, instance, **kwargs):
    if instance.estado == 'COMPLETADO':
        auto = instance.vehiculo
        auto.estado = 'VENDIDO'
        auto.save()