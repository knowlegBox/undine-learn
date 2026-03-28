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
    profile_picture = models.CharField(max_length=255, null=True, blank=True)

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

class Product(models.Model):
    # Rendu optionnel
    name = models.CharField(max_length=100, null=True, blank=True)
    # Rendu optionnel
    description = models.TextField(null=True, blank=True)
    # Rendu optionnel
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
class Order(models.Model):
    # Rendu optionnel
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Rendu optionnel
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    # Rendu optionnel
    total_quantity = models.IntegerField(null=True, blank=True)
    # Rendu optionnel
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class OrderItem(models.Model):
    # Rendu optionnel
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        null=True,
        blank=True
    )
    # Rendu optionnel
    product_name = models.CharField(max_length=100, null=True, blank=True)
    # Rendu optionnel
    quantity = models.IntegerField(null=True, blank=True)
    # Rendu optionnel
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)