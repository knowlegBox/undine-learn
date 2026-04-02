from django.db import models

class Projects(models.Model):
    name = models.CharField(max_length=255, db_column="name", help_text="Nom du projet")
    description = models.TextField(db_column="description", help_text="Description détaillée du projet")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_column="created_at", help_text="Date de création")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, db_column="updated_at", help_text="Date de dernière mise à jour")
    is_active = models.BooleanField(default=True, null=True, blank=True, db_column="is_active", help_text="Indique si le projet est actif")
    is_deleted = models.BooleanField(default=False, null=True, blank=True, db_column="is_deleted", help_text="Indique si le projet est supprimé")
    metas = models.JSONField(null=True, blank=True, db_column="metas", help_text="Métadonnées additionnelles en format JSON")

class User(models.Model):
    # Rendu optionnel
    username = models.CharField(max_length=50, null=True, blank=True, db_column="username", help_text="Nom d'utilisateur unique")
    first_name = models.CharField(max_length=50, null=True, blank=True, db_column="first_name", help_text="Prénom de l'utilisateur")
    last_name = models.CharField(max_length=50, null=True, blank=True, db_column="last_name", help_text="Nom de famille de l'utilisateur")
    email = models.EmailField(max_length=50, null=True, blank=True, db_column="email", help_text="Adresse email de l'utilisateur")
    password = models.CharField(max_length=50, null=True, blank=True, db_column="password", help_text="Mot de passe sécurisé")
    # Rendu optionnel
    bio = models.TextField(null=True, blank=True, db_column="bio", help_text="Biographie ou description de l'utilisateur")
    # Rendu optionnel
    profile_picture = models.CharField(max_length=255, null=True, blank=True, db_column="profile_picture", help_text="URL de la photo de profil")
    is_active = models.BooleanField(default=True, null=True, blank=True, db_column="is_active", help_text="Indique si l'utilisateur est actif")
    is_deleted = models.BooleanField(default=False, null=True, blank=True, db_column="is_deleted", help_text="Indique si l'utilisateur est supprimé")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_column="created_at", help_text="Date de création")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, db_column="updated_at", help_text="Date de dernière mise à jour")
    metas = models.JSONField(null=True, blank=True, db_column="metas", help_text="Métadonnées additionnelles en format JSON")

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="posts",
        null=True,
        blank=True,
        db_column="author_user",
        help_text="Auteur de la publication"
    )
    content = models.TextField(null=True, blank=True, db_column="content", help_text="Contenu textuel de la publication")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_column="created_at", help_text="Date de création")
    is_active = models.BooleanField(default=True, null=True, blank=True, db_column="is_active", help_text="Indique si la publication est active")
    is_deleted = models.BooleanField(default=False, null=True, blank=True, db_column="is_deleted", help_text="Indique si la publication est supprimée")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, db_column="updated_at", help_text="Date de dernière mise à jour")
    metas = models.JSONField(null=True, blank=True, db_column="metas", help_text="Métadonnées additionnelles en format JSON")

class Comment(models.Model):
    # Rendu optionnel
    post = models.ForeignKey(
        Post,
        on_delete=models.DO_NOTHING,
        related_name="comments",
        null=True,
        blank=True,
        db_column="post",
        help_text="Publication associée au commentaire"
    )
    # Rendu optionnel
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="comments",
        db_column="user",
        help_text="Utilisateur ayant rédigé le commentaire"
    )
    # Rendu optionnel
    text = models.TextField(null=True, blank=True, db_column="text", help_text="Texte du commentaire")
    is_active = models.BooleanField(default=True, null=True, blank=True, db_column="is_active", help_text="Indique si le commentaire est actif")
    is_deleted = models.BooleanField(default=False, null=True, blank=True, db_column="is_deleted", help_text="Indique si le commentaire est supprimé")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_column="created_at", help_text="Date de création")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, db_column="updated_at", help_text="Date de dernière mise à jour")
    metas = models.JSONField(null=True, blank=True, db_column="metas", help_text="Métadonnées additionnelles en format JSON")

