# from django.http import HttpResponse
# from django.shortcuts import render, redirect, get_object_or_404
# from .forms import MovieForm
# from movieapp.models import Movie
#
#
# # Create your views here.
# def index(request):
#     movie = Movie.objects.all()
#     context = {
#         'movie_list': movie
#     }
#     return render(request, 'index.html', context)
#
#
# def detail(request, movie_id):
#     movie = Movie.objects.get(id=movie_id)
#     return render(request, 'detail.html', {'movie': movie})
#     # return HttpResponse("This is Movie No. %s" %movie_id)
#
#
# def add_movie(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         desc = request.POST.get('desc')
#         year = request.POST.get('year')
#         img = request.FILES['img']
#         movie = Movie(name=name, desc=desc, year=year, img=img)
#         movie.save()
#         return redirect('/')
#     return render(request, 'add.html')
#
#
# def update_movie(request, id):
#     if request.method == 'POST':
#         movie = Movie.objects.get(id=id)
#         form = MovieForm(request.POST or None, request.FILES, instance=movie)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#         else:
#             print("Form errors:", form.errors)
#     else:
#         movie = get_object_or_404(Movie, id=id)
#         form = MovieForm(instance=movie)
#     return render(request, 'update.html', {'form': form, 'movie': movie})
#
# def delete_movie(request, id):
#     if request.method == "POST":
#         movie = Movie.objects.get(id=id)
#         print(movie)
#         print('post')
#         movie.delete()
#         return redirect('/')
#     else:
#         movie = get_object_or_404(Movie, id=id)
#         form = MovieForm(instance=movie)
#         print(movie)
#         print('get')
#     return render(request, 'delete.html',{'form': form, 'movie': movie})


from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.contrib.auth.models import User

from movieproject import settings
from .forms import UserRegisterForm, MovieForm, ReviewForm, UserEditViewForm, CategoryForm
from .models import Movie, Category, Review

import logging

logger = logging.getLogger(__name__)


def register(request):
    print('1.Username is already taken. Please choose a different one.')
    if request.method == 'POST':
        print('2.Username is already taken. Please choose a different one.')
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print('3.Username is already taken. Please choose a different one.')
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                print('4.Username is already taken. Please choose a different one.')
                messages.error(request, 'Username is already taken. Please choose a different one.')
            else:
                print('5.Username is already taken. Please choose a different one.')
                user = form.save()
                # login(request, user)
                send_welcome_email(user.email)
                return redirect('/welcome')
        else:
            logger.error(form.errors)  # Log form errors
            print(form.errors)  # Print form errors to console for debugging
    else:
        print('6.Username is already taken. Please choose a different one.')
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def send_welcome_email(email):
    subject = 'Welcome to Our Site!'
    html_message = render_to_string('welcome_email.html')
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = email
    # send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


@login_required
def add_movie(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            return redirect('/')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form, 'categories': categories})


@login_required
def review_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            movie_detail_url = f'/movie/{movie_id}/'
            return redirect(movie_detail_url)
            # return redirect('movie_detail', movie_id=movie.id)
    else:
        form = ReviewForm()
    return render(request, 'review_movie.html', {'form': form, 'movie': movie, 'categories': categories})


def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    categories = Category.objects.all()
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'movie_detail.html', {'movie': movie, 'reviews': reviews, 'categories': categories})


def category(request, category_id):
    category = Category.objects.get(id=category_id)
    movies = Movie.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'category.html', {'category': category, 'movies': movies, 'categories': categories})


def home(request):
    movies = Movie.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'movies': movies, 'categories': categories})


def welcome(request):
    return render(request, 'welcome.html')


@login_required
def view_profile(request):
    categories = Category.objects.all()
    user = request.user
    form = UserEditViewForm(instance=user)
    return render(request, 'view_profile.html', {'form': form, 'categories': categories})


@login_required
def edit_profile(request):
    profile = request.user
    categories = Category.objects.all()
    if request.method == 'POST':
        form = UserEditViewForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/view_profile')
    else:
        form = UserEditViewForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form, 'categories': categories})


@login_required
def edit_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    categories = Category.objects.all()
    if movie.added_by != request.user:
        return HttpResponseForbidden("You are not allowed to edit this movie.")

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'edit_movie.html', {'form': form, 'movie': movie, 'categories': categories})


@login_required
def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    if movie.added_by != request.user:
        return HttpResponseForbidden("You are not allowed to delete this movie.")
    if request.method == "POST":
        movie.delete()
        return redirect('/')
    return render(request, 'delete_movie.html', {'movie': movie})


@login_required
def search_result(request):
    query = request.GET.get('query')
    movies = Movie.objects.all()
    categories = Category.objects.all()
    results = None

    if query:
        # Perform case-insensitive search on the movie title
        results = Movie.objects.filter(title__icontains=query)
        print(results)
    return render(request, 'search_result.html',
                  {'results': results, 'query': query, 'movies': movies, 'categories': categories})


@login_required
def users(request):
    # Retrieve all users from the database
    users = User.objects.all()

    # Render the users in a template
    return render(request, 'users.html', {'users': users})


@login_required
def delete_user(request, user_id):
    # Retrieve the user object to be deleted
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        # If the request method is POST, it means the user has confirmed deletion
        user.delete()
        # Redirect to a page confirming the deletion or any other appropriate page
        return redirect('/users')
    else:
        # If the request method is not POST, render a confirmation template
        return render(request, 'confirm_user_delete.html', {'user': user})


@login_required
def confirm_delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'confirm_user_delete.html', {'user': user})


@login_required
def add_category(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/categories')  # Assuming you have a view for viewing categories
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})


@login_required
def admin_panel(request):
    # Logic for retrieving data or performing actions in the admin panel
    return render(request, 'admin_panel.html')
@login_required
def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})
