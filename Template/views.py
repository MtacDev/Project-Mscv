from django.shortcuts import render, HttpResponse #(este metodo nos permite contestar a una peticion, devolviendo un codigo de progamacion)
from Template.config import Auth
from BDmscv.models import Comunidad, data
from django.db import IntegrityError
import time
import requests                                                  
import json

# Create your views here.
def home(request):    
    
    viewg = tiposGroups(request)
    cantusu = cantUsuarios(requests)
    ctranc = cantTransacc(request)
    """
    hoy = time.strftime("%Y-%m-%d") 
    dato = data(fecha_add = hoy,
                cant_usuarios = cantusu, 
                cant_nodos =  viewg[1], 
                cant_transacc = int(ctranc[0]),
                sum_valpos = float(ctranc[1]))
    dato.save()
    """
    
    return render(request, "paginas/home.html",{'viewgrupos':viewg[0], 
                                                'cantg':viewg[1], 
                                                'cantusu':cantusu, 
                                                'canttr':ctranc[0], 
                                                'sumtr':ctranc[1]})
    
def reglamento(request):
    
    return render(request, "paginas/reglamento.html")

def task_api_cyclos():

    c_crea_guarda_grupos.delay()
    resultadoCG= c_cantidad_grupos.delay()
    resultadoCU= c_cantidad_usuarios.delay()
    resultadoCST= c_cantidad_suma_transacciones.delay()
    hoy = time.strftime("%Y-%m-%d") 

    print(resultadoCG)

    dato = data(fecha_add = hoy,
                cant_usuarios = resultadoCU, 
                cant_nodos =  resultadoCG, 
                cant_transacc = int(resultadoCST[0]),
                sum_valpos = float(resultadoCST[1]))
    dato.save()
    

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
            if tipogroup['kind'] == 'memberGroup' and tipogroup['groupSet'] == 'nodoValpos' :
                grupos.append(tipogroup)     
                
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
        
    #Grupos guardados en la lista
    viewg.append(Comunidad.objects.all().values())
    nodos = Comunidad.objects.all().values()

    for elemnts in nodos:    
        if elemnts['is_active'] == True:
            countnodos = countnodos + 1

    viewg.append(countnodos)
    return  viewg

def cantUsuarios(requests):
    auth = Auth()
    countUsu = 0
    r = requests.get('https://communities.cyclos.org/valpos/api/users?groups=nodoValpos&includeGroup=true&includeGroupSet=true&orderBy=alphabeticallyAsc&roles=member&statuses=active&pageSize=5000', 
                        auth=(auth.getUser(), 
                        auth.getPass()))
    parsedJsonObject = json.loads(r.text)
 
    for tipoGroups in parsedJsonObject:
        if  tipoGroups['groupSet']['internalName'] == "nodoValpos":
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

