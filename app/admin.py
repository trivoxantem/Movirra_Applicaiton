from django.contrib import admin
from .models import Genre, Comment, Country, Episode, Video, UserProfile, WatchHistory, Trailer, Profile

# Register your models here.

all = [Genre, Comment, Country, Episode, Video, UserProfile, WatchHistory, Trailer, Profile]

admin.site.register(all)