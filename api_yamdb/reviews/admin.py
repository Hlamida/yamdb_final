from django.contrib import admin
from reviews.models import Category, Genre, Review, Title, User

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
