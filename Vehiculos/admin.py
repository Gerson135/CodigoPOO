from django.contrib import admin
from .models import Cliente, Auto, AutoReparacion, Venta

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('identidad', 'nombre', 'email', 'telefono')
    search_fields = ('nombre', 'email', 'identidad')

@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'año', 'precio', 'estado', 'numero_serie')
    search_fields = ('marca', 'modelo', 'numero_serie')
    list_filter = ('estado', 'marca', 'año')
    list_editable = ('precio', 'estado')
    ordering = ('marca', 'modelo', 'año')  # Ordenar por marca, modelo y año

@admin.register(AutoReparacion)
class AutoReparacionAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'descripcion', 'fecha', 'precio_reparacion', 'estado')
    search_fields = ('vehiculo__marca', 'vehiculo__modelo', 'vehiculo__numero_serie')
    list_filter = ('estado', 'fecha')
    list_editable = ('estado',)
    date_hierarchy = 'fecha'  # Añadir una jerarquía de fechas para facilitar la navegación por fechas

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'cliente', 'fecha', 'precio_venta', 'estado')
    search_fields = ('vehiculo__marca', 'vehiculo__modelo', 'cliente__nombre', 'cliente__identidad')
    list_filter = ('estado', 'fecha')
    list_editable = ('estado',)
    date_hierarchy = 'fecha'  # Añadir una jerarquía de fechas para facilitar la navegación por fechas
    readonly_fields = ('precio_venta',)  # Hacer que el campo de precio de venta sea de solo lectura, ya que se asigna automáticamente

    def get_readonly_fields(self, request, obj=None):
        # Si la venta está completada, todos los campos son de solo lectura
        if obj and obj.estado == 'COMPLETADO':
            return self.readonly_fields + ('vehiculo', 'cliente', 'fecha', 'estado')
        return self.readonly_fields