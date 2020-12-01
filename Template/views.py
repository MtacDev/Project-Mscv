from django.shortcuts import render, HttpResponse #(este metodo nos permite contestar a una peticion, devolviendo un codigo de progamacion)
import requests                                                  #(render devuelve un plantilla html renderizada)
import json
from Template.config import Auth
from BDmscv.models import Comunidad, data
from django.db import IntegrityError

 
# Create your views here.
def home(request):    
    
    viewg = tiposGroups(request)
    cantusu = cantUsuarios(requests)
    ctranc = cantTransacc(request)
    dato = data(cant_usuarios = cantusu, 
                cant_nodos =  viewg[1], 
                cant_transacc = int(ctranc[0]),
                sum_valpos = float(ctranc[1]))
    dato.save()
    
    return render(request, "paginas/home.html",{'viewgrupos':viewg[0], 
                                                'cantg':viewg[1], 
                                                'cantusu':cantusu, 
                                                'canttr':ctranc[0], 
                                                'sumtr':ctranc[1]})

def tiposGroups(request):
    #obtiene la lista de la Api se transforma en objeto de json y se extrae los datos necesarios
    auth = Auth()
    grupos =  []
    viewg = []
    countnodos = 0
    r = requests.get('https://communities.cyclos.org/valpos/api/users/data-for-search?fields=&fromMenu=false', 
                        auth=(auth.getUser(), 
                        auth.getPass()))
                        
    if r.status_code == 200:
        #Transformo r en un objeto de python    
        parsedJsonObject = json.loads(r.text)
        resultObject = parsedJsonObject['groups']
        #separo y obtengo solo los grupos tipo memeberGroup
        for tipogroup in resultObject: 
            if tipogroup['kind'] == 'memberGroup' :
                grupos.append(tipogroup)     
                countnodos = countnodos + 1
        #Busco en la BD si la id del grupo esta agregada, si no esta se agrega
                
        for ingrupos in grupos:
            #Aqui si el objeto no existe, se devuelve una tupla donde el objeto se guarda en insert
            # y un boolean se guarda en creado, True si fue creado el objeto. 
            try:
                insert, creado = Comunidad.objects.get_or_create(cod_comunidad = ingrupos['id'],
                                            nom_comunidad = ingrupos['name'], 
                                            descrip = "Activar y Agregar Descripción",
                                            hubi_comuni = 'Activar',
                                            coor_comuni='0')
                if creado:                     
                    insert.save() 
            except IntegrityError:
                #Si hay un cambio de nombre que no provenga desde cyclos, habra un error de integridad
                # y entrara aqui, aca obtendre el qreryset con la id del del campo cod_comunidad.
                #luego comparare el nombre del grupo de la BD de esa fila con el nombre del grupo que traigo desde cyclos y se cambia
                #por el de cyclos.
                cambionom = Comunidad.objects.get(cod_comunidad = ingrupos['id'])
                #print(cambionom.nom_comunidad)
                if cambionom.nom_comunidad != ingrupos['name']:
                    cambionom.nom_comunidad = ingrupos['name']
                    cambionom.save()
                                
    else:
        f'No se pudo hacer hacer la conexión code :{r.status_code}'
    #Grupos guardados de forma random en la lista
    viewg.append(Comunidad.objects.order_by('?')[:8])
    viewg.append(countnodos)
    return  viewg

def cantUsuarios(requests):
    auth = Auth()
    countUsu = 0
    r = requests.get('https://communities.cyclos.org/valpos/api/users?roles=&statuses=', 
                        auth=(auth.getUser(), 
                        auth.getPass()))
    parsedJsonObject = json.loads(r.text)
    for display in parsedJsonObject:
        countUsu=countUsu + 1
    return countUsu        
            
def cantTransacc(request):
    auth = Auth() 
    ctranc = []     
    r = requests.get('https://communities.cyclos.org/valpos/api/transfers/summary?kinds=&skipTotalCount=false&transferKinds=', 
                        auth=(auth.getUser(), 
                        auth.getPass()))
    parsedJsonObject = json.loads(r.text)
    ctranc.append(parsedJsonObject[0]['count'])
    ctranc.append(parsedJsonObject[0]['sum'])
    return ctranc

def reglamento(request):
    return render(request, "paginas/reglamento.html")