import requests

def obtener_texto():
    url = "https://baconipsum.com/api/?type=meat-and-filler&paras=5&format=text"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lanza error si algo falla
        texto = response.text
        return texto
    except requests.RequestException as e:
        print("Error al obtener el texto:", e) 
        return "No se pudo obtener el texto desde la API."