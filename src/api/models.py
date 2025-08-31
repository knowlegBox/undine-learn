from django.db import models

class User(models.Model):
    # Rendu optionnel
    username = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    # Rendu optionnel
    bio = models.TextField(null=True, blank=True)
    # Rendu optionnel




class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        null=True,
        blank=True
    )
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Comment(models.Model):
    # Rendu optionnel
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True
    )
    # Rendu optionnel
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Rendu optionnel
    text = models.TextField(null=True, blank=True)

class Like(models.Model):
    # Rendu optionnel
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Rendu optionnel
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
        null=True,
        blank=True
    )