import requests
import random

# url = "https://poetrydb.org/author/Ernest Dowson"

def texto_generico():

    sujetos = ["La naturaleza", "El programador", "Una mente curiosa", "El conocimiento", "La paciencia", "El arte", "La ciencia"]
    verbos = ["crea", "inspira", "transforma", "enseña", "guía", "fortalece", "descubre", "encuentra"]
    complementos = ["el camino correcto", "una solución nueva", "la armonía interior", "el poder del cambio", "la belleza de lo natural", "la esencia de la vida", "la fuerza del equilibrio"]

    palabra_generada = [random.choice(sujetos),random.choice(verbos),random.choice(complementos)]

    return palabra_generada

def generador_frases(url: str):
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        palabras_generadas = []
        
        for i in datos:
            palabras_generadas.append(i[0])

        return palabras_generadas

    except requests.ConnectionError as error_conect:
        return texto_generico()