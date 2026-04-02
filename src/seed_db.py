import os
import json
import django
from decimal import Decimal

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zconfig.settings')
django.setup()

from api.models import User, Category, Product, Order, OrderItem

def load_json(filename):
    path = os.path.join(os.path.dirname(__file__), '..', 'dataset', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def seed():
    print("--- Démarrage du remplissage de la base de données ---")

    # 1. Users
    print("Chargement des utilisateurs...")
    users_data = load_json('user_data.json')
    for data in users_data:
        User.objects.update_or_create(
            id=data['id'],
            defaults={
                'username': data.get('username'),
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'email': data.get('email'),
                'password': data.get('password'),
                'bio': data.get('bio'),
                'profile_picture': data.get('profile_picture'),
                'is_active': data.get('is_active', True),
                'is_deleted': data.get('is_deleted', False)
            }
        )

    # 2. Categories
    print("Chargement des catégories...")
    categories_data = load_json('categorie.json')
    for data in categories_data:
        Category.objects.update_or_create(
            id=data['id'],
            defaults={
                'name': data['name'],
                'description': data['description'],
                'is_active': data.get('is_active', True),
                'is_deleted': data.get('is_deleted', False)
            }
        )

    # 3. Products
    print("Chargement des produits...")
    products_data = load_json('product_data.json')
    for data in products_data:
        category = Category.objects.get(id=data['categorie'])
        Product.objects.update_or_create(
            id=data.get('id'),
            defaults={
                'category': category,
                'name': data.get('name'),
                'description': data.get('description'),
                'price': Decimal(str(data.get('price'))),
                'is_active': data.get('is_active', True),
                'is_deleted': data.get('is_deleted', False)
            }
        )

    # 4. Orders & OrderItems
    print("Chargement des commandes...")
    orders_data = load_json('order_data.json')
    for order_data in orders_data:
        user = User.objects.get(id=order_data['user'])
        order, created = Order.objects.update_or_create(
            id=order_data['id'],
            defaults={
                'user': user,
                'total_price': Decimal(str(order_data['total_price'])),
                'is_active': order_data.get('is_active', True),
                'is_deleted': order_data.get('is_deleted', False)
            }
        )
        
        # Effacer les anciens items pour cette commande si nécessaire (uniquement si update)
        if not created:
            OrderItem.objects.filter(order=order).delete()

        # Créer les items de commande
        for item_data in order_data['items']:
            product = Product.objects.get(id=item_data['product'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=Decimal(str(item_data['price'])),
                total_price=Decimal(str(item_data['total_price'])),
                is_active=True,
                is_deleted=False
            )

    print("--- Remplissage terminé avec succès ! ---")

if __name__ == "__main__":
    seed()
