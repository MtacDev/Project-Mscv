from django.db import models


class Comunidad(models.Model):

    cod_comunidad = models.CharField(primary_key= True, max_length= 50)
    nom_comunidad = models.CharField('Nombre de la comunidad',null= False, max_length= 100)
    descrip = models.TextField('Descripcion', blank=True, null=True, max_length= 500)
    fecha_creacion = models.DateField('Fecha de creacion',blank=True, null=True, auto_now_add=True)
    hubi_comuni = models.CharField('Hubicacion de la Comunidad ',max_length= 100, blank=True, null=True)
    coor_comuni = models.CharField('Coordenadas para google maps',max_length= 100, blank=True, null=True)
    image_co = models.ImageField('Imagen de referencia',default = 'static/img/Comunidad-online.png',upload_to = 'static/img' ,blank=True, null=True)
    is_active = models.BooleanField('¿Esta activo?', default=False)

    def __str__(self):
        return self.nom_comunidad
        
class item(models.Model):
    
    cod_item = models.BigAutoField(primary_key=True)
    cod_comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, verbose_name="Codigo de la Comunidad")
    nom_item = models.CharField('Nombre del item',max_length= 100)
    fecha_recib = models.DateField('Fecha cuando se recibio el item',blank=True,null=True)
    img_item = models.ImageField('Imagen del item',blank=True,null=True)

class Usuario(models.Model): #Actualizar modelo BD

    cod_per = models.BigAutoField(primary_key= True)
    cod_comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE,verbose_name="Codigo de la Comunidad")
    username= models.CharField( 'Nombre de Usuario',unique=True,max_length=100)
    email = models.EmailField('Correo Electronico', max_length=254, unique=True)
    Rut = models.CharField(null= False,unique=True,max_length=100)
    nombre = models.CharField('Nombres',max_length= 200,blank=True,null=True)
    apellido = models.CharField('Apellidos', max_length=200,blank=True,null=True)
    imgen = models.ImageField('Imagen de Perfil', upload_to='perfil/', max_length=200,blank=True,null=True )
    fecha_nac = models.DateField('Fecha de Nacimiento',null= False)
    direccion = models.CharField('Direccion',max_length= 200,blank=True,null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_admin = models.BooleanField(default=False)

class data(models.Model):
    id_data = models.BigAutoField(primary_key=True)
    fecha_add = models.DateField(auto_now_add=True)
    cant_usuarios = models.IntegerField(max_length=500)  
    cant_nodos = models.IntegerField(max_length=500)
    cant_transacc = models.IntegerField(max_length=500)
    sum_valpos = models.IntegerField(max_length=500)





