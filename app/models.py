from django.db import models
from django.contrib.auth.models import User

# ALL MY MODELS HERE FOR MY PROJECTS



# Genre Model
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Country or Region for movies (e.g., Korean, Bollywood)
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Movie or TV Series model (shared base)
class Video(models.Model):
    VIDEO_TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('tv_series', 'TV Series'),
        ('episode', 'Episode'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='videos')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    video_upload = models.FileField(upload_to='videos')
    video_type = models.CharField(max_length=20, choices=VIDEO_TYPE_CHOICES)
    poster_image = models.ImageField(blank=True, null=True, upload_to='imgages/')  # URL or upload
    created_at = models.DateTimeField(auto_now_add=True)
    video_file_url = models.URLField(blank=True, null=True)  # just one video per movie


    def __str__(self):
        return self.title

# For TV Series: episodes
class Episode(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='episodes')  # The parent TV Series
    season_number = models.PositiveIntegerField()
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    video_file_url = models.URLField(blank=True, null=True)  # Link to the video file or streaming URL
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'season_number', 'episode_number')

    def __str__(self):
        return f"{self.video.title} S{self.season_number}E{self.episode_number}"


# User profile - extend built-in User if needed
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add fields like subscription status, watch history, etc.
    subscription_active = models.BooleanField(default=False)
    # Add other fields as needed

    def __str__(self):
        return self.user.username

# User watch history (optional)
class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, null=True, blank=True)
    watched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.video:
            return f"{self.user.username} watched {self.video.title}"
        elif self.episode:
            return f"{self.user.username} watched {self.episode}"
        return f"{self.user.username} watched unknown content"

# Comments or reviews
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.video.title}"


class Trailer(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    rating = models.CharField(max_length=10, blank=True, null=True)
    trailers = models.FileField(upload_to='trailers')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatar.webp')
    bio = models.TextField(blank=True)
    # Add more fields as needed

    def __str__(self):
        return self.user.username