# from django import forms
# from .models import Movie
#
# class MovieForm(forms.ModelForm):
#     class Meta:
#         model=Movie
#         fields=['name','desc','year','img']


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Movie, Review, Category


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserEditViewForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class MovieForm(forms.ModelForm):
    release_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    # poster = forms.ImageField(required=False)

    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'category', 'trailer_link']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
