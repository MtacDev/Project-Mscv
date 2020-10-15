from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
#AbstractBaseUser crear un usuario base o normal
# Create your models here.

'''class UsuarioManager(BaseUserManager): #Un manager son metodos que me permiten realizar cierto tipo de consulta especifica o recurrente
    def create_user(self,email,username,nombre,apellido,password=None):    #que va  ayudar a optimizar de cierta manera las cunsultas que se realizan en el sistema.
        if not email:
            raise ValueError('El usuario debe tener un correo electronico')

        usuario = self.model(
            username=username,
            email = self.normalize_email(email), #normalize_email normaliza el email para poder hacer ciertas validaciones en el
            nombre = nombre,
            apellido = apellido
        )

        usuario.set_password(password) #encripta la contraseña y la guarda en el mismo campo
        usuario.save()
        return usuario  
    
    def create_superuser(self,email,username,nombre,apellido,password):
        usuario = self.create_user(email,
            username = username,
            nombre = nombre,
            apellido= apellido
        )
        usuario.usuario_admin = True
        return usuario

class Comunidad(models.Model):

    cod_comunidad = models.BigAutoField(primary_key= True)
    nom_comunidad = models.CharField(null= False, max_length= 30)
    fecha_creacion = models.DateField(null= False)
    fecha_ter = models.DateField(blank=True,null=True)
    hubi_comuni = models.CharField(max_length= 30)
    coor_comuni = models.CharField(max_length= 60)
    def __str__(self):
        return self.nom_comunidad + " - " + self.hubi_comuni


class item(models.Model):
    
    cod_item = models.BigAutoField(primary_key=True)
    cod_comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    nom_item = models.CharField(max_length= 30)
    fecha_recib = models.DateField()
    img_item = models.ImageField()


class Usuario(AbstractBaseUser): #Actualizar modelo BD

    cod_per = models.BigAutoField(primary_key= True)
    cod_comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
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
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRE_FIELDS = ['email','nombre']
    
    def __str__(self):
        return f'{self.nombre},{self.apellido}'

    def has_perm(self,perm,obj = None): #Se define para que se pueda usar el modelo usuario en el administrador de django
        return True

    def has_module_perms (self,app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_admin #devuelve el usuario administrador


class Rol(models.Model):
    cod_rol = models.BigAutoField(primary_key= True)
    cod_per = models.ForeignKey(Usuario, on_delete= models.CASCADE)
    fecha_ele_rol = models.DateField(null= False)
    fecha_ter_rol = models.DateField()

class Evento(models.Model):
    cod_evento = models.BigAutoField(primary_key= True)
    cod_comunidad = models.ForeignKey(Comunidad, on_delete= models.CASCADE)
    nom_evento = models.CharField(max_length=30, null= False)
    hubi_eve = models.CharField(max_length= 60, null= False)
    coor_eve = models.IntegerField()
    fecha_crea_eve = models.DateField(auto_now=True) 
    fecha_reali_eve = models.DateField()
'''