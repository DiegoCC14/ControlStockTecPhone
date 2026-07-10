from django.contrib import admin
from .models import (
    Moneda, EstadoCelular, ColorCelular, MarcaModelo,
    ModeloCelular, EstadoReserva, Celular, LogCelular,
    Cliente, ReservaCelular, VentaCelular
)

admin.site.register(Moneda)
admin.site.register(EstadoCelular)
admin.site.register(ColorCelular)
admin.site.register(MarcaModelo)
admin.site.register(ModeloCelular)
admin.site.register(EstadoReserva)
admin.site.register(Celular)
admin.site.register(LogCelular)
admin.site.register(Cliente)
admin.site.register(ReservaCelular)
admin.site.register(VentaCelular)