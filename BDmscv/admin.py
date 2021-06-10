from django.contrib import admin
from BDmscv.models import Comunidad, Persona, Reporte, Modulo_Comp, AuthPago, data, Agradecimiento

# Register your models here.
admin.site.register(Comunidad)
admin.site.register(Persona)
admin.site.register(Reporte)
admin.site.register(Modulo_Comp)
admin.site.register(AuthPago)
admin.site.register(data)
admin.site.register(Agradecimiento)

