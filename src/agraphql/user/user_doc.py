###### ====================================================================
######                   DOCUMENTATION DE L'API USER
###### ====================================================================

add_user = """
###### ====================================================================
######                   ADD USER MUTATION
###### ====================================================================

Cette mutation permet de créer un nouvel utilisateur.

📝 Description
-------------
Crée un compte utilisateur avec un nom d'utilisateur, un email et un mot de passe.

⚡ Arguments
-----------
    - username (String!)        : Nom d'utilisateur unique (requis)
    - email (String)            : Adresse email
    - password (String)         : Mot de passe

📤 Returns
---------
    - success (Boolean)         : Statut de l'opération
    - message (String)          : Message de confirmation ou d'erreur
    - instance (User)           : L'utilisateur créé

🔍 Example Usage
----------------
```graphql
mutation {
  addUser(
    username: "jdoe"
    email: "jdoe@example.com"
    password: "securepassword123"
  ) {
    success
    message
    instance {
      id
      username
      email
    }
  }
}
```
"""

update_user = """
###### ====================================================================
######                   UPDATE USER MUTATION
###### ====================================================================

Cette mutation permet de mettre à jour les informations d'un utilisateur existant.

⚡ Arguments
-----------
    - id (ID!)                  : Identifiant unique de l'utilisateur (pk)
    - username (String)         : Nouveau nom d'utilisateur
    - email (String)            : Nouvel email
    - password (String)         : Nouveau mot de passe
    - isActive (Boolean)        : État du compte
    - isDeleted (Boolean)       : Marqué comme supprimé

📤 Returns
---------
    - success (Boolean)         : Statut de l'opération
    - message (String)          : Message de confirmation
    - instance (User)           : L'utilisateur mis à jour

🔍 Example Usage
----------------
```graphql
mutation {
  updateUser(
    id: "1"
    email: "newemail@example.com"
  ) {
    success
    message
    instance {
      id
      username
      email
    }
  }
}
```
"""

get_users = """
###### ====================================================================
######                   GET USERS (RELAY CONNECTION)
###### ====================================================================

Cette requête permet de lister les utilisateurs avec pagination Relay, filtrage et tri.

📝 Description
-------------
Récupère une liste d'utilisateurs paginée par curseur.

⚡ Arguments (Relay + Filter + Order)
-----------
    - first (Int)               : Nombre d'éléments à récupérer
    - after (String)            : Curseur de début
    - filter (UserFilter)       : Filtres dynamiques (username, email, etc.)
    - order (UserOrder)         : Options de tri (username, createdAt, etc.)

🔍 Example Usage
----------------
```graphql
query {
  users(first: 10, filter: { username: "jdoe" }) {
    edges {
       node {
         id
         username
         email
         createdAt
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
