from django.db import models
from s3direct.fields import S3DirectField
from MSCValpo.storage_backends import PublicMediaStorage, PublicImagesStorage, PublicFilesStorage


class Comunidad(models.Model):
    cod_comunidad = models.CharField(primary_key= True, max_length= 50)
    nom_comunidad = models.CharField('Nombre de la comunidad',null= False, max_length= 100)
    descrip = models.TextField('Descripcion', blank=True, null=True, max_length= 500)
    fecha_creacion = models.DateField('Fecha de creacion',blank=True, null=True, auto_now_add=True)
    hubi_comuni = models.CharField('Hubicacion de la Comunidad ',max_length= 100, blank=True, null=True)
    coor_comuni = models.CharField('Coordenadas para google maps',max_length= 100, blank=True, null=True)
    image_co = models.CharField('Imagen de referencia',max_length = 500,default = 'static/img/Comunidad-online.png',blank=True, null=True)
    is_active = models.BooleanField('¿Esta activo?', default=False)

    def __str__(self):
        return self.nom_comunidad
        

class Persona(models.Model): 
    cod_per = models.CharField(primary_key= True, max_length= 100)
    cod_comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, blank= True, null= True)
    nombre = models.CharField('Nombres',max_length= 200,blank=True,null=True)
    imagen = models.CharField('Imagen de Perfil', max_length=200,blank=True, )
    fecha_nac = models.DateField('Fecha de Nacimiento',null= True)
    direccion = models.CharField('Direccion',max_length= 200,blank=True,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre

class Reporte(models.Model):
    cod_rep = models.BigAutoField(primary_key= True)
    cant_valpos = models.IntegerField('Cantidad de Valpos',blank=True,null=True)
    fecha_act= models.DateField('Fecha de realizacion de la actividad comunitaria',blank=True,null=True)
    nom_act = models.CharField('Nombre de la actividad', max_length= 500, blank=True,null=True)
    nom_partici = models.CharField('Participantes',max_length= 1000)
    desc_act = models.CharField('Descripción de la Actividad',max_length= 1000)
    cod_per = models.ForeignKey(Persona, on_delete=models.CASCADE, blank= True, null= True, verbose_name= 'Nombre de quien hizo el reporte')
    report_image = models.FileField(storage=PublicMediaStorage())
    report_files = models.FileField(storage=PublicMediaStorage())
    def __str__(self):
        titulo = str(self.cod_rep) + ' | ' + str(self.fecha_act)  
        return titulo 


class Modulo_Comp(models.Model):
    cod_mo_com = models.BigAutoField(primary_key= True)
    cod_per = models.ForeignKey(Persona, on_delete=models.CASCADE)
    nom_mod = models.CharField('Nombre del Modulo',max_length= 200,blank=True,null=True)
    fecha_ini = models.DateField('Fecha de Inicio',null= True)
    fecha_ter = models.DateField('Fecha de Termino',null= True)
    Categoria = models.CharField('Categoria',max_length= 200,blank=True,null=True)
    recompensa = models.FloatField('Recompensa pagada')

class data(models.Model):
    id_data = models.BigAutoField(primary_key=True)
    fecha_add = models.CharField('Fecha de registro', max_length=50)
    cant_usuarios = models.IntegerField()  
    cant_nodos = models.IntegerField()
    cant_transacc = models.IntegerField()
    sum_valpos = models.IntegerField()

class AuthPago(models.Model):
    cod_authpay = models.BigAutoField(primary_key = True, )
    cod_rep = models.ForeignKey(Reporte, on_delete=models.CASCADE, blank= True, null= True)
    fecha_auth1 = models.DateField('Fecha de la primera autorizacion',blank=True,null=True)
    fecha_auth2 = models.DateField('Fecha de la segunda autorizacion',blank=True,null=True)
    per_auth1 = models.CharField('Id de la persona que autoriza 1', max_length=50,blank=True,null=True)
    per_auth2 = models.CharField('Id de la persona que autoriza 2', max_length=50,blank=True,null=True)
   
class Agradecimiento(models.Model):
    cod_recom = models.BigAutoField(primary_key = True)
    cod_per = models.CharField("Codigo de la Persona", max_length=50)
    nom_per_agre = models.CharField("Nombre de quien recibe el agradecimiento", max_length=100)
    from_cuenta = models.CharField("Cuenta proveniente", max_length=50, blank= True, null= True)
    fecha_agre = models.CharField("Fecha de agradecimiento", max_length=50, blank= True, null= True)
    descrip_pago = models.CharField("Descripcion del pago", max_length=100,blank= True, null= True)
    amount = models.CharField("Cantidad depositada", max_length=50, blank= True, null= True)
    id_transacc = models.CharField("Id de la Transaccion", max_length=100, blank= True, null= True)



        

