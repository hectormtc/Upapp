# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid
from django.urls import reverse


class Address(models.Model):
    address = models.CharField(max_length=50)

    def __str__(self):
            return self.address


class Phone(models.Model):
    phone = models.CharField(
            max_length=15)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)

    def __str__(self):
            return self.phone + "-" + self.address.address


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
            if not email:
                    raise ValueError('Users must have an email address')

            elif not username:
                    raise ValueError('Users must have an username')

            user = self.model(
                    email=self.normalize_email(email),
                    username=username,
            )

            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, username, email, password):
            user = self.create_user(
                    email=email,
                    username=username,
                    password=password,
            )
            user.is_admin = True
            user.save(using=self._db)
            return user


class User(models.Model):

    #user = models.OneToOneField(User, on_delete=models.CASCADE,)
    username = models.CharField(max_length=30,
                                unique=True)
    name = models.CharField(max_length=30)
    slogan = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    bio = models.CharField(max_length=350)
    #profile_pic = models.ImageField(upload_to='Profile/Picture/')
    date = models.DateTimeField(auto_now_add=True,
                                null=True)
    email = models.EmailField(max_length=255,
                            unique=True)
    address = models.ManyToManyField(Address)
    phone = models.ManyToManyField(Phone)

    def __str__(self):
            return self.username


class Connection(models.Model):
    follower = models.ForeignKey(
                            User,
                            related_name='Cliente',
                            on_delete=models.CASCADE
                            )
    following = models.ForeignKey(
                            User,
                            related_name='Proveedor',
                            on_delete=models.CASCADE
                            )
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
            return "{} : {}".format(
                    self.follower.username,
                    self.following.username
                    )



class Categoria(models.Model):
    categoria = models.CharField(
                            max_length=50,
                            help_text="Tipo de categoria"
                            )

    def __str__(self):
                    return self.categoria


class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Encargado(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    rol = models.ForeignKey(
                            'Rol',
                            on_delete=models.SET_NULL,
                            null=True
                            )

    def __str__(self):
        return '{0} {1}'.format(
                                self.nombre,
                                self.apellido
                                )


class Inventario(models.Model):
    producto  = models.CharField(
                                'Producto',
                                max_length=200,
                                help_text="Nombre del producto"
                                )
    detalles  = models.CharField(
                                max_length=200,
                                help_text="Detalles sobre el producto",
                                blank=True
                                )
    cantidad  = models.PositiveIntegerField()
    precio    = models.PositiveIntegerField()
    categoria = models.ForeignKey(
                                'Categoria',
                                on_delete=models.SET_NULL,
                                null=True)

    def display_Categoria(self):
            return ', '.join([ self.categoria.categoria])
            display_Categoria.short_description = 'Categoria'

    def __str__(self):
            return '{0},  {1},Precio: {2}'.format(
                                            self.producto,
                                            self.detalles,
                                            self.precio
                                            )


class Articulo(models.Model):
    producto = models.ForeignKey(
                            Inventario,
                            on_delete=models.SET_NULL,
                            null=True
                            )
    cantidad  = models.PositiveIntegerField()

    def getProductName(self):
        return '%s %s' % (
                        self.producto.producto,
                        self.producto.detalles
                        )
    def getSubtotal(self):
            return int(
                    self.producto.precio * self.cantidad
                    )

    def getTotal(self):
            return sum(self.getSubtotal())

    def __str__(self):
            return '{0}, Cantidad: {1}, SubTotal: {2}'.format(
                                            self.producto,
                                            self.cantidad,
                                            self.getSubtotal()
                                            )


class Orden(models.Model):
    articulo = models.ForeignKey(
                        Articulo,
                        on_delete=models.SET_NULL,
                        null=True
                        )
    #articulo = models.ManyToManyField('Articulo')

    def __str__(self):
        return 'Orden: %s' % (
                            self.articulo.getProductName()
                            )


class InOrden(models.Model):
    in_orden = models.ManyToManyField('Orden')

    def __str__(self):
        return 'InOrden: %s' % (
                                self.in_orden
                                )


class Factura(models.Model):
    #factura = models.ForeignKey('Articulo', on_delete=models.SET_NULL, null=True)
    orden = models.ManyToManyField('InOrden')
    #orden = models.ForeignKey('Orden', on_delete=models.SET_NULL,null=True)
    cliente = models.ForeignKey(
                                'User',
                                on_delete=models.SET_NULL,
                                null=True
                                )
    encargado = models.ForeignKey(
                                'Encargado',
                                on_delete=models.SET_NULL,
                                null=True
                                )
    date_deliver = models.DateField(
                                    "Fecha de pedido",
                                    auto_now_add=True,
                                    null=True,
                                    help_text="Fecha en que se hizo el pedido"
                                    )
    date_receive = models.DateField(
                                    "Fecha de entrega",
                                    null=True,
                                    blank=True,
                                    help_text="Fecha en que se debe recibir el pedido"
                                    )
    PAGADO             = 'P'
    PENDIENTE          = 'PP'
    ENTREGADO          = 'E'
    ALQUILADO          = 'A'
    ALQUILER_PENDIENTE = 'AP'
    LOCAL              = 'L'
    ENTREGAR           = 'EE'

    PAY     = (
            (PAGADO, 'Pagado'),
            (PENDIENTE,'Pendiente Pago'),
            )
    RENT    =((ENTREGADO, 'Entregado'),
            (ALQUILADO, 'En Alquiler'),
            (ALQUILER_PENDIENTE,'Alquiler Pendiente'),
            )
    DELIVER = ((LOCAL, 'Local'),
            (ENTREGAR,'Entrega exterior'),
            )

    estado_de_pago  = models.CharField(max_length=2,choices=PAY, default=PAGADO)
    estado_de_renta = models.CharField(max_length=2, choices=RENT, default=ALQUILADO)
    tipo_de_entrega = models.CharField(max_length=2, choices=DELIVER, default=LOCAL)
    pago_pendiente  = models.PositiveIntegerField(blank=True)
    deposito        = models.PositiveIntegerField(blank=True)
    direccion       = models.TextField(help_text='Solo en caso de entrega exterior', blank=True)
    observacion     = models.TextField(help_text="Observacion Adicional", blank=True)


    class Meta:
                    ordering = ["date_deliver"]


    def __str__(self):
                    return '%s' % (
                                self.cliente.name
                                )
