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
    Autores
    ID libros
    Tags
    Año de publicacion

    Retorna el catalogo inicializado.
    """
    catalog = {'movies': None,
               'moviesIds': None,
               'producers': None,
               'tags': None,
               'tagIds': None,
               'years': None}

    t1_start = process_time() #tiempo inicial
    catalog['movies'] = lt.newList('SINGLE_LINKED', compareMoviesIds)
    catalog['moviesIds'] = mp.newMap(1000,
                                   maptype='CHAINING',
                                   loadfactor=2,
                                   comparefunction=compareMapMovieIds)
    catalog['producers'] = mp.newMap(500,
                                   maptype='CHAINING',
                                   loadfactor=2,
                                   comparefunction=compareProducersByName)
#    catalog[''] = mp.newMap(1000,
#                                maptype='CHAINING',
#                                loadfactor=0.7,
#                                comparefunction=compareTagNames)
#    catalog[''] = mp.newMap(1000,
#                                  maptype='CHAINING',
#                                  loadfactor=0.7,
#                                  comparefunction=compareTagIds)
#    catalog[''] = mp.newMap(500,
#                                 maptype='CHAINING',
#                                 loadfactor=0.7,
#                                 comparefunction=compareMapYear)

    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return catalog



def newFilmProducer(name):
    """
    Crea una nueva estructura para modelar las películas de una productora
    y su promedio de ratings
    """
    producer = {'name': "", "movies": None,  "average_rating": 0}
    producer['name'] = name
    producer['movies'] = lt.newList('SINGLE_LINKED', )
    return producer


# Funciones para agregar informacion al catalogo

def addMovie(catalog, movie):
    """
    Esta funcion adiciona una película a la lista de películas,
    adicionalmente lo guarda en un Map usando como llave su Id.
    """
    lt.addLast(catalog['movies'], movie)
    mp.put(catalog['moviesIds'], movie['id'], movie)


def addMovieFilmProducer(catalog, producername, movie):
    """
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

def moviesSize(catalog):
    """
    Número de películas en el catago
    """
    return lt.size(catalog['movies'])


def producersSize(catalog):
    """
    Numero de productoras en el catalogo
    """
    return mp.size(catalog['producers'])

# ==============================
# Funciones de Comparacion
# ==============================


def compareMoviesIds(id1,id2):
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
