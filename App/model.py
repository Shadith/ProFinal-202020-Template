"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.Algorithms.Sorting import mergesort
from DISClib.Algorithms.Sorting import shellsort
from DISClib.ADT import orderedmap as om
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo

def newInicial():
    inicial = {"compañias": None, "taxis": None, "fechas": None}
    inicial["fechas"] = om.newMap("BST", comparefunction=compararEstacion)
    inicial["compañias"] = m.newMap(maptype="PROBING", comparefunction=compararEstacions2)
    inicial["taxis"] = []

    return inicial

def parteA(inicial, data):
    if data["company"] == "":
        data["company"] = "Independent Owner"
    if data["taxi_id"] not in inicial["taxis"]:
        inicial["taxis"].append(data["taxi_id"])

    existe = m.get(inicial["compañias"], data["company"])
    if existe is None:
        nodo = auxiliar(data)
        m.put(inicial["compañias"], data["company"], nodo)
    else: 
        existe = me.getValue(existe)
        if data["taxi_id"] not in existe["taxis"]:
            existe["taxis"].append(data["taxi_id"])
        existe["servicios"] += 1



# ==============================
# Funciones de consulta
# ==============================

def parteA_consulta(inicial, rankingM, rankingN):
    orden_compañias = m.valueSet(inicial["compañias"])
    compañias_servicios_ordenados = m.valueSet(inicial["compañias"])

    mergesort.mergesort(orden_compañias, comparador_de_taxis)  
    mergesort.mergesort(compañias_servicios_ordenados, comparador_de_servicios) 
    
    numero_compañias = m.size(inicial["compañias"])

    topM = lt.newList("ARRAY_LIST")
    topN =lt.newList("ARRAY_LIST")

    cuantas_tengoM = 1
    while cuantas_tengoM <= rankingM:
        elemento_agregar = lt.getElement(orden_compañias, cuantas_tengoM)
        lt.addLast(topM, elemento_agregar)
        cuantas_tengoM += 1

    cuantas_tengoN = 1
    while cuantas_tengoN <= rankingN:
        elemento_agregar = lt.getElement(compañias_servicios_ordenados, cuantas_tengoN)
        lt.addLast(topN, elemento_agregar)
        cuantas_tengoN += 1

    return (topM, topN, numero_compañias, len(inicial["taxis"]))

def parteB_consultaB(inicial, fecha_ini, fecha_fin, topN):
    fecha_fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")
    fecha_fin = fecha_fin.date()

    fecha_ini = datetime.datetime.strptime(fecha_ini, "%Y-%m-%d")
    fecha_ini = fecha_ini.date()

    datos_mitad = om.values(inicial["fechas"], fecha_ini, fecha_fin)
    datos = m.newMap(maptype="PROBING", comparefunction=compararEstacions2)
    for dic in range(1, lt.size(datos_mitad) + 1):
        lista = lt.getElement(datos_mitad, dic)
        lista = m.valueSet(lista) 

        for ele in range(1, lt.size(lista) + 1):
            dato = lt.getElement(lista, ele)
            obtenido = m.get(datos , dato["taxi"])
            if obtenido == None:
                m.put(datos, dato["taxi"],dato)
            else:
                obtenido=me.getValue(obtenido)
                nodo_antes_servicio=obtenido["puntos"]/obtenido["servicios"]
                nodo_ahora_servicio=dato["puntos"]/dato["servicios"]
                nuevo=nodo_ahora_servicio+nodo_antes_servicio
                nuevo*=(obtenido["servicios"]+dato["servicios"])
                nuevo_nodo={"taxi":obtenido["taxi"],"puntos":nuevo,"servicios":obtenido["servicios"]+dato["servicios"]}
                m.put(datos, nuevo_nodo["taxi"],nuevo_nodo)
    list_final = lt.newList("ARRAY_LIST")
    ordenado = m.valueSet(datos)
    mergesort.mergesort(ordenado, comparador_puntos)
    for dato_ in range(1, lt.size(ordenado) + 1):
        candidato = lt.getElement(ordenado, dato_)
        lt.addLast(list_final, candidato)
        if dato_ == topN:
            break
    return list_final

def consulta_parteBA(inicial, fecha, top):
    fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d")
    fecha = fecha.date()
    mapa_taxi = me.getValue(om.get(inicial["fechas"], fecha))
    final = lt.newList("ARRAY_LIST")
    lst = m.valueSet(mapa_taxi)
    mergesort.mergesort(lst, comparador_puntos)
    cuantas_tengo = 1
    while cuantas_tengo <= top:
        elemento_agregar = lt.getElement(lst, cuantas_tengo)
        lt.addLast(final, elemento_agregar)
        cuantas_tengo += 1
    return final

def mapa_ordenado_fecha(inicial, data):
    if data["trip_total"] == "":
        data["trip_total"] = 0
    if data["trip_miles"] == "":
        data["trip_miles"] = 0
    distancia = float(data["trip_miles"])
    total_dinero = float(data["trip_total"])
    fecha_dia = data["trip_start_timestamp"]
    fecha_dia = fecha_dia[:10]
    fecha_dia = datetime.datetime.strptime(fecha_dia, "%Y-%m-%d")
    fecha_dia = fecha_dia.date()
    fecha = om.get(inicial["fechas"], fecha_dia)
    
    if distancia > 0 and total_dinero > 0:
        if fecha is None:
            mapa_taxi = m.newMap(maptype="PROBING", comparefunction=compararEstacions2)
            nodo = {"taxi": data["taxi_id"], "puntos": float(data["trip_miles"]) / (total_dinero),"servicios": 1}
            m.put(mapa_taxi, data["taxi_id"], nodo)
            om.put(inicial["fechas"], fecha_dia, mapa_taxi)
        else:
            taxi = m.get(me.getValue(fecha), data["taxi_id"])
            if taxi is None:
                nodo = {"taxi": data["taxi_id"], "puntos": float(data["trip_miles"]) / (total_dinero),"servicios": 1}
                m.put(me.getValue(fecha), data["taxi_id"], nodo)
            else:
                taxi = m.get(me.getValue(fecha), data["taxi_id"])
                taxi = me.getValue(taxi)
                puntos = taxi["puntos"]
                servicios = taxi["servicios"]
                suma_nueva = total_dinero/distancia
                puntos = ((puntos / servicios) + suma_nueva) * (servicios + 1) 
                taxi["puntos"] = puntos
                taxi["servicios"] += 1
                


# ==============================
# Funciones Helper
# ==============================

def auxiliar(data):
    nodo = {"compañia": data["company"], "taxis":[data["taxi_id"]], "servicios": 1}
    return nodo

# ==============================
# Funciones de Comparacion
# ==============================

def compararEstacion(estacion1, estacion2):
    if estacion1 == estacion2:
        return 0
    elif estacion1 > estacion2:
        return 1
    else:
        return -1


def compararEstacions2(estacion1, estacion2):
    estacion2 = me.getKey(estacion2)
    if estacion1 == estacion2:
        return 0
    elif estacion1 > estacion2:
        return 1
    else:
        return -1

def comparador_de_servicios(nodo1, nodo2):
    if nodo1["servicios"] > nodo2["servicios"]:
        return True
    return False


def comparador_de_taxis(nodo1, nodo2):
    if len(nodo1["taxis"]) > len(nodo2["taxis"]):
        return True
    return False

def comparador_puntos(nodo1, nodo2):
    if nodo1["puntos"] > nodo2["puntos"]:
        return True
    return False
