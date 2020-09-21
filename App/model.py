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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from time import process_time 
from DISClib.DataStructures import mapentry as me
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

"""

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------

def newCatalog():
    """ Inicializa el catálogo de libros

    Crea una lista vacia para guardar todas las películas

    Se crean indices (Maps) por los siguientes criterios:
    Movies Ids
    Producers
    
    Año de publicacion

    Retorna el catalogo inicializado.
    """
    catalog = {'movies': None,
               'moviesIds': None,
               'producers': None,
               'directors': None,
               'countries': None}

    t1_start = process_time() #tiempo inicial
    catalog['movies'] = lt.newList('SINGLE_LINKED', compareMovies)
    catalog['moviesIds'] = mp.newMap(1000,
                                   maptype='CHAINING',
                                   loadfactor=2,
                                   comparefunction=compareMapMovieIds)
    catalog['producers'] = mp.newMap(500,
                                   maptype='CHAINING',
                                   loadfactor=2,
                                   comparefunction=compareProducersByName)
    catalog['directors'] = mp.newMap(500,
                                maptype='CHAINING',
                                loadfactor=2,
                                comparefunction=compareDirectorsByName)
#    catalog['actors'] = mp.newMap(1000,
#                                  maptype='CHAINING',
#                                  loadfactor=0.7,
#                                  comparefunction=compareTagIds)
#    catalog['genres'] = mp.newMap(500,
#                                 maptype='CHAINING',
#                                 loadfactor=0.7,
#                                 comparefunction=compareMapYear)
    catalog['countries'] = mp.newMap(500,
                                 maptype='CHAINING',
                                 loadfactor=2,
                                 comparefunction=compareCountriesByName)


    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return catalog



def newFilmProducer(name):
    """
    RETO2 - REQ1
    Crea una nueva estructura para modelar las películas de una productora
    y su promedio de ratings
    """
    producer = {'name': "", "movies": None,  "average_rating": 0}
    producer['name'] = name
    producer['movies'] = lt.newList('SINGLE_LINKED',compareProducersByName )
    return producer

def newDirector(name):
    """
    RETO2 - REQ2
    Crea una nueva estructura para modelar las películas de una productora
    y su promedio de ratings
    """
    director = {'name': "", "movies": None,  "average_rating": 0}
    director['name'] = name
    director['movies'] = lt.newList('SINGLE_LINKED',compareDirectorsByName )
    return director

def newCountry(name):
    """
    RETO2 - REQ5
    Crea una nueva estructura para modelar las películas de un país
    """
    country = {'name': "", "movies": None}
    country['name'] = name
    country['movies'] = lt.newList('ARRAY_LIST',compareCountriesByName)
    return country


# Funciones para agregar informacion al catalogo

def addMovie(catalog, movie):
    """
    Esta funcion adiciona una película a la lista de películas,
    adicionalmente lo guarda en un Map usando como llave su Id.
    """
    lt.addLast(catalog['movies'], movie)
    mp.put(catalog['moviesIds'], movie['id'], movie)

def addMovietoMovieFilmProducer(catalog, producername, movie):
    """
    RETO2 - REQ1
    Esta función adiciona una película a la lista de películas producidas
    por la respectiva productora.
    Cuando se adiciona la película se actualiza el promedio de dicha productora
    """
    producers = catalog['producers']
    existproducer = mp.contains(producers, producername)
    if existproducer:
        entry = mp.get(producers, producername)
        producer = me.getValue(entry)
    else:
        producer = newFilmProducer(producername)
        mp.put(producers, producername, producer)   
    lt.addLast(producer['movies'], movie)

    producerAvg = producer['average_rating']
    movieAvg = movie['vote_average']
    if (producerAvg == 0.0):
        producer['average_rating'] = float(movieAvg)
    else:
        producer['average_rating'] = round((producerAvg + float(movieAvg)) / 2,2)

def addMovietoDirector(catalog,directorname,movie_id):
    """
    RETO2 - REQ2
    Esta función adiciona una película a la lista de películas dirigidas
    por el respectivo director.
    Cuando se adiciona la película se actualiza el promedio de dicho director
    """
    directors = catalog['directors']
    movies_ids = catalog['moviesIds']
    entry = mp.get(movies_ids,movie_id)
    movie = me.getValue(entry)

    existdirector = mp.contains(directors,directorname)
    if existdirector:
        entry = mp.get(directors,directorname)
        director = me.getValue(entry)
    else:
        director = newDirector(directorname)
        mp.put(directors,directorname,director)      
    lt.addLast(director['movies'], movie)

    directorAvg = director['average_rating']
    movieAvg = movie['vote_average']
    if (directorAvg == 0.0):
        director['average_rating'] = float(movieAvg)
    else:
        director['average_rating'] = round((directorAvg + float(movieAvg)) / 2,2)

def addMovietoCountry(catalog,countryname,movie):
    """
    RETO2 - REQ5
    Esta función adiciona una película a la lista de películas producidas en un país.
    """
    countries = catalog['countries']
    existcountry = mp.contains(countries,countryname)
    if existcountry:
        entry = mp.get(countries,countryname)
        country = me.getValue(entry)
    else:
        country = newCountry(countryname)
        mp.put(countries,countryname,country)

    lt.addLast(country['movies'], movie)

    "POR REVISAR, INCOMPLETO"
    movies_Ids = catalog['moviesIds']
    movie_id_for_search = movie['id']

    entry = mp.get(movies_Ids,movie_id_for_search)
    movieinfo = me.getValue(entry)
    print("hola")

    director_name = movieinfo['director_name']
    movie['director_name'] = director_name
    

# ==============================
# Funciones de consulta
# ==============================

def getMoviesByProducer(catalog, producername):
    """
    RETO2 - REQ1
    Retorna una productora con sus películas a partir del nombre de la productora
    """
    t1_start = process_time() #tiempo inicial
    producer = mp.get(catalog['producers'], producername)
    if producer:
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
        return me.getValue(producer)
    return None

def getMoviesByDirector(catalog,directorname):
    """
    RETO2 - REQ2
    Retorna un director con sus películas a partir del nombre ingresado
    """
    t1_start = process_time() #tiempo inicial
    director = mp.get(catalog['directors'], directorname)
    if director:
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
        return me.getValue(director)
    return None

def getMoviesByCountry(catalog,countryname):
    """
    RETO2 - REQ5
    Retorna un país con sus películas a partir del nombre ingresado
    """
    t1_start = process_time() #tiempo inicial
    country = mp.get(catalog['countries'], countryname)
    if country:
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
        return me.getValue(country)
    return None

def moviesSize(catalog):
    """
    Número de películas en el catago
    """
    return lt.size(catalog['movies'])
def producersSize(catalog):
    """
    RETO2 - REQ1
    Numero de productoras en el catalogo
    """
    return mp.size(catalog['producers'])
def directorsSize(catalog):
    """
    RETO2 - REQ2
    Numero de directores en el catalogo
    """
    return mp.size(catalog['directors'])
def countriesSize(catalog):
    """
    RETO2 - REQ5
    Numero de países en el catalogo
    """
    return mp.size(catalog['countries'])

# ==============================
# Funciones de Comparacion
# ==============================


def compareMovies(id1,id2):
    """
    Compara dos ids de películas
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareMapMovieIds(id, entry):
    """
    Compara dos ids de películas, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return -1

def compareProducersByName(keyname, producer):
    """
    RETO2 - REQ1
    Compara dos nombres de productoras. El primero es una cadena
    y el segundo un entry de un map
    """
    prodEntry = me.getKey(producer)
    if (keyname == prodEntry):
        return 0
    elif (keyname > prodEntry):
        return 1
    else:
        return -1

def compareDirectorsByName(keyname, director):
    """
    RETO2 - REQ2
    Compara dos nombres de directores. El primero es una cadena
    y el segundo un entry de un map
    """

    direcEntry = me.getKey(director)
    if (keyname == direcEntry):
        return 0
    elif (keyname > direcEntry):
        return 1
    else:
        return -1

def compareCountriesByName(keyname,country):
    """
    RETO2 - REQ5
    Compara dos nombres de países. El primero es una cadena
    y el segundo un entry de un map
    """
    countryEntry = me.getKey(country)
    if (keyname == countryEntry):
        return 0
    elif (keyname > countryEntry):
        return 1
    else:
        return -1


def numeritos(num1,num2):
    if (num1 == num2):
        return 0
    elif num1 > num2:
        return 1
    else:
        return -1
        
lista_numeritos = lt.newList("ARRAY_LIST",cmpfunction=numeritos)
numerito1 = input("Ingrese el primer numero:")
numerito2 = input("Ingrese el numero:")
numerito3 = input("Ingrese el numero:")
numerito4 = input("Ingrese el numero:")
lt.addLast(lista_numeritos,numerito1)
lt.addLast(lista_numeritos,numerito2)
lt.addLast(lista_numeritos,numerito3)
lt.addLast(lista_numeritos,numerito4)
print(lista_numeritos)