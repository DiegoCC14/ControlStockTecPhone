from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from .models import Cliente, Celular, ModeloCelular, ColorCelular, EstadoCelular, Moneda
from .models import LogCelular

import json


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
            
            if dni: #Solo necesitamos dni, para crear
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



class StockListView(ListView):
    model = Celular
    template_name = 'stock.html'
    context_object_name = 'celulares'

    def get_queryset(self):
        queryset = Celular.objects.select_related(
            'id_modelo__id_marca', 'id_color', 'id_estado', 'id_moneda'

        ).prefetch_related( 'logcelular_set__id_user'
        ).all().order_by('-fecha_ingreso')
        
        filtro_serie = self.request.GET.get('numero_serie', '')
        filtro_modelo = self.request.GET.get('modelo', '')
        filtro_proveedor = self.request.GET.get('proveedor', '')
        fecha_desde = self.request.GET.get('fecha_desde', '')
        fecha_hasta = self.request.GET.get('fecha_hasta', '')
        
        if filtro_serie:
            queryset = queryset.filter(numero_serie__icontains=filtro_serie)
        if filtro_modelo:
            queryset = queryset.filter(id_modelo__id_marca__nombre__icontains=filtro_modelo)
        if filtro_proveedor:
            queryset = queryset.filter(proveedor__icontains=filtro_proveedor)
            
        # APLICAMOS LOS FILTROS DE FECHA
        if fecha_desde:
            queryset = queryset.filter(fecha_ingreso__date__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_ingreso__date__lte=fecha_hasta)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro_serie'] = self.request.GET.get('numero_serie', '')
        context['filtro_modelo'] = self.request.GET.get('modelo', '')
        context['filtro_proveedor'] = self.request.GET.get('proveedor', '')
        # ENVIAMOS LAS FECHAS AL HTML PARA MANTENERLAS SELECCIONADAS
        context['filtro_fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['filtro_fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        
        context['modelos'] = ModeloCelular.objects.select_related('id_marca').all()
        context['colores'] = ColorCelular.objects.all()
        context['estados'] = EstadoCelular.objects.all()
        context['monedas'] = Moneda.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        accion = request.POST.get('accion')
        
        if accion in ['crear', 'editar']:
            numero_serie = request.POST.get('numero_serie')
            numero_serie_original = request.POST.get('numero_serie_original') # util si editó la primary key
            
            # Obtener relaciones desde la BD
            modelo = get_object_or_404(ModeloCelular, id=request.POST.get('id_modelo'))
            color = get_object_or_404(ColorCelular, id=request.POST.get('id_color'))
            estado = get_object_or_404(EstadoCelular, id=request.POST.get('id_estado'))
            moneda = get_object_or_404(Moneda, id=request.POST.get('id_moneda'))
            
            precio_compra = request.POST.get('precio_compra')
            proveedor = request.POST.get('proveedor')
            observacion = request.POST.get('observacion')

            if accion == 'crear':
                celular = Celular.objects.create(
                    numero_serie=numero_serie,
                    id_modelo=modelo,
                    id_color=color,
                    id_estado=estado,
                    id_moneda=moneda,
                    precio_compra=precio_compra,
                    proveedor=proveedor,
                    observacion=observacion
                )
                
            elif accion == 'editar':
                # Buscamos usando el S/N original antes del cambio
                celular = get_object_or_404(Celular, numero_serie=numero_serie_original)
                
                # (Opcional) Capturar el estado anterior para dejar un log más rico
                estado_anterior = celular.id_estado.nombre
                
                # Actualizamos sus atributos
                celular.numero_serie = numero_serie 
                celular.id_modelo = modelo
                celular.id_color = color
                celular.id_estado = estado
                celular.id_moneda = moneda
                celular.precio_compra = precio_compra
                celular.proveedor = proveedor
                celular.observacion = observacion
                celular.save()

            datos_snapshot = {
                'numero_serie': numero_serie,
                'id_modelo': modelo.id,
                'modelo_nombre': f"{modelo.id_marca.nombre} - {modelo.capacidad}", # Guardamos nombres para facil lectura
                'id_color': color.id,
                'color_nombre': color.nombre,
                'id_estado': estado.id,
                'estado_nombre': estado.nombre,
                'id_moneda': moneda.id,
                'moneda_nombre': moneda.nombre,
                'precio_compra': precio_compra,
                'proveedor': proveedor,
                'observacion': observacion
            }
            json_snapshot = json.dumps(datos_snapshot)
            LogCelular.objects.create( id_celular=celular, id_user=request.user, value=json_snapshot )

        elif accion == 'eliminar':
            numero_serie = request.POST.get('numero_serie')
            celular = get_object_or_404(Celular, numero_serie=numero_serie)
            celular.delete()
            
        return redirect('stock')