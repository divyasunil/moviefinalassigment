# from django.db import models
#
#
# # Create your models here.
# class Movie(models.Model):
#     name = models.CharField(max_length=250)
#     desc = models.TextField()
#     year = models.IntegerField()
#     img = models.ImageField(upload_to='gallery')
#
#     def __str__(self):
#         return self.name
#


from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='posters/')
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trailer_link = models.URLField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'