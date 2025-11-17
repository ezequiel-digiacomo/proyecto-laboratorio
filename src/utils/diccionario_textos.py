import requests
import random
import json
import os

def breaking_bad():
    url = "https://api.breakingbadquotes.xyz/v1/quotes/7" # el 20 indica cuantas frases trae

    respuesta = requests.get(url)
    datos = respuesta.json()
    palabras_generadas = [] # armo una lista vacia para pasarle las frases, es el tipo de dato que trabaj nuestro juego
    
    for i in datos:
        palabras_generadas.append(i["quote"]) 

    return palabras_generadas # nos devuelve la lista de frases

def poemas():
    url_autores = "https://poetrydb.org/author"
    url_poemas = "https://poetrydb.org/author/"
    autores = requests.get(url_autores)
    datos = autores.json()
    autor = random.choice(datos["authors"])
    url_poemas += autor

    obtener_lineas = requests.get(url_poemas).json()

    obtenida = obtener_lineas[0]["lines"]

    return obtenida

def textos_offline():
    ruta_de_la_carpeta =  os.getcwd()
    ruta_textos = ruta_de_la_carpeta + "/src/utils/offlinetexts"
    archivos_y_carpetas = os.listdir(ruta_textos)
    archivo_elegido = random.choice(archivos_y_carpetas)
    
    with open(f"{ruta_textos}/{archivo_elegido}" , "r", encoding="utf-8") as f:
        lineas = f.readlines()
        lista_limpia = [linea.replace('\n', '') for linea in lineas]

    return lista_limpia

################################################################################################################
def selector():
    lista_apis = [breaking_bad, poemas, textos_offline]
    selecta = random.choice(lista_apis)
    try:
        return selecta()
    except requests.ConnectionError as error_conect:
        print(f"{error_conect}")
        return textos_offline()