class Like(models.Model):
    # Rendu optionnel
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="likes",
        db_column="user",
        help_text="Utilisateur ayant aimé la publication"
    )
    # Rendu optionnel
    post = models.ForeignKey(
        Post,
        on_delete=models.DO_NOTHING,
        related_name="likes",
        null=True,
        blank=True,
        db_column="post",
        help_text="Publication aimée"
    )
    is_active = models.BooleanField(default=True, null=True, blank=True, db_column="is_active", help_text="Indique si le like est actif")
    is_deleted = models.BooleanField(default=False, null=True, blank=True, db_column="is_deleted", help_text="Indique si le like est supprimé")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_column="created_at", help_text="Date de création")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, db_column="updated_at", help_text="Date de dernière mise à jour")
    metas = models.JSONField(null=True, blank=True, db_column="metas", help_text="Métadonnées additionnelles en format JSON")

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, db_column="name",unique=True, help_text="Nom de la catégorie")
    description = models.TextField(null=True, blank=True, db_column="description", help_text="Description de la catégorie")
    is_active = models.BooleanField(default=True, null=True, blank=True, db_column="is_active", help_text="Indique si la catégorie est active")
    is_deleted = models.BooleanField(default=False, null=True, blank=True, db_column="is_deleted", help_text="Indique si la catégorie est supprimée")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_column="created_at", help_text="Date de création")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, db_column="updated_at", help_text="Date de dernière mise à jour")
    metas = models.JSONField(null=True, blank=True, db_column="metas", help_text="Métadonnées additionnelles en format JSON")

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="products",
        db_column="category",
        help_text="Catégorie du produit"
    )
    # Rendu optionnel
    name = models.CharField(max_length=100, null=True, blank=True, db_column="name", help_text="Nom du produit")
    # Rendu optionnel
    description = models.TextField(null=True, blank=True, db_column="description", help_text="Description du produit")
    # Rendu optionnel
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column="price", help_text="Prix unitaire du produit")
    is_active = models.BooleanField(default=True, null=True, blank=True, db_column="is_active", help_text="Indique si le produit est actif")
    is_deleted = models.BooleanField(default=False, null=True, blank=True, db_column="is_deleted", help_text="Indique si le produit est supprimé")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_column="created_at", help_text="Date de création")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, db_column="updated_at", help_text="Date de dernière mise à jour")
    metas = models.JSONField(null=True, blank=True, db_column="metas", help_text="Métadonnées additionnelles en format JSON")
    
class Order(models.Model):
    # Rendu optionnel
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="orders",
        db_column="user",
        help_text="Client ayant passé la commande"
    )
    date = models.DateField(blank=True,null=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column="total_price", help_text="Prix total de la commande")
    is_active = models.BooleanField(default=True, null=True, blank=True, db_column="is_active", help_text="Indique si la commande est active")
    is_deleted = models.BooleanField(default=False, null=True, blank=True, db_column="is_deleted", help_text="Indique si la commande est supprimée")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_column="created_at", help_text="Date de création")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, db_column="updated_at", help_text="Date de dernière mise à jour")
    metas = models.JSONField(null=True, blank=True, db_column="metas", help_text="Métadonnées additionnelles en format JSON")

class OrderItem(models.Model):
    # Rendu optionnel
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        related_name="items",
        null=True,
        blank=True,
        db_column="order",
        help_text="Commande parente"
    )
    # Rendu optionnel
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column="total_price", help_text="Prix total de l'article")
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING, null=True, blank=True, db_column="products", help_text="Nom du produit au moment de l'achat")
    # Rendu optionnel
    quantity = models.IntegerField(null=True, blank=True, db_column="quantity", help_text="Quantité commandée")
    # Rendu optionnel
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column="price", help_text="Prix unitaire au moment de l'achat")
    is_active = models.BooleanField(default=True, null=True, blank=True, db_column="is_active", help_text="Indique si l'article est actif")
    is_deleted = models.BooleanField(default=False, null=True, blank=True, db_column="is_deleted", help_text="Indique si l'article est supprimé")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_column="created_at", help_text="Date de création")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, db_column="updated_at", help_text="Date de dernière mise à jour")
    metas = models.JSONField(null=True, blank=True, db_column="metas", help_text="Métadonnées additionnelles en format JSON")