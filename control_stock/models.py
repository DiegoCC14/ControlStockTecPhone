from django.db import models
from django.contrib.auth.models import User

# --- Modelos Auxiliares y Catalogos ---

class Moneda(models.Model):
    nombre = models.CharField(max_length=50, help_text="Ej: USD")
    def __str__(self):
        return self.nombre

class EstadoCelular(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class ColorCelular(models.Model):
    nombre = models.CharField(max_length=300)
    def __str__(self):
        return self.nombre

class MarcaModelo(models.Model):
    nombre = models.CharField(max_length=300)
    def __str__(self):
        return self.nombre

class ModeloCelular(models.Model):
    id_marca = models.ForeignKey(MarcaModelo, on_delete=models.CASCADE, db_column='id_marca')
    capacidad = models.IntegerField(help_text="Capacidad en GB")
    def __str__(self):
        return f"Modelo ID {self.id} ({self.capacidad}GB)"

class EstadoReserva(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre


# --- Entidades Principales ---

class Celular(models.Model):
    # Clave primaria manual ingresada por el usuario
    numero_serie = models.CharField(max_length=200, primary_key=True)
    
    # Claves foraneas con el nombre exacto e id_ del diagrama
    id_modelo = models.ForeignKey(ModeloCelular, on_delete=models.PROTECT, db_column='id_modelo')
    id_color = models.ForeignKey(ColorCelular, on_delete=models.PROTECT, db_column='id_color')
    id_estado = models.ForeignKey(EstadoCelular, on_delete=models.PROTECT, db_column='id_estado')
    id_moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, db_column='id_moneda')
    
    # Fecha generada automaticamente en la creacion
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    
    precio_compra = models.FloatField()
    proveedor = models.CharField(max_length=200)
    observacion = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return f"S/N: {self.numero_serie}"

class LogCelular(models.Model):
    dni = models.AutoField(primary_key=True, db_column='dni')
    id_celular = models.ForeignKey(Celular, on_delete=models.CASCADE, db_column='id_celular')
    id_user = models.ForeignKey(User, on_delete=models.PROTECT, db_column='id_user', null=True, blank=True)
    value = models.CharField(max_length=4000)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Log {self.dni} - Celular: {self.id_celular_id}"

class Cliente(models.Model):
    dni = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"


# --- Entidades Transaccionales ---

class ReservaCelular(models.Model):
    id_celular = models.ForeignKey(Celular, on_delete=models.CASCADE, db_column='id_celular')
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_vendedor = models.ForeignKey(User, on_delete=models.PROTECT, db_column='id_vendedor')
    id_estado_reserva = models.ForeignKey(EstadoReserva, on_delete=models.PROTECT, db_column='id_estado_reserva')
    
    # --- NUEVOS CAMPOS ---
    precio_venta = models.FloatField(null=True, blank=True)
    id_moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, db_column='id_moneda', null=True, blank=True)
    
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    observaciones = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return f"Reserva {self.id} - Celular: {self.id_celular_id}"

class VentaCelular(models.Model):
    id_celular = models.ForeignKey(Celular, on_delete=models.CASCADE, db_column='id_celular')
    id_cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, db_column='id_cliente')
    id_vendedor = models.ForeignKey(User, on_delete=models.PROTECT, db_column='id_vendedor')
    id_moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, db_column='id_moneda')
    
    precio_venta = models.FloatField()
    observaciones = models.CharField(max_length=2000, blank=True, null=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta {self.id} - Celular: {self.id_celular_id}"