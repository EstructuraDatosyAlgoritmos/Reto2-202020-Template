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

import config as cf
from App import model
from time import process_time 
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta. Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newCatalog()
    return catalog

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(catalog,moviesDetailsFile,moviesCastingFile):
    """
    Carga los datos de los archivos en el modelo
    """
    loadDetails(catalog, moviesDetailsFile)
    loadCasting(catalog, moviesCastingFile)

#def loadFiles(catalog,moviesDetailsFile,moviesCastingFile):
#    """
#    Carga cada una de las lineas de ambos archivos de películas.
#    - Se agrega cada película al catalogo de películas.
#    - Por cada película se encuentra su productora y por cada
#      productora, se crea una lista con sus películas
#    """
#    t1_start = process_time() #tiempo inicial
#    moviesDetailsFile = cf.data_dir + moviesDetailsFile
#    moviesCastingFile = cf.data_dir + moviesCastingFile
#    input_file = csv.DictReader(open(moviesDetailsFile,encoding="utf-8-sig"),delimiter=";")
 #   input_file2 = csv.DictReader(open(moviesCastinFile,encoding="utf-8-sig"),delimiter=";")
#
 #   for movie in input_file:
#
 #       actor1_name;actor1_gender;actor2_name;actor2_gender;actor3_name;actor3_gender;actor4_name;actor4_gender;actor5_name;actor5_gender;actor_number;director_name;director_gender;director_number;producer_name;producer_number;screeplay_name;editor_name
  #      model.addMovie(catalog, movie)
    
def loadDetails(catalog, moviesDetailsFile):
    """
    Carga cada una de las lineas del archivo de películas.
    - Se agrega cada película al catalogo de películas.
    - Por cada película se encuentra su productora y por cada
      productora, se crea una lista con sus películas
    """
    t1_start = process_time() #tiempo inicial
    moviesDetailsFile = cf.data_dir + moviesDetailsFile
    input_file = csv.DictReader(open(moviesDetailsFile,encoding="utf-8-sig"),delimiter=";")
    for movie in input_file:
        model.addMovie(catalog, movie)
        producers = movie['production_companies'].split(",")  
        countries = movie['production_countries'].split(",") 
        for producer in producers:
            model.addMovietoMovieFilmProducer(catalog, producer.strip(), movie)
        for country in countries:
            model.addMovietoCountry(catalog,country.strip(),movie)

    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")

def loadCasting(catalog, moviesCastingFile):
    """
    Carga cada una de las lineas del archivo de películas.
   - Se agrega cada libro al catalogo de libros
    - Por cada libro se encuentran sus autores y por cada
      autor, se crea una lista con sus libros
    """
    t1_start = process_time() #tiempo inicial
    moviesCastingFile = cf.data_dir + moviesCastingFile
    input_file = csv.DictReader(open(moviesCastingFile,encoding="utf-8-sig"),delimiter=";")
    for movie in input_file:
        directors = movie['director_name'].split(",") 
        movie_id = movie['id']
        for director in directors:
            model.addMovietoDirector(catalog, director.strip(), movie_id)

    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def moviesSize(catalog):
    """
    Numero de películas leido
    """
    return model.moviesSize(catalog)
def producersSize(catalog):
    """
    RETO2 - REQ1
    Numero de productoras leido
    """
    return model.producersSize(catalog)
def directorsSize(catalog):
    """
    RETO2 - REQ2
    Numero de directores leido
    """
    return model.directorsSize(catalog)
def countriesSize(catalog):
    """
    RETO2 - REQ5
    Numero de países leido
    """ 
    return model.countriesSize(catalog)
  

def getMoviesByProducer(catalog,producername):
    """
    RETO2 - REQ1
    Retorna las películas de una productora
    """
    producerinfo = model.getMoviesByProducer(catalog,producername)
    return producerinfo
def getMoviesByDirector(catalog,directorname):
    """
    RETO2 - REQ2
    Retorna las películas de una productora
    """
    directorinfo = model.getMoviesByDirector(catalog,directorname)
    return directorinfo
def getMoviesByCountry(catalog,countryname):
    """
    RETO2 - REQ5
    Retorna las películas de un país
    """
    countryinfo = model.getMoviesByCountry(catalog,countryname)
    return countryinfo