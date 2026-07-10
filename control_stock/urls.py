
from django.urls import path
from django.views.generic import TemplateView

from .views import ClienteListView


urlpatterns = [
    path('ventas/', TemplateView.as_view(template_name='ventas.html'), name='ventas'),
    path('clientes/', ClienteListView.as_view(), name='clientes'),
    path('reserva/', TemplateView.as_view(template_name='reserva.html'), name='reserva'),
    path('panel_control/', TemplateView.as_view(template_name='panel_control.html'), name='panel_control'),
    path('stock/', TemplateView.as_view(template_name='stock.html'), name='stock'),
]
