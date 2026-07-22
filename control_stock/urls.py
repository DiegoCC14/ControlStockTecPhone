
from django.urls import path
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test

from .views import ClienteListView, StockListView, VentasListView, ReservasListView


urlpatterns = [
    
    path('login/', LoginView.as_view( template_name='admin/login.html', next_page='home' ) , name='login'),
    path('logout/', LogoutView.as_view(next_page='login') , name='logout'),


    path( '',
        user_passes_test(
            lambda user: user.is_superuser or user.groups.filter(name__in=['Vendedor']).exists(),
            login_url='login'
        ) ( RedirectView.as_view(pattern_name='stock') ), name='home' ),
    
    path( 'clientes/',
        user_passes_test(
            lambda user: user.is_superuser,
            login_url='login'
        ) (ClienteListView.as_view()), name='clientes' ),

    
    path( 'stock/',
        user_passes_test(
            lambda user: user.is_superuser or user.groups.filter(name__in=['Vendedor']).exists(),
            login_url='login'
        ) (StockListView.as_view()), name='stock' ),
    
    path('ventas/', login_required( VentasListView.as_view() ), name='ventas'),
    path('reserva/', login_required( ReservasListView.as_view() ), name='reserva'),
    
    #path('panel_control/', login_required( TemplateView.as_view(template_name='panel_control.html') ), name='panel_control'),
    path( 'panel_control/',
        user_passes_test(
            lambda user: user.is_superuser,
            login_url='login'
        ) ( TemplateView.as_view(template_name='panel_control.html') ), name='panel_control' ),

]
