
"""MSCValpo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Template import views as template
from usuario import views as usuario

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',template.home, name = 'home'),
    path('reglamento/',template.reglamento, name = 'reglamento'),
    path('login/',usuario.acclogin, name = 'login'),
    path('Bienvenido/',usuario.Bienvenido, name = 'Bienvenido'),
    path('reporte/',usuario.Reporte_Act, name = 'reporte'),
    path('modulo/',usuario.Modulo, name = 'modulo'),
    path('Historial/',usuario.Historial, name = 'Historial'),
    path('graphs/',usuario.graphs, name = 'graphs'),
    path('admin/', admin.site.urls)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
