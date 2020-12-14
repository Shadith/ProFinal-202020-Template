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
import config as cf
from App import model
import csv
import os
"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def inicial():
    inicial = model.newInicial()
    return inicial


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los
#  modelos
# ___________________________________________________

def carga_archivos (inicial, opcion):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith(opcion + ".csv"):
            print("Cargando archivo: " + filename)
            cargar(inicial, filename)
    return inicial

def cargar(inicial, ruta):
    rutaCom = cf.data_dir + ruta
    input_file = csv.DictReader(open(rutaCom, encoding="utf-8"), delimiter=",")
    for data in input_file:
        model.parteA(inicial, data)
        model.mapa_ordenado_fecha(inicial, data)
    return inicial



# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def parteA_consulta(inicial, rankingM, rankingN):
    retorno = model.parteA_consulta(inicial, rankingM, rankingN)
    return retorno

def consulta_parteBA(inicial, fecha, top):
    retorno = model.consulta_parteBA(inicial, fecha, top)
    return retorno

def ParteB_consultaB(inicial, fecha_ini, fecha_fin, topN):
    retorno = model.parteB_consultaB(inicial, fecha_ini, fecha_fin, topN)
    return retorno
