
from django.urls import path
from django.views.generic import TemplateView, RedirectView

from .views import ClienteListView, StockListView


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='panel_control', permanent=False), name='home'),
    path('clientes/', ClienteListView.as_view(), name='clientes'),
    path('stock/', StockListView.as_view(), name='stock'),
    
    path('ventas/', TemplateView.as_view(template_name='ventas.html'), name='ventas'),
    path('reserva/', TemplateView.as_view(template_name='reserva.html'), name='reserva'),
    path('panel_control/', TemplateView.as_view(template_name='panel_control.html'), name='panel_control'),
    
    
]
