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
 """

import sys
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from App import controller
assert config


"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones y por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

#moviesCastingFile = 'Movies/MoviesCastingRaw-small.csv'
moviesCastingFile = 'Movies/AllMoviesCastingRaw.csv'

#moviesDetailsFile = 'Movies/SmallMoviesDetailsCleaned.csv'
moviesDetailsFile = 'Movies/AllMoviesDetailsCleaned.csv'


# ___________________________________________________
#  Funciones para imprimir la inforamación de
#  respuesta.  La vista solo interactua con
#  el controlador.
# ___________________________________________________

def printProducerData(producer):
    """
    RETO2 - REQ1
    Imprime las películas de una productora determinada
    """
    if producer:
        print('Productora encontrada: ' + producer['name'])
        print('Promedio votación películas: ' + str(producer['average_rating']))
        print('Total de películas: ' + str(lt.size(producer['movies'])))
        iterator = it.newIterator(producer['movies'])
        while it.hasNext(iterator):
            movie = it.next(iterator)
            print('Titulo: ' + movie['title'] + '  Avg. Rating: ' + movie['vote_average'])
    else:
        print('No se encontró la productora.')

def printDirectorData(director):
    """
    RETO2 - REQ2
    Imprime las películas de un director determinado
    """
    if director:
        print('Director encontrado: ' + director['name'])
        print('Promedio votación películas: ' + str(director['average_rating']))
        print('Total de películas: ' + str(lt.size(director['movies'])))
        iterator = it.newIterator(director['movies'])
        while it.hasNext(iterator):
            movie = it.next(iterator)
            print('Titulo: ' + movie['title'] + '  Avg. Rating: ' + movie['vote_average'])
    else:
        print('No se encontró el director.')

def printActorData(actor):
    if actor:
        print('Actor encontrado: ' + actor['name'])
        print('Promedio votación películas: ' + str(actor['average_rating']))
        print('Total de películas: ' + str(lt.size(actor['movies'])))
        iterator = it.newIterator(actor['movies'])
        while it.hasNext(iterator):

            movie = it.next(iterator)
            print('Titulo: ' + movie['title'] + '  Avg. Rating: ' + movie['vote_average'])
    else:
         print('No se encontró el actor/actriz.')
def printGenderData(gender):
    """
    RETO2 - REQ4
    Imprime las películas de un género determinado
    """
    if gender:
        print('Películas asociadas encontradas: ' + gender['name'])
        print('Promedio votación películas: ' + str(gender['average_rating']))
        print('Total de películas: ' + str(lt.size(gender['movies'])))
        iterator = it.newIterator(gender['movies'])
        while it.hasNext(iterator):
            movie = it.next(iterator)
            print('Titulo: ' + movie['title'] + '  Avg. Rating: ' + movie['vote_average'])
    else:
        print('No se encontró película asociada.')
def printCountryData(country):
    """
    RETO2 - REQ5
    Imprime las películas de un país determinado
    """
    if country:
        print('País encontrado: ' + country['name'])
        print('Total de películas: ' + str(lt.size(country['movies'])))
        iterator = it.newIterator(country['movies'])
        while it.hasNext(iterator):
            movie = it.next(iterator)
            print('Titulo: ' + movie['title'] + '   Director: ' + movie['director_name'] + '   Fecha de producción: ' + movie['release_date'] )
    else:
        print('No se encontró el país.')

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("Bienvenido")
    print("1- Inicializar Catálogo")
    print("2- Cargar información en el catálogo")
    print("3- REQ1: Descubrir productoras de cine.")
    print("4- REQ2: Conocer a un director. ")
    print("5- REQ3: Conocer a un actor.")
    print("6- REQ4: Entender un género cinematográfico.")
    print("7- REQ5: Encontrar películas por país.")
    print("0- Salir")

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.initCatalog()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(cont,moviesDetailsFile,moviesCastingFile)
        print('Películas cargadas: ' + str(controller.moviesSize(cont)))
        print('Productoras de Cine cargadas: ' + str(controller.producersSize(cont)))
        print('Directores de Cine cargados: ' + str(controller.directorsSize(cont)))
        print('Actores de Cine cargados: ' + str(controller.actorssize(cont)))
        print('Países cargados: ' + str(controller.countriesSize(cont)))

    elif int(inputs[0]) == 3:
        producername = input("Nombre de la productora a buscar: ")
        producerinfo = controller.getMoviesByProducer(cont, producername)
        printProducerData(producerinfo)

    elif int(inputs[0]) == 4:
        directorname =  input("Ingrese el nombre del director a buscar: ")
        directorinfo = controller.getMoviesByDirector(cont, directorname)
        printDirectorData(directorinfo)

    elif int(inputs[0]) == 5:
        actorname =  input("Ingrese el nombre del actor/actriz a buscar: ")
        actorinfo = controller.getMoviesByActor(cont, actorname)
        printActorData(actorinfo)

    elif int(inputs[0]) == 6:
        gendername = input("Ingrese el nombre del género a buscar: ")
        genreinfo = controller.getMoviesByGender(cont,gendername)
        printGenderData(genreinfo)
    elif int(inputs[0]) == 7:
        countryname = input("Ingrese el nombre del país a buscar: ")
        countryinfo = controller.getMoviesByCountry(cont,countryname)
        printCountryData(countryinfo)

    else:
        sys.exit(0)
sys.exit(0)
