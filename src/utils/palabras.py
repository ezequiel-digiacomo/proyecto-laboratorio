import requests
import random

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
    
