# ====================================================================
#                   DOCUMENTATION DE L'API GRAPHQL
# ====================================================================

add_product = """
# ====================================================================
#                   ADD PRODUCT MUTATION
# ====================================================================

Cette mutation permet de créer un nouveau produit dans le catalogue.

📝 Description
-------------
Crée un produit avec un nom, une description, un prix et optionnellement une catégorie.

⚡ Arguments
-----------
    - name (String)             : Nom du produit
    - description (String)      : Description détaillée
    - price (Float)             : Prix unitaire
    - category (Object)         : Catégorie à associer (nom et description)

📤 Returns
---------
    - success (Boolean)         : Statut de l'opération
    - message (String)          : Statut ou message d'erreur
    - instance (Product)        : Le produit créé

🔍 Example Usage
----------------
```graphql
mutation {
  addProduct(
    name: "Clavier Mécanique"
    description: "Clavier RVB avec switchs rouges"
    price: 89.99
    category: {
      name: "Informatique"
      description: "Périphériques et accessoires"
    }
  ) {
    success
    message
    instance {
      id
      name
      price
    }
  }
}
```
"""

update_product = """
# ====================================================================
#                   UPDATE PRODUCT MUTATION
# ====================================================================

Cette mutation permet de mettre à jour un produit existant.

⚡ Arguments
-----------
    - id (ID!)                  : Identifiant unique du produit (pk)
    - name (String)             : Nouveau nom
    - description (String)      : Nouvelle description
    - price (Float)             : Nouveau prix
    - category (Object)         : Nouvelle catégorie ou mise à jour
    - isActive (Boolean)        : État du produit
    - isDeleted (Boolean)       : Marqué comme supprimé

📤 Returns
---------
    - success (Boolean)         : Statut de l'opération
    - message (String)          : Message de confirmation
    - instance (Product)        : Le produit mis à jour

🔍 Example Usage
----------------
```graphql
mutation {
  updateProduct(
    id: "1"
    price: 79.99
    isActive: true
  ) {
    success
    message
    instance {
      id
      name
      price
      isActive
    }
  }
}
```
"""

get_products = """
# ====================================================================
#                   GET PRODUCTS LIST (QUERY)
# ====================================================================

Cette requête permet de lister les produits avec des options de filtrage et de tri.

📝 Description
-------------
Récupère une liste simple de produits.

⚡ Arguments (Filtres & Tri)
-----------
    - filter (ProductFilter) :
        - category (String)     : Filtre par nom de catégorie (icontains)
    - order (ProductOrder) :
        - name (ASC/DESC)       : Tri par nom
        - price (ASC/DESC)      : Tri par prix

🔍 Example Usage (Filter & Order)
------------------------------
```graphql
query {
  productListe(
    filter: { category: "Info" }
    order: { price: DESC }
  ) {
    id
    name
    price
    category {
      name
    }
  }
}
```
"""

get_product_connection = """
# ====================================================================
#                   GET PRODUCT CONNECTION (RELAY)
# ====================================================================

Requête paginée utilisant la norme Relay Connection.

📝 Description
-------------
Idéal pour charger de grandes quantités de données avec pagination par curseur.

⚡ Arguments (Relay + Filter)
-----------
    - first (Int)               : Nombre d'éléments à récupérer
    - after (String)            : Curseur de début
    - filter (ProductFilter)    : Filtrage par catégorie
    - order (ProductOrder)      : Tri avancé

🔍 Example Usage
----------------
```graphql
query {
  product(first: 5, after: "...", order: { name: ASC }) {
    edges {
       node {
         id
         name
       }
       cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```
"""
