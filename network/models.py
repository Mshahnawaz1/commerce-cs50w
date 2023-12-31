from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # add fields for follower, following etc
    pass

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")
    post = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} posted {self.post}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ensure  user can only follow one per one time
        unique_together = ('user', 'followed')

    def __str__(self):
        return f"{self.user} follows {self.followed}"

class Likes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="Liked" )
    post = models.ForeignKey(Posts, on_delete=models.CASCADE,blank=True, related_name='liked_post')
    timestamp=models.DateTimeField(auto_now_add=True)

# python manage.py makemigrations