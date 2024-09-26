import os
import json
import requests
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import numpy as np

# Cargar la clave API desde el archivo .env
_ = load_dotenv('api_keys.env')
hf_api_key = os.environ.get('hp_api_key')

# URL de la API de Hugging Face para Stable Diffusion XL
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {hf_api_key}"}

# Función para hacer la consulta a Hugging Face
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code != 200:
        raise Exception(f"Error en la solicitud a Hugging Face API: {response.status_code} - {response.text}")
    
    return response.content

# Se carga la lista de películas desde el archivo movie_descriptions.json
with open('movie_descriptions.json', 'r') as file:
    movies = json.load(file)

# Seleccionar aleatoriamente una película
idx_movie = np.random.randint(len(movies) - 1)
selected_movie = movies[idx_movie]
print(f"Título de la película seleccionada: {selected_movie['title']}")

# Preparar el prompt para generar la imagen
prompt = f"Portada de la película {selected_movie['title']}"

# Hacer la consulta a la API de Hugging Face
image_bytes = query({"inputs": prompt})

# Verificar si el contenido recibido es una imagen válida
try:
    # Convertir la respuesta en una imagen con PIL
    image = Image.open(BytesIO(image_bytes))
    
    # Mostrar la imagen generada
    image.show()
except Exception as e:
    print("Error al generar la imagen:", e)
    print("Contenido recibido:", image_bytes[:500])  # Muestra los primeros 500 bytes para depuración
