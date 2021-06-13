from django.shortcuts import render, HttpResponse #(este metodo nos permite contestar a una peticion, devolviendo un codigo de progamacion)
from BDmscv.models import Comunidad, data
from django.db import IntegrityError
import time
import requests                                                  
import json
import aiohttp
import asyncio
import logging
import os
from time import perf_counter
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)

# Create your views here.
def home(request):  
    dataStats = []
    dataCall = asyncio.run(cyclosApiCall())
    if  dataCall != 'errorApi':
        tiposGroups(dataCall[0]) 
        cantgroups = cantGrupos()
        cantusu = cantUsuarios(dataCall[1])
        ctranc = cantTransacc(dataCall[2])
        
        dataStats.extend([cantusu,
                            cantgroups,
                            int(ctranc[0]),
                            float(ctranc[1])])
        saveData(dataStats)
    listaGroups = listaGrupos()

    dinamicStats = data.objects.order_by('fecha_add').last()
    
    return render(request, "paginas/home.html",{'viewgrupos':listaGroups, 
                                                'cantg':dinamicStats.cant_nodos, 
                                                'cantusu':dinamicStats.cant_usuarios, 
                                                'canttr':dinamicStats.cant_transacc, 
                                                'sumtr':dinamicStats.sum_valpos})
    
def reglamento(request):
    
    return render(request, "paginas/reglamento.html")


def tiposGroups(grupos):
    objGrupos =  [] 
    resultObject = grupos['groups']
    #separo y obtengo solo los grupos tipo memeberGroup
    for tipogroup in resultObject: 
        if tipogroup['kind'] == 'memberGroup' and tipogroup['groupSet'] == 'nodoValpos' :
            objGrupos.append(tipogroup)     
            
    #Busco en la BD si la id del grupo esta agregada, si no esta se agrega
            
    for ingrupos in objGrupos:
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

def listaGrupos():
    listaGr = Comunidad.objects.all().values()
    return listaGr

def cantGrupos():
    countnodos = 0
    nodos = Comunidad.objects.all().values()

    for elemnts in nodos:    
        if elemnts['is_active'] == True:
            countnodos += 1
    return countnodos

def cantUsuarios(cantUsers):
    countUsu = 0
    for tipoGroups in cantUsers:
        if  tipoGroups['groupSet']['internalName'] == "nodoValpos":
            countUsu=countUsu + 1
    return countUsu        
            
def cantTransacc(totalTransac):
    ctranc = []     
    ctranc.append(totalTransac[0]['count'])
    ctranc.append(totalTransac[0]['sum'])
    return ctranc

def saveData(dataStats):

    hoy = time.strftime("%Y-%m-%d")
    if not data.objects.filter(fecha_add = hoy):
        dato = data(fecha_add = hoy,
                    cant_usuarios = dataStats[0], 
                    cant_nodos =  dataStats[1], 
                    cant_transacc = dataStats[2],
                    sum_valpos = dataStats[3])
        dato.save()
    else:
        print("fecha ya ingresada")


async def get_response(session, url):
    auth = Auth() 
    async with session.get(url, auth=aiohttp.BasicAuth(os.environ.get('CYCLOS_USER'), os.environ.get('CYCLOS_PASSWORD'))) as resp:
        response = await resp.json()
        return response

async def cyclosApiCall():
    try:
        dataCall = []
        async with aiohttp.ClientSession() as session:
            urls =[
                'https://communities.cyclos.org/valpos/api/users/data-for-search?fields=&fromMenu=false',
                'https://communities.cyclos.org/valpos/api/users?groups=nodoValpos&includeGroup=true&includeGroupSet=true&orderBy=alphabeticallyAsc&roles=member&statuses=active&pageSize=5000',
                'https://communities.cyclos.org/valpos/api/transfers/summary?kinds=&skipTotalCount=false&transferKinds=', 
                ]

            tasks = []
            for url in urls:
                tasks.append(asyncio.ensure_future(get_response(session, url)))

            result_response = await asyncio.gather(*tasks)
            for response in result_response:
                dataCall.append(response)
            
            return dataCall
    except Exception as e:
        logger.error(e)
        dataCall = 'errorApi'
        return dataCall
