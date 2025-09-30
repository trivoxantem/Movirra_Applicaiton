from django.shortcuts import render, get_object_or_404
from .models import Genre, Comment, Country, Episode, Video, UserProfile, WatchHistory, Trailer, Profile
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect   
from django.contrib import messages


# Create your views here.


# def home(request):
#     # Latest movies
#     latest_movies = Video.objects.filter(video_type='movie').order_by('-created_at')[:10]

#     # Trending or most recent TV series
#     tv_series = Video.objects.filter(video_type='tv_series').order_by('-created_at')[:10]

#     # All genres for filter menu
#     genres = Genre.objects.all()

#     # All countries for regional categories
#     countries = Country.objects.all()

#     context = {
#         'latest_movies': latest_movies,
#         'tv_series': tv_series,
#         'genres': genres,
#         'countries': countries,
#     }
#     return render(request, 'home.html', context)


def signupUser(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Name already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')
            
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.get_or_create(user=user)
        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')


def loginUser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
    return render(request, 'login.html')   


def home(request):
    trailers = Trailer.objects.all()
    episodes = Episode.objects.all().order_by('-created_at')[:12] 
    query = request.GET.get("q")
    trending_movies = Video.objects.filter(video_type='movie').order_by('-created_at')[:7]

    if query:
        # Search for both movies and TV series
        latest_movies = Video.objects.filter(
            Q(video_type='movie'),
            Q(title__icontains=query) | Q(description__icontains=query) | Q(genres__name__icontains=query)
        ).distinct()

        tv_series = Video.objects.filter(
            Q(video_type='tv_series'),
            Q(title__icontains=query) | Q(description__icontains=query) | Q(genres__name__icontains=query)
        ).distinct()
    else:
        # Default content
        latest_movies = Video.objects.filter(video_type='movie').order_by('-created_at')[:10]
        tv_series = Video.objects.filter(video_type='tv_series').order_by('-created_at')[:10]

    genres = Genre.objects.all()
    countries = Country.objects.all()

    context = {
        'latest_movies': latest_movies,
        'tv_series': tv_series,
        'genres': genres,
        'countries': countries,
        'query': query,
        'trailers': trailers,
        'episodes': episodes,  
        'trending_movies': trending_movies,
    }
    return render(request, 'home.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request, pk):
    user_profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'profile.html', {'user_profile': user_profile})

@login_required
def movies(request):
    all_movies = Video.objects.all().order_by('-created_at')
    return render(request, 'movies.html', {'all_movies': all_movies})

@login_required
def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'watchnow.html', {'video': video})

@login_required
def play_video_simple(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'play_video_simple.html', {'video': video})

@login_required
def tv_series_list(request):
    episodes = Episode.objects.all()
    return render(request, 'tv_series_list.html', {'episodes': episodes})

