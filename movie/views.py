from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv


def get_embedding(text, client, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recommendation(request):


    _ = load_dotenv('api_keys.env')
    client = OpenAI(
        api_key=os.environ.get('openai_api_key'),
    )

    req = request.GET.get('recommendation')

    if req:

        items = Movie.objects.all()
        embeddings = get_embedding(req, client)

        sim = []
 
        for item in items:
            emb = list(np.frombuffer(item.emb))
            sim.append(cosine_similarity(emb, embeddings))
 
        idx = int(np.argmax(sim))
        
        movies = Movie.objects.filter(title=items[idx].title)
        print(movies)
    else:
 
        movies = Movie.objects.all()


    return render(request, 'recommendation.html', {'recommendation': req, 'movies': movies})


def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Jhonsito'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})



def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html', {'name':'Jhon'})

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def statistics_view(request):
    matplotlib.use('Agg')

    # Películas
    all_movies = Movie.objects.all()

    # Año
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))
    plt.figure(figsize=(12, 6))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Películas por Año')
    plt.xlabel('Año')
    plt.ylabel('Número de Películas')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png).decode('utf-8')

    # Género
    movie_counts_by_genre = {}
    for movie in all_movies:
        genre = "None"
    
        if movie.genre:
            
            genres = [g.strip() for g in movie.genre.split(',')]
            
            
            for g in genres:
                if g.lower() != "short": 
                    genre = g
                    break
            if genre == "None" and "short" in [g.lower() for g in genres]:
                genre = "Short"

        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1
    bar_positions = range(len(movie_counts_by_genre))
    plt.figure(figsize=(12, 6))  
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')
    plt.title('Películas por Género')
    plt.xlabel('Género')
    plt.ylabel('Número de Películas')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=45, ha='right', fontsize=10)  
    plt.subplots_adjust(bottom=0.4)  
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png).decode('utf-8')

    # Gráficos finales
    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})
