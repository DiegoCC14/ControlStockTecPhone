
from django.urls import path
from django.views.generic import TemplateView, RedirectView

from .views import ClienteListView, StockListView, VentasListView, ReservasListView


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='panel_control', permanent=False), name='home'),
    path('clientes/', ClienteListView.as_view(), name='clientes'),
    path('stock/', StockListView.as_view(), name='stock'),
    path('ventas/', VentasListView.as_view(), name='ventas'),
    path('reserva/', ReservasListView.as_view(), name='reserva'),
    
    path('panel_control/', TemplateView.as_view(template_name='panel_control.html'), name='panel_control'),
    
    
]
