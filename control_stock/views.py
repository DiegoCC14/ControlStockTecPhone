from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Cliente, Celular, ModeloCelular, ColorCelular, EstadoCelular, Moneda
from .models import LogCelular, VentaCelular, ReservaCelular, EstadoReserva

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
            queryset = queryset.filter(id_modelo__nombre__icontains=filtro_modelo)
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
            numero_serie_original = request.POST.get('numero_serie_original')
            
            modelo = get_object_or_404(ModeloCelular, id=request.POST.get('id_modelo'))
            color = get_object_or_404(ColorCelular, id=request.POST.get('id_color'))
            moneda = get_object_or_404(Moneda, id=request.POST.get('id_moneda'))
            
            precio_compra = request.POST.get('precio_compra')
            proveedor = request.POST.get('proveedor')
            observacion = request.POST.get('observacion')

            # --- SEGURIDAD: SIEMPRE "Disponible" ---
            estado_disponible, _ = EstadoCelular.objects.get_or_create(nombre='Disponible')

            if accion == 'crear':
                celular = Celular.objects.create(
                    numero_serie=numero_serie,
                    id_modelo=modelo,
                    id_color=color,
                    id_estado=estado_disponible, # Forzado
                    id_moneda=moneda,
                    precio_compra=precio_compra,
                    proveedor=proveedor,
                    observacion=observacion
                )
                
            elif accion == 'editar':
                celular = get_object_or_404(Celular, numero_serie=numero_serie_original)
                
                celular.numero_serie = numero_serie 
                celular.id_modelo = modelo
                celular.id_color = color
                # celular.id_estado = ... (NO TOCAMOS EL ESTADO AQUÍ)
                celular.id_moneda = moneda
                celular.precio_compra = precio_compra
                celular.proveedor = proveedor
                celular.observacion = observacion
                celular.save()

            # Registro del Log
            datos_snapshot = {
                'evento': "CREACION" if accion == 'crear' else "MODIFICACION",
                'numero_serie': celular.numero_serie,
                'id_modelo': modelo.id,
                'modelo_nombre': f"{modelo.id_marca.nombre} - {modelo.capacidad}",
                'id_color': color.id,
                'color_nombre': color.nombre,
                'id_estado': celular.id_estado.id, # Registramos el estado actual
                'estado_nombre': celular.id_estado.nombre,
                'id_moneda': moneda.id,
                'moneda_nombre': moneda.nombre,
                'precio_compra': precio_compra,
                'proveedor': proveedor,
                'observacion': observacion
            }
            json_snapshot = json.dumps(datos_snapshot)
            LogCelular.objects.create(id_celular=celular, id_user=request.user, value=json_snapshot)

            return redirect('stock')



