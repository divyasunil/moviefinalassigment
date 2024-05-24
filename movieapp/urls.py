# from . import views
# from django.urls import path, include
# app_name='movieapp'
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('movie/<int:movie_id>/', views.detail, name='detail'),
#     path('add/', views.add_movie, name='add_movie'),
#     path('update/<int:id>/', views.update_movie, name='update_movie'),
#     path('delete/<int:id>/', views.delete_movie, name='delete_movie'),
# ]



from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='movieapp'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/review/', views.review_movie, name='review_movie'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('welcome/', views.welcome, name='welcome'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('movie/<int:id>/edit/', views.edit_movie, name='edit_movie'),
    path('movie/<int:id>/delete/', views.delete_movie, name='delete_movie'),
    path('search_result/', views.search_result, name='search_result'),
    path('add_category/', views.add_category, name='add_category'),
    path('users/', views.users, name='users'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('confirm_delete_user/<int:user_id>/', views.confirm_delete_user, name='confirm_delete_user'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('categories/', views.view_categories, name='view_categories'),
]
