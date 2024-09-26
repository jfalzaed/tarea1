import os
import json
import time  # Para introducir pausas entre solicitudes
from dotenv import load_dotenv
import google.generativeai as genai

# Se leen las claves API desde el archivo .env
_ = load_dotenv('api_keys.env')
genai.configure(api_key=os.environ.get('gemini_api_key'))

# Se carga la lista de películas desde el archivo movie_titles.json
with open('movie_titles.json', 'r') as file:
    file_content = file.read()
    movies = json.loads(file_content)

# Selecciona un modelo de Google Generative AI
model = genai.GenerativeModel('gemini-pro')

# Instrucción para la IA generativa con un prompt seguro
instruction = """
Proporciona una breve y objetiva descripción de la película en menos de 100 palabras.
La descripción debe ser completamente neutral, sin contenido explícito, inapropiado o dañino, y debe centrarse únicamente en
los detalles de la trama y los géneros cinematográficos. No incluyas opiniones, juicios de valor o temas sensibles.
Recuerda no usar tildes ni simbolos para evitar conflictos con mi app
"""

instruction_genre = "El género de la película es:"
instruction_year = "El año de lanzamiento de la película es:"

# Función auxiliar para manejar el contenido generado y comprobar los safety_ratings
def generar_contenido(prompt):
    try:
        response = model.generate_content(prompt)
        # Verificar si hay candidatos y si hay alguna restricción de seguridad
        if response.candidates and hasattr(response.candidates[0], 'safety_ratings'):
            print(f"Safety ratings: {response.candidates[0].safety_ratings}")
        # Si no hay bloqueo, devolver el texto
        if hasattr(response, 'text') and response.text:
            return response.text.strip()
    except Exception as e:
        print(f"Error al generar contenido: {e}")
    return "No disponible"

# Iterar sobre las primeras 8 películas, agregando pausas
for i in range(8):
    print(f"Procesando película {i+1}: {movies[i]['title']}")

    # Generar la descripción de la película
    prompt_description = f"{instruction} Haz una descripción de la película {movies[i]['title']}"
    descripcion = generar_contenido(prompt_description)
    movies[i]['description'] = descripcion
    
    # Generar el género de la película
    prompt_genre = f"{instruction_genre} {movies[i]['title']}"
    genero = generar_contenido(prompt_genre)
    movies[i]['genre'] = genero
    
    # Generar el año de lanzamiento de la película
    prompt_year = f"{instruction_year} {movies[i]['title']}"
    year = generar_contenido(prompt_year)
    movies[i]['year'] = year
    
    # Mostrar la película procesada
    print(f"Título: {movies[i]['title']}")
    print(f"Género: {movies[i]['genre']}")
    print(f"Año: {movies[i]['year']}")
    print(f"Descripción: {movies[i]['description']}")
    print(f"Pelicula {i+1} de 8 procesada")

    # Introducir una pausa de 3 segundos para no superar el límite de solicitudes
    time.sleep(3)

# Guardar los datos en un archivo JSON
file_path = "movie_descriptions.json"
with open(file_path, 'w') as json_file:
    json.dump(movies[:8], json_file, indent=4)

print(f"Datos guardados en {file_path}")