class VentasListView(ListView):
    model = VentaCelular
    template_name = 'ventas.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        queryset = VentaCelular.objects.select_related(
            'id_celular', 'id_cliente', 'id_vendedor', 'id_moneda'
        ).prefetch_related(
            'id_celular__logcelular_set__id_user'
        ).all().order_by('-fecha_venta')
        
        filtro_cliente = self.request.GET.get('cliente', '')
        filtro_serie = self.request.GET.get('numero_serie', '')
        filtro_vendedor = self.request.GET.get('vendedor', '')
        fecha_desde = self.request.GET.get('fecha_desde', '')
        fecha_hasta = self.request.GET.get('fecha_hasta', '')
        
        if filtro_cliente:
            queryset = queryset.filter(
                Q(id_cliente__dni__icontains=filtro_cliente) | 
                Q(id_cliente__nombre__icontains=filtro_cliente) | 
                Q(id_cliente__apellido__icontains=filtro_cliente)
            )
        if filtro_serie:
            queryset = queryset.filter(id_celular__numero_serie__icontains=filtro_serie)
        if filtro_vendedor:
            queryset = queryset.filter(id_vendedor__username__icontains=filtro_vendedor)
            
        if fecha_desde:
            queryset = queryset.filter(fecha_venta__date__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_venta__date__lte=fecha_hasta)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['filtro_cliente'] = self.request.GET.get('cliente', '')
        context['filtro_serie'] = self.request.GET.get('numero_serie', '')
        context['filtro_vendedor'] = self.request.GET.get('vendedor', '')
        context['filtro_fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['filtro_fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        
        context['clientes'] = Cliente.objects.all()
        context['monedas'] = Moneda.objects.all()
        
        # FILTRO ESTRICTO: Solo trae celulares cuyo estado sea exactamente "Disponible"
        context['celulares_disponibles'] = Celular.objects.filter(
            id_estado__nombre__iexact='Disponible'
        ).select_related('id_modelo__id_marca', 'id_color')
            
        return context

    def post(self, request, *args, **kwargs):
        accion = request.POST.get('accion')
        
        if accion in ['crear', 'editar']:
            celular = get_object_or_404(Celular, numero_serie=request.POST.get('id_celular'))
            cliente = get_object_or_404(Cliente, dni=request.POST.get('dni'))
            moneda = get_object_or_404(Moneda, id=request.POST.get('id_moneda'))
            
            precio_venta = request.POST.get('precio_venta')
            observaciones = request.POST.get('observaciones')

            if accion == 'crear':
                # VALIDACION DE SEGURIDAD (Backend)
                if celular.id_estado.nombre.lower() != 'disponible':
                    return redirect('ventas')
                
                # AUTOMATIZACION: El vendedor es el usuario que esta usando el sistema
                vendedor = request.user
                
                VentaCelular.objects.create(
                    id_celular=celular,
                    id_cliente=cliente,
                    id_vendedor=vendedor,
                    id_moneda=moneda,
                    precio_venta=precio_venta,
                    observaciones=observaciones
                )
                
                estado_vendido, created = EstadoCelular.objects.get_or_create(nombre='Vendido')
                celular.id_estado = estado_vendido
                celular.save()
                
            elif accion == 'editar':
                venta_id = request.POST.get('id_venta')
                venta = get_object_or_404(VentaCelular, id=venta_id)
                
                venta.id_cliente = cliente
                venta.id_moneda = moneda
                # No actualizamos el vendedor en la edicion por seguridad
                venta.precio_venta = precio_venta
                venta.observaciones = observaciones
                venta.save()
                
                vendedor = venta.id_vendedor # Rescatamos el vendedor original para el log

            evento_nombre = "VENTA REGISTRADA" if accion == 'crear' else "VENTA MODIFICADA"
            
            datos_snapshot = {
                'evento': evento_nombre,
                'numero_serie': celular.numero_serie,
                'cliente': f"{cliente.nombre} {cliente.apellido}",
                'dni_cliente': str(cliente.dni),
                'vendedor': vendedor.username,
                'precio_venta': precio_venta,
                'moneda': moneda.nombre,
                'observacion_venta': observaciones,
                'estado_actual_celular': celular.id_estado.nombre
            }
            
            json_snapshot = json.dumps(datos_snapshot)
            LogCelular.objects.create(id_celular=celular, id_user=request.user, value=json_snapshot)

        elif accion == 'eliminar':
            venta_id = request.POST.get('id_venta')
            serie_celular = request.POST.get('numero_serie')
            
            venta = get_object_or_404(VentaCelular, id=venta_id)
            venta.delete()
            
            # REVERTIMOS EL ESTADO DEL CELULAR A DISPONIBLE
            celular = get_object_or_404(Celular, numero_serie=serie_celular)
            
            estado_disponible = EstadoCelular.objects.filter(nombre__icontains='Disponible').first()
            
            if estado_disponible:
                celular.id_estado = estado_disponible
                celular.save()
            
            datos_snapshot = {
                'evento': "VENTA ANULADA",
                'numero_serie': celular.numero_serie,
                'detalle': "La venta fue eliminada. El dispositivo retorna a stock.",
                'estado_actual_celular': celular.id_estado.nombre if estado_disponible else "Desconocido"
            }
            json_snapshot = json.dumps(datos_snapshot)
            LogCelular.objects.create(id_celular=celular, id_user=request.user, value=json_snapshot)
            
        return redirect('ventas')



class ReservasListView(ListView):
    model = ReservaCelular
    template_name = 'reserva.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        queryset = ReservaCelular.objects.select_related(
            'id_celular', 'id_cliente', 'id_vendedor', 'id_estado_reserva', 'id_moneda'
        ).prefetch_related(
            'id_celular__logcelular_set__id_user'
        ).all().order_by('-fecha_reserva')
        
        filtro_cliente = self.request.GET.get('cliente', '')
        filtro_serie = self.request.GET.get('numero_serie', '')
        filtro_vendedor = self.request.GET.get('vendedor', '')
        fecha_desde = self.request.GET.get('fecha_desde', '')
        fecha_hasta = self.request.GET.get('fecha_hasta', '')
        
        if filtro_cliente:
            queryset = queryset.filter(
                Q(id_cliente__dni__icontains=filtro_cliente) | 
                Q(id_cliente__nombre__icontains=filtro_cliente) | 
                Q(id_cliente__apellido__icontains=filtro_cliente)
            )
        if filtro_serie:
            queryset = queryset.filter(id_celular__numero_serie__icontains=filtro_serie)
        if filtro_vendedor:
            queryset = queryset.filter(id_vendedor__username__icontains=filtro_vendedor)
            
        if fecha_desde:
            queryset = queryset.filter(fecha_reserva__date__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_reserva__date__lte=fecha_hasta)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['filtro_cliente'] = self.request.GET.get('cliente', '')
        context['filtro_serie'] = self.request.GET.get('numero_serie', '')
        context['filtro_vendedor'] = self.request.GET.get('vendedor', '')
        context['filtro_fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['filtro_fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        
        context['clientes'] = Cliente.objects.all()
        context['estados_reserva'] = EstadoReserva.objects.all()
        context['monedas'] = Moneda.objects.all() # <- NUEVO
        
        context['celulares_disponibles'] = Celular.objects.filter(
            id_estado__nombre__iexact='Disponible'
        ).select_related('id_modelo__id_marca', 'id_color')
            
        return context

    def post(self, request, *args, **kwargs):
        accion = request.POST.get('accion')
        
        if accion in ['crear', 'editar']:
            celular = get_object_or_404(Celular, numero_serie=request.POST.get('id_celular'))
            cliente = get_object_or_404(Cliente, dni=request.POST.get('dni'))
            estado_reserva = get_object_or_404(EstadoReserva, id=request.POST.get('id_estado_reserva'))
            moneda = get_object_or_404(Moneda, id=request.POST.get('id_moneda')) # <- NUEVO
            
            precio_venta = request.POST.get('precio_venta') # <- NUEVO
            fecha_entrega = request.POST.get('fecha_entrega') or None
            observaciones = request.POST.get('observaciones')
            
            es_entregado = estado_reserva.nombre.lower() in ['entregado', 'entregada']

            if accion == 'crear':
                if celular.id_estado.nombre.lower() != 'disponible':
                    return redirect('reserva')
                
                vendedor = request.user
                
                if es_entregado:
                    # Crea Venta Directa con el precio pactado en el formulario
                    VentaCelular.objects.create(
                        id_celular=celular,
                        id_cliente=cliente,
                        id_vendedor=vendedor,
                        id_moneda=moneda,
                        precio_venta=precio_venta,
                        observaciones=f"Venta directa desde Reserva. {observaciones}"
                    )
                    estado_vendido, _ = EstadoCelular.objects.get_or_create(nombre='Vendido')
                    celular.id_estado = estado_vendido
                    celular.save()
                    evento_nombre = "RESERVA ENTREGADA -> AUTO VENTA REGISTRADA"
                else:
                    ReservaCelular.objects.create(
                        id_celular=celular,
                        id_cliente=cliente,
                        id_vendedor=vendedor,
                        id_estado_reserva=estado_reserva,
                        id_moneda=moneda,
                        precio_venta=precio_venta,
                        fecha_entrega=fecha_entrega,
                        observaciones=observaciones
                    )
                    estado_reservado_cel, _ = EstadoCelular.objects.get_or_create(nombre='Reservado')
                    celular.id_estado = estado_reservado_cel
                    celular.save()
                    evento_nombre = "RESERVA CREADA"
                
            elif accion == 'editar':
                reserva_id = request.POST.get('id_reserva')
                reserva = get_object_or_404(ReservaCelular, id=reserva_id)
                vendedor = reserva.id_vendedor
                
                if es_entregado:
                    # Transicion a Venta con los datos exactos pactados
                    VentaCelular.objects.create(
                        id_celular=celular,
                        id_cliente=cliente,
                        id_vendedor=vendedor,
                        id_moneda=moneda,
                        precio_venta=precio_venta,
                        observaciones=f"Reserva finalizada. {observaciones}"
                    )
                    reserva.delete()
                    estado_vendido, _ = EstadoCelular.objects.get_or_create(nombre='Vendido')
                    celular.id_estado = estado_vendido
                    celular.save()
                    evento_nombre = "RESERVA FINALIZADA -> AUTO VENTA REGISTRADA"
                else:
                    reserva.id_cliente = cliente
                    reserva.id_estado_reserva = estado_reserva
                    reserva.id_moneda = moneda
                    reserva.precio_venta = precio_venta
                    reserva.fecha_entrega = fecha_entrega
                    reserva.observaciones = observaciones
                    reserva.save()
                    evento_nombre = "RESERVA MODIFICADA"

            datos_snapshot = {
                'evento': evento_nombre,
                'numero_serie': celular.numero_serie,
                'cliente': f"{cliente.nombre} {cliente.apellido}",
                'estado_reserva': estado_reserva.nombre,
                'vendedor': vendedor.username,
                'precio_pactado': f"{precio_venta} {moneda.nombre}",
                'fecha_entrega_pactada': str(fecha_entrega) if fecha_entrega else 'Sin definir',
                'observaciones': observaciones,
                'estado_actual_celular': celular.id_estado.nombre
            }
            json_snapshot = json.dumps(datos_snapshot)
            LogCelular.objects.create(id_celular=celular, id_user=request.user, value=json_snapshot)

        elif accion == 'eliminar':
            reserva_id = request.POST.get('id_reserva')
            serie_celular = request.POST.get('numero_serie')
            
            reserva = get_object_or_404(ReservaCelular, id=reserva_id)
            reserva.delete()
            
            celular = get_object_or_404(Celular, numero_serie=serie_celular)
            estado_disponible, _ = EstadoCelular.objects.get_or_create(nombre='Disponible')
            celular.id_estado = estado_disponible
            celular.save()
            
            datos_snapshot = {
                'evento': "RESERVA ANULADA",
                'numero_serie': celular.numero_serie,
                'detalle': "La reserva fue cancelada y el dispositivo volvió a stock.",
                'estado_actual_celular': celular.id_estado.nombre
            }
            json_snapshot = json.dumps(datos_snapshot)
            LogCelular.objects.create(id_celular=celular, id_user=request.user, value=json_snapshot)
            
        return redirect('reserva')