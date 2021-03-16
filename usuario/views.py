from django.shortcuts import render
from django.http import HttpResponse 
import requests                                         
import json
from BDmscv.models import Persona, Comunidad, Reporte, AuthPago, Agradecimiento
from django.views.decorators.csrf import csrf_exempt
from usuario.config import Auth
from .forms import userInfo, ReporteAct, delReporte
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
import logging
import time
import datetime

# Create your views here.

logger = logging.getLogger(__name__)

def acclogin(request):
    obj = loginData(request)  
    
    if obj[1] == 'redirect':
         return redirect('/Bienvenido')
    else:
         return render(request, "accTemplate/login.html",{'form':obj[0],
                                                      'message':obj[1]})
    

def Bienvenido(request):

    try:
        imagen = Persona.objects.filter(cod_per = request.session['id']).values('imagen')
        request.session['imagen'] = imagen[0]['imagen']
        datainBienvenido(request)
        context ={
            'id': request.session['id'],
            'name': request.session['name'],
            'imagen':imagen[0]['imagen'],
            'staff':request.session['staff'], 
        }
        return render(request, "accTemplate/Bienvenido.html", context = context)
    except Exception as e:
        logger.error(e)
        return redirect('/login')
    
        

def Reporte_Act(request):

    try:
        obj = storageData(request)    
        usuarios = reporteApiUsuarios(request)
        context ={
            'id': request.session['id'],
            'name': request.session['name'],
            'imagen':request.session['imagen'],
            'staff':request.session['staff'],
            'form':obj[0],
            'msj':obj[1],
            'usuarios':usuarios, 
        }
        return render(request, "accTemplate/reporte.html",context = context)
    except Exception as e:
        logger.error(e)
        return redirect('/login')

def Modulo(request):

    try:
        context ={
            'id': request.session['id'],
            'name': request.session['name'],
            'imagen':request.session['imagen'],
            'staff':request.session['staff'], 
        }
        return render(request, "accTemplate/modulo.html", context = context)
    except Exception as e:
        logger.error(e)
        return redirect('/login')


def Historial(request):

        reporte = Reporte.objects.values_list('cod_rep',
                                                'nom_act',
                                                'fecha_act',
                                                'acta_reu',
                                                'nom_partici',
                                                'img_act', 
                                                'desc_act',
                                                'cant_valpos'
                                                ).order_by('fecha_act')
        por_confirm = listaReporte(request, reporte)
        historialData(request, por_confirm)
        ultimoReporte = Reporte.objects.all().values().last()
        ultper = splitData(request, ultimoReporte['nom_partici'])
        form = eliminarReporte(request)
        
        context ={
            'id': request.session['id'],
            'name': request.session['name'],
            'imagen':request.session['imagen'],
            'staff':request.session['staff'],
            'por_confirm': por_confirm, 
            'ultimo':ultimoReporte,
            'ultper':ultper,
            'form':form,
        }
        return render(request, "accTemplate/Historial.html", context = context)
          
    

                                                                
def loginData(request):
    """
    Se obtine los datos de sesion del unsuario que desea ingresar,
    se guardadn 2 datos relevantes el nombre y la id en 
    vaiables de session.    
    """
    obj = []
    auth = Auth()   
    url = "https://communities.cyclos.org/valpos/api/sessions"
    headers = {
        'Content-Type': 'application/json',   
        "X-Requested-With": "XMLHttpRequest"              
      }
    
    if request.method == 'POST':
        
        form = userInfo(request.POST)
        obj.append(form)
     
        if form.is_valid():
           
            user = form.cleaned_data.get('user')
            pas = form.cleaned_data.get('password')
            data = {
                    'user': user,
                    'password': pas,
                    'remoteAddress':'string',
                    'channel':'main',
                    'sessionTimeout':{
                    'amount':0,
                    'field':'days'},
                    }
            r = requests.post(url,data= json.dumps(data), headers = headers , auth = (auth.getUser(), 
                        auth.getPass()))
            if r.status_code == 200:
                 processData(request, r)               
                 obj.append('redirect')                           
            else:
                message = 'La contraseña o el nombre de usuario no son correctos'
                obj.append(message)
        else:
            form = form.errors   
    else:
        form = userInfo()
        obj.append(form)
        obj.append('')
             
    return obj

    
def processData(request, data):
    """
    Si la peticion a la API es correcta con status 200,
    en esta funcion se crean las variables de sesión
    y se guarda informacion de la persona en la tabla
    Persona.
    """
    parsedJsonObject = json.loads(data.text)
      
    request.session['id'] =  parsedJsonObject['user']['id']
    request.session['name'] =  parsedJsonObject['user']['display']
    
    try:
        imagen = parsedJsonObject['user']['image']['url']
    except KeyError:
        imagen = 'https://squashcolombia.org.co/wp-content/uploads/2020/05/checkmark.png'                                                                                                                                                                                                                                                       

    #si existe la persona, se obtienen sus datos, si no existe se levanta la exepcion
    try:
        Persona.objects.get(cod_per = parsedJsonObject['user']['id'])
    except Persona.DoesNotExist:
        crearPer =  Persona(cod_per = parsedJsonObject['user']['id'], 
                            nombre = parsedJsonObject['user']['display'],
                            imagen = imagen,
                            )  
        crearPer.save()
        if parsedJsonObject['group']['name'] != 'Network administrators':
            Persona.objects.update(cod_comunidad= parsedJsonObject['group']['id'])
            
           

 
def datainBienvenido(request):
    """
    Se obtienen los datos del usuario y si es administrador de red o de nodo 
    en la base de dato se actualiza el capo is_staff para, que en la vista de pueda
    hacer reportes de actividaes    
     """
    auth = Auth()
    r = requests.get('https://communities.cyclos.org/valpos/api/users/'+ request.session['id'] + '?fields=permissions.products%2C%20group',auth = (auth.getUser(), 
                                                                                                       auth.getPass()))
    parsedJsonObject = json.loads(r.text)

    staff = Persona.objects.filter(cod_per = request.session['id']).values('is_staff')
    try:
        admin = parsedJsonObject['permissions']['products']['individual'][0]['internalName']  
    except Exception as e:
        logger.error(e)
        admin = 'not admin'
    
    if staff[0]['is_staff'] == False:
        if admin == 'adminNodo' or parsedJsonObject['group']['name'] == 'Network administrators':
            Persona.objects.filter(cod_per = request.session['id']).update(is_staff = True)
            request.session['staff'] = True
        else:
            request.session['staff'] = False 
    else:
        request.session['staff'] = True    
            
def storageData(request):
    """
    La funcion obtiene los valores de los campos form
    y los guarda en la base de datos.
    """
    obj = []
    ingrepart = []
    if request.method == 'POST':
        
        form = ReporteAct(request.POST, request.FILES)

        if form.is_valid():
            cantAgradecimiento = form.cleaned_data.get('cantAgradecimiento')
            nomAct = form.cleaned_data.get('nomAct')
            fechaAct = form.cleaned_data.get('fechaAct')
            actareu = form.cleaned_data.get('actareu')
            ingrepart = request.POST.getlist('ingrepart')
            imgPart = form.cleaned_data.get('imgAct')
            descact = form.cleaned_data.get('descact')

            reporte = Reporte(nom_act = nomAct,
                                  cant_valpos = cantAgradecimiento, 
                                  fecha_act = fechaAct,
                                  cod_per = Persona.objects.get(cod_per = request.session['id']),
                                  acta_reu = actareu,
                                  nom_partici = ingrepart,
                                  img_act = imgPart,
                                  desc_act = descact)
            reporte.save()

            #Se crea el registro en AuthPago (BD) del reporte recien creado

            pkrep = Reporte.objects.values('cod_rep').last()
            authp = AuthPago(cod_rep = Reporte.objects.get(cod_rep = pkrep['cod_rep']))
            authp.save()

            #Mensaje de reporte coreecamente realizado
            msj = 'Reporte de '+ nomAct +' guardado' 
            obj.append(form)
            obj.append(msj)
        else:
            form = form.errors  
    else:
        form = ReporteAct()
        obj.append(form)
        obj.append('')

    return obj

def reporteApiUsuarios(request):
    """
    Api call para obtener los usuarios que estan registrados en Cyclos
    Losd resultados estan filtyrados desde la url, ver documentacion 
    de la Api de Cyclos.
    """
    auth = Auth()
    resulUsuarios = requests.get('https://communities.cyclos.org/valpos/api/users?groups=nodoValpos&includeGroup='+
                                        'true&includeGroupSet=true&orderBy=alphabeticallyAsc&roles=member&statuses=active&pageSize=5000',
                                         auth = (auth.getUser(), 
                                         auth.getPass()))
    parsedJsonObject = json.loads(resulUsuarios.text)
    
    return parsedJsonObject

def historialData(request, por_confirm):
    '''
    Se obtienen todos los reportes de actividades comunitarias
    '''
    hoy = time.strftime("%Y-%m-%d") 
    if request.method == 'POST':

        id_rep = request.POST['reporteid']    
        confirm = request.POST['confirmacion']
           
        if confirm == 'confirmacion1':
            
            AuthPago.objects.filter(cod_rep = id_rep).update(fecha_auth1 = str(hoy), per_auth1 = request.session['id']) 

        elif confirm == 'confirmacion2':

            AuthPago.objects.filter(cod_rep = id_rep).update(fecha_auth2 = str(hoy), per_auth2 = request.session['id'])
            cantValpos = Reporte.objects.filter(cod_rep = id_rep).values()
            realizarPago(request, por_confirm, cantValpos[0]['cant_valpos'])
            
    
    

        

def splitData(request, datos_personas):
    """
    Funcion para separa los nombres de los participantes de su username. 
    Datos traidos desded la base de datos.
    """
    data_names = []
    data_user = []
    participantes = []  
    
    #Como es un objeto convertido a string, de deben quitar los caracteres que sobran,
    #como los parentesis y las cmillas simples.
    
    names = datos_personas.replace("['", "")
    
    names = names.replace("']", "")
    names = names.replace(" '", "")
    names = names.replace("' ", "")
    names = names.replace("'", "")

    #se reemplazan las comas por guiones para despues separar los nombres del username 
    names = names.replace(",", "-")

    #se separa todo y se crea un objeto con los nombres de los participantes y su username 
    names = names.split("-") 

    #se itera sobre el objeto creado anteriomente y se separan nombres y username
    #en dos listas diferentes
    for items in names:

        if (names.index(items)+1) % 2 == 0:
            data_names.append(items)
        else:    
            data_user.append(items)

    participantes.append(data_names)
    participantes.append(data_user)
    return participantes

def listaReporte(request, reporte):
    """
    Se obtienen todos los reportes, se separan los que no estan confirmados
    y se guardan en otra lista par ser mostrados.
    """
    datos_sep = []
    por_confirm = []
    
    for elements in reporte:
        listarep = AuthPago.objects.filter(cod_rep = elements[0]).values() 
        datos_sep = splitData(request, elements[4])
        if listarep[0]['per_auth1'] == None:  

            elements += ('confirmacion1',)
            elements += (datos_sep[0],)
            elements += (datos_sep[1],)

            por_confirm.append(elements)

        if listarep[0]['per_auth2'] == None and listarep[0]['per_auth1'] != None: 
            
            elements += ('confirmacion2',)
            elements += (datos_sep[0],)
            elements += (datos_sep[1],)
            elements += (listarep[0]['per_auth1'],) 
            por_confirm.append(elements)
            
    return por_confirm

def realizarPago(request, users, cantValpos):
    auth = Auth()
    headers = {
        'Content-Type': 'application/json',   
        "X-Requested-With": "XMLHttpRequest"              
      }
    url = 'https://communities.cyclos.org/valpos/api/system/payments/preview'
    for elements in users:
        hoy = str(datetime.datetime.utcnow().replace(microsecond=100).isoformat())
        
        for username, name in zip(elements[10], elements[9]):
            data = {
                    "amount": cantValpos,
                    "description": "Agradecimiento por la participación de la  actividad comunitaria: "+ elements[1],
                    "currency": "∀alpos",
                    "type": "organization.pagoUsu",
                    "customValues": {                      
                    },
                    "subject": username,
                    "fromName": "organization",
                    "toName": name,
                    "installmentsCount": 0,
                    "firstInstallmentDate": hoy + "Z",
                    "installments": [
                        {
                        "dueDate": hoy + "Z",
                        "amount": cantValpos
                        }
                    ],
                    "occurrencesCount": 0,
                    "firstOccurrenceDate": hoy + "Z",
                    "occurrenceInterval": {
                        "amount": 1,
                        "field": "days"
                    },
                    "nfcChallence": "string",
                    "scheduling": "direct"
                    }    
            r = requests.post(url,data= json.dumps(data), headers = headers , auth = (auth.getUser(), 
                                                                                      auth.getPass()))
            if r.status_code == 200:
                parsedobj = json.loads(r.text)
                print(r.status_code)
                print(users[0][1])   
                #storagePago(request, parsedobj, hoy)
            else:
                print('Coneccion error')    
            
def storagePago(request, objpago, hoy):
    """
    Se registra el pago o "Agradecimento" entregado al participante de una 
    actividad comunitaria.
    """

    pago = Agradecimiento(cod_per = objpago['to']['user']['id'],
                        nom_per_agre = objpago['to']['user']['display'], 
                        from_cuenta = objpago['from']['type']['name'],
                        fecha_agre = hoy,
                        descrip_pago = objpago['description'],
                        amount = objpago['amount'],
                        id_transacc = objpago['display'],)
    pago.save()
    
def eliminarReporte(request):
    """
    Se obtiene la id del reporte y luego se elimina
    """
    if request.method == 'GET': 
        form = delReporte(request.GET)
        if form.is_valid():

            elmrepo = form.cleaned_data.get('elmrepo')  
            Reporte.objects.filter(cod_rep = elmrepo).delete()
                                                           
        else:
            form = form.errors 
    else:
        form = delReporte()
    return form                            