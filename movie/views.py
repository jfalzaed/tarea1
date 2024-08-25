from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.

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

    # Obtener todas las películas
    all_movies = Movie.objects.all()

    # Gráfico de películas por año
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

    # Gráfico de películas por género
    movie_counts_by_genre = {}
    for movie in all_movies:
        genre = movie.genre if movie.genre else "None"
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1
    bar_positions = range(len(movie_counts_by_genre))
    plt.figure(figsize=(12, 6))  # Aumentar el tamaño de la figura para acomodar etiquetas largas
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')
    plt.title('Películas por Género')
    plt.xlabel('Género')
    plt.ylabel('Número de Películas')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=45, ha='right', fontsize=10)  # Rotar y ajustar el tamaño de la fuente
    plt.subplots_adjust(bottom=0.4)  # Ajustar espaciado inferior para evitar que se corten las etiquetas
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png).decode('utf-8')

    # Renderizar la plantilla con ambos gráficos
    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})
