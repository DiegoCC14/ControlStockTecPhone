from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from .models import Cliente

class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes.html'
    context_object_name = 'clientes'

    def get_queryset(self):
        queryset = Cliente.objects.all().order_by('-fecha_ingreso')
        filtro_nombre = self.request.GET.get('nombre', '')
        filtro_dni = self.request.GET.get('dni', '')
        filtro_telefono = self.request.GET.get('telefono', '')
        
        if filtro_nombre:
            queryset = queryset.filter(nombre__icontains=filtro_nombre)
        if filtro_dni:
            queryset = queryset.filter(dni__icontains=filtro_dni)
        if filtro_telefono:
            queryset = queryset.filter(telefono__icontains=filtro_telefono)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro_nombre'] = self.request.GET.get('nombre', '')
        context['filtro_dni'] = self.request.GET.get('dni', '')
        context['filtro_telefono'] = self.request.GET.get('telefono', '')
        return context

    # Unico metodo POST que maneja las 3 acciones
    def post(self, request, *args, **kwargs):
        # Obtenemos la accion que el formulario quiere ejecutar
        accion = request.POST.get('accion')
        
        if accion == 'crear':
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            dni = request.POST.get('dni')
            telefono = request.POST.get('telefono')
            email = request.POST.get('email')
            
            if dni and nombre and apellido:
                Cliente.objects.get_or_create(
                    dni=dni,
                    defaults={'nombre': nombre, 'apellido': apellido, 'telefono': telefono, 'email': email}
                )
                
        elif accion == 'editar':
            dni = request.POST.get('dni')
            cliente = get_object_or_404(Cliente, dni=dni)
            cliente.nombre = request.POST.get('nombre')
            cliente.apellido = request.POST.get('apellido')
            cliente.telefono = request.POST.get('telefono')
            cliente.email = request.POST.get('email')
            cliente.save()
            
        elif accion == 'eliminar':
            dni = request.POST.get('dni')
            cliente = get_object_or_404(Cliente, dni=dni)
            cliente.delete()
            
        return redirect('clientes')