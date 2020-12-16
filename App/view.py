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
import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
from DISClib.ADT import list as lt
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Menu principal
# ___________________________________________________

"""
Menu principal
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analyzer")
    print("2- Cargar información en el Analyzer")
    print("3- PARTE A")
    print("4- APARTE B")
    print("5- APARTE 2B")
    print("0- Salir")

while True:
    printMenu()
    inputs = input("Seleccione una opcion para continuar:\n")
    if inputs == "1":
        vacio = controller.inicial()
    elif inputs == "2":
        decision = input("Qué archivo desea cargar :\n")
        controller.carga_archivos(vacio, decision)
    elif inputs == "3":
        rankingM = int(input("Top M de compañias por cantidad de taxis:\n"))
        rankingN = int(input("Top N compañias por servicios:\n"))
        parteA = controller.parteA_consulta(vacio, rankingM, rankingN)
    
        print("Cantidad de taxis de los servicios reportados:", parteA[3])
        print("Cantidad de compañias de los servicios reportados:", parteA[2])
        print("******************************************************************")
        print("Compañias con mas taxis inscritos: ")
        print("******************************************************************")
        for i in range(1,lt.size(parteA[0])+1):
            imprime = lt.getElement(parteA[0], i)
            print(imprime["compañia"],len(imprime["taxis"]))
        print("******************************************************************")
        print("Top de compañias que mas servicios prestaron: ")
        print("******************************************************************")
        for i in range(1,lt.size(parteA[1])+1):
            imprime = lt.getElement(parteA[1], i)
            print(imprime["compañia"], imprime["servicios"])
        print("******************************************************************")

    elif inputs == "4":
        fechaUs = input("Fecha \n:")
        top = int(input("Digite el top \n:"))
        resultado=controller.consulta_parteBA(vacio, fechaUs, top)
        print("******************************************************************")
        print("Top taxi en una fecha: ")
        print("******************************************************************")
        for taxi in range(1, lt.size(resultado) + 1):
            imprime = lt.getElement(resultado, taxi)
            print(imprime["taxi"],imprime["puntos"])
        print("******************************************************************")
            

    elif inputs == "5":
        fecha_ini = input("Fecha_ini\n:")
        fecha_fin=input("fecha_fin\n:")
        top = int(input("Digite el top \n:"))
        resultado=controller.ParteB_consultaB(vacio, fecha_ini,fecha_fin, top)
        print("******************************************************************")
        print("Top taxi con mas puntos entre dos fechas: ")
        print("******************************************************************")
        for taxi in range(1, lt.size(resultado) + 1):
            imprime = lt.getElement(resultado, taxi)
            print(imprime["taxi"],imprime["puntos"])
        print("******************************************************************")

    else:
        sys.exit(0)
sys.exit(0)
