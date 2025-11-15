import requests
import random
import json
import os

# url = "https://poetrydb.org/author/Ernest Dowson"
# url = "https://api.breakingbadquotes.xyz/v1/quotes/20"

def texto_generico():

    texto = """

    En la actualidad, el desarrollo tecnológico ha transformado profundamente la manera en que vivimos, 
    trabajamos y nos relacionamos. Desde la aparición de los teléfonos inteligentes hasta la expansión 
    del internet de las cosas, cada avance ha contribuido a una sociedad más conectada y eficiente. Sin embargo, 
    esta evolución también plantea desafíos importantes, como la protección de la privacidad, la dependencia
    digital y la brecha de acceso entre distintos sectores sociales. Uno de los aspectos más fascinantes
    de esta transformación es cómo ha impactado la educación. Hoy en día, es posible acceder a cursos, 
    tutoriales y bibliotecas virtuales desde cualquier parte del mundo, lo que democratiza el conocimiento y permite
    a millones de personas aprender nuevas habilidades sin necesidad de asistir a una institución física. 
    westa flexibilidad ha dado lugar a nuevas formas de enseñanza, como el aprendizaje autodidacta y las comunidades
    colaborativas en línea, que fomentan la creatividad y el pensamiento crítico.

    """
    
    return texto
"""
def obtener_frases_api(url: str):
    
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        palabras_generadas = []
        
        for i in datos:
            palabras_generadas.append(i["quote"])

        return palabras_generadas

    except requests.ConnectionError as error_conect:
        return texto_generico()
    except ValueError:
        return texto_generico()
"""  

def breaking_bad():
    url = "https://api.breakingbadquotes.xyz/v1/quotes/20"

    respuesta = requests.get(url)
    datos = respuesta.json()
    palabras_generadas = []
    
    for i in datos:
        palabras_generadas.append(i["quote"])

    return palabras_generadas

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


"""
def leer_txt():
"""

lista_textos = ["hola " + str(x) for x in range(20)]

#print(poemas())
#print(textos_offline())
#print(lista_textos)


def selector():
    lista_apis = [breaking_bad, poemas, textos_offline]
    selecta = random.choice(lista_apis)
    try:
        return selecta()
    except:
        return textos_offline()

selector()