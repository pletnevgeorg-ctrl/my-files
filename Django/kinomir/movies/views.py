from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Movie

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movies/movie_detail.html', {'movie': movie})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        if not username or not email or not password:
            messages.error(request, "Все поля обязательны для заполнения.")
        elif password != password_confirm:
            messages.error(request, "Пароли не совпадают.")
        elif len(password) < 6:
            messages.error(request, "Пароль должен быть не менее 6 символов.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким именем уже существует.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('movie_list')

    return render(request, 'movies/register.html')