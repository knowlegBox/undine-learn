# Formation complète : API GraphQL avec Django & Undine

> **Public cible :** Développeurs Django souhaitant maîtriser Undine pour construire des API GraphQL performantes, sécurisées et maintenables.
> **Niveau :** Débutant → Avancé
> **Documentation officielle :** https://mrthearman.github.io/undine/

---

## Table des matières

1. [Module 1 — Introduction à Undine](#module-1--introduction-à-undine)
2. [Module 2 — Schémas, RootTypes et Entrypoints](#module-2--schémas-roottypes-et-entrypoints)
3. [Module 3 — QueryTypes et Fields](#module-3--querytypes-et-fields)
4. [Module 4 — Filtrage, tri et pagination](#module-4--filtrage-tri-et-pagination)
5. [Module 5 — Mutations et gestion des données](#module-5--mutations-et-gestion-des-données)
6. [Module 6 — Mutations avancées : relations, validation, permissions](#module-6--mutations-avancées--relations-validation-permissions)
7. [Module 7 — Temps réel avec les Subscriptions](#module-7--temps-réel-avec-les-subscriptions)
8. [Module 8 — Optimisation des performances](#module-8--optimisation-des-performances)
9. [Module 9 — Sécurité, documents persistés et bonnes pratiques](#module-9--sécurité-documents-persistés-et-bonnes-pratiques)
10. [Module 10 — Intégrations et outils](#module-10--intégrations-et-outils)
11. [Module 11 — Configuration avancée et personnalisation](#module-11--configuration-avancée-et-personnalisation)
12. [Module 12 — Projet final : API de gestion de projets](#module-12--projet-final--api-de-gestion-de-projets)

---

## Module 1 — Introduction à Undine

### Objectifs du module

- Comprendre ce qu'est Undine et pourquoi l'utiliser face à Graphene ou Strawberry
- Saisir l'architecture globale d'une API Undine
- Installer et configurer Undine dans un projet Django
- Créer et tester un premier endpoint GraphQL

### Durée estimée : 1h30

### Concepts clés

- Bibliothèque Undine, graphql-core, PyPI
- `INSTALLED_APPS`, `UNDINE` settings dict
- `create_schema`, endpoint `/graphql/`
- GraphiQL

---

### 1.1 Pourquoi Undine ?

Undine est une bibliothèque GraphQL pour Django, disponible sur PyPI. Elle est construite au-dessus de `graphql-core` (le port Python de la référence GraphQL.js) et propose une approche **code-first** directement liée aux modèles Django.

#### Comparatif des bibliothèques GraphQL Django

| Critère | Graphene-Django | Strawberry | **Undine** |
|---|---|---|---|
| Approche | Code-first | Code-first (type hints) | Code-first (type hints) |
| Auto-génération depuis modèles | Partielle | Non | **Oui (complète)** |
| Optimiseur automatique N+1 | Non natif | Non natif | **Oui, intégré** |
| Subscriptions | Limitées | Oui | **Oui (WS, SSE, Multipart)** |
| Async natif | Non | Oui | **Oui** |
| DataLoaders | Manuel | Manuel | **Intégré** |
| Documents persistés | Non | Non | **Oui** |
| Hooks de cycle de vie | Non | Non | **Oui** |
| Tests intégrés | Non | Non | **Oui** |
| Maintenance active (2024-2025) | Ralentie | Active | **Active** |

**Points forts d'Undine :**
- Génération automatique de types GraphQL depuis les modèles Django
- Optimisation automatique des requêtes (résolution du problème N+1)
- Filtrage logiquement composable (`AND`, `OR`, `NOT`, `XOR`)
- Mutations unitaires et bulk, avec gestion des relations
- Support complet des subscriptions (WebSockets, SSE, Multipart HTTP)
- Outils de test intégrés

---

### 1.2 Architecture globale

Une API Undine s'articule autour de quatre concepts fondamentaux :

```
Django Models
     │
     ▼
QueryType / MutationType  ←── Logique métier, permissions, validation
     │
     ▼
RootType (Query / Mutation / Subscription)
     │
     ▼
Entrypoint  ←── "endpoint dans le schéma GraphQL"
     │
     ▼
create_schema()  →  Schéma GraphQL exposé via /graphql/
```

**Flux d'une requête :**
1. Le client envoie une requête GraphQL en HTTP POST (ou WebSocket pour les subscriptions)
2. Undine parse et valide le document GraphQL
3. Les lifecycle hooks s'exécutent (cache, auth, logging...)
4. L'optimiseur analyse la requête et prépare les QuerySets optimisés
5. Les resolvers s'exécutent avec les données déjà chargées
6. La réponse JSON est retournée au client

---

### 1.3 Installation et configuration

#### Installation

```bash
pip install undine
```

Pour les subscriptions WebSocket ou SSE en Single Connection mode :

```bash
pip install undine django-channels channels-redis
```

#### `settings.py`

```python
INSTALLED_APPS = [
    "django.contrib.contenttypes",  # Requis par Undine
    "django.contrib.auth",
    # ... vos apps
    "undine",
]

# Configuration de base d'Undine
UNDINE = {
    # Pointer vers votre schéma (dotted import path)
    "SCHEMA": "myapp.schema.schema",

    # Activer GraphiQL pour le développement
    "GRAPHIQL_ENABLED": True,
    "ALLOW_INTROSPECTION_QUERIES": True,

    # Convertit snake_case → camelCase dans le schéma (actif par défaut)
    "CAMEL_CASE_SCHEMA_FIELDS": True,
}
```

#### `urls.py`

```python
from django.urls import include, path

urlpatterns = [
    # Undine enregistre automatiquement /graphql/
    path("", include("undine.http.urls")),
]
```

#### Vérification de l'installation

```bash
python manage.py check undine
# → System check identified no issues (0 silenced).
```

#### Premier schéma (`myapp/schema.py`)

```python
from undine import Entrypoint, RootType, create_schema


class Query(RootType):
    @Entrypoint
    def hello(self) -> str:
        return "Bonjour depuis Undine !"


schema = create_schema(query=Query)
```

Démarrez le serveur et naviguez vers `http://localhost:8000/graphql/` pour accéder à GraphiQL.

Testez votre premier appel :

```graphql
query {
  hello
}
```

Réponse attendue :

```json
{
  "data": {
    "hello": "Bonjour depuis Undine !"
  }
}
```

---

### Mise en garde

> ⚠️ **`"django.contrib.contenttypes"` est obligatoire** dans `INSTALLED_APPS` pour qu'Undine fonctionne. Il n'est pas nécessaire de placer `"undine"` à un endroit précis dans la liste.

> ⚠️ **`ALLOW_INTROSPECTION_QUERIES` est `False` par défaut** — c'est une mesure de sécurité délibérée. Ne l'activez qu'en développement ou pour des clients de confiance.

---

### Exercice d'application

Créez un projet Django vierge avec une application `api`. Installez Undine, configurez-le et créez un schéma exposant :
- Un entrypoint `ping` qui retourne `"pong"`
- Un entrypoint `version` qui retourne `"1.0.0"`

Vérifiez le fonctionnement dans GraphiQL.

---

### Ressources complémentaires

- [Home — Undine](https://mrthearman.github.io/undine/)
- [Getting Started — Undine](https://mrthearman.github.io/undine/getting-started/)
- [Tutorial — Undine](https://mrthearman.github.io/undine/tutorial/)
- [GraphQL Learn](https://graphql.org/learn/)

---

## Module 2 — Schémas, RootTypes et Entrypoints

### Objectifs du module

- Maîtriser la création de `RootType` pour Query, Mutation et Subscription
- Comprendre les différents types de références pour les `Entrypoints`
- Configurer les options avancées : caching, permissions, visibilité, complexité
- Exporter le schéma GraphQL en SDL

### Durée estimée : 2h

### Concepts clés

- `RootType`, `Entrypoint`, `create_schema`
- `GQLInfo`, type hints, arguments
- `cache_time`, `cache_per_user`, `complexity`
- `errors` (Error as Data), `nullable`, `many`
- `schema_name`, `description`, `deprecation_reason`

---

### 2.1 Les RootTypes

En GraphQL, un `RootType` est un `ObjectType` spécial qui sert de point d'entrée racine. Undine reconnaît trois opérations : `Query`, `Mutation`, `Subscription`.

```python
from undine import Entrypoint, RootType, create_schema


class Query(RootType):
    """Opérations de lecture."""

    @Entrypoint
    def testing(self) -> str:
        return "Hello, World!"


class Mutation(RootType):
    """Opérations d'écriture."""

    @Entrypoint
    def testing(self) -> int:
        return 42


# Le schéma est valide dès qu'un Query RootType existe
schema = create_schema(query=Query, mutation=Mutation)
```

**Règles importantes :**
- `Query` est **obligatoire**
- `Mutation` et `Subscription` sont optionnels
- Chaque `RootType` doit contenir au moins un `Entrypoint`

**Options disponibles sur un RootType :**

```python
class Query(RootType, schema_name="MyQuery", extensions={"version": "1.0"}):
    """Description exposée dans le schéma."""
    ...
```

---

### 2.2 Les Entrypoints

Un `Entrypoint` est l'équivalent d'un "endpoint dans le schéma GraphQL". Il définit le resolver, le type de retour et les arguments d'une opération.

#### Référence par fonction (cas basique)

```python
from undine import Entrypoint, GQLInfo, RootType


class Query(RootType):
    @Entrypoint
    def greeting(self, info: GQLInfo, name: str = "World") -> str:
        """
        Retourne un message de bienvenue.

        :param name: Le prénom à saluer.
        """
        return f"Bonjour, {name} !"
```

> **Note :** Le paramètre `self` dans une méthode décorée `@Entrypoint` n'est **pas** une instance de `RootType` — c'est l'argument `root` du resolver GraphQL (valeur `None` par défaut). Il est conseillé de le renommer `root` pour éviter toute confusion.

**Arguments optionnels :**

```python
@Entrypoint
def greet(self, name: str | None = None) -> str:
    return f"Bonjour, {name or 'inconnu'} !"
```

**TypedDict en retour :**

```python
from typing import TypedDict


class UserInfo(TypedDict):
    id: int
    email: str


@Entrypoint
def me(self, info: GQLInfo) -> UserInfo:
    user = info.context.user
    return {"id": user.pk, "email": user.email}
```

---

#### Référence par QueryType (module 3)

```python
from undine import Entrypoint, QueryType, RootType

from .models import Task


class TaskType(QueryType[Task]): ...


class Query(RootType):
    # Un seul objet (par clé primaire)
    task = Entrypoint(TaskType)

    # Liste d'objets
    tasks = Entrypoint(TaskType, many=True)
```

---

### 2.3 Options avancées des Entrypoints

#### Cache côté serveur

```python
class Query(RootType):
    # Cache 60 secondes, commun à tous les utilisateurs
    @Entrypoint(cache_time=60)
    def public_data(self) -> str:
        return "donnée coûteuse"

    # Cache 30 secondes, par utilisateur
    @Entrypoint(cache_time=30, cache_per_user=True)
    def user_data(self, info: GQLInfo) -> str:
        return f"data de {info.context.user.pk}"
```

> ⚠️ Le caching requiert `undine.hooks.RequestCacheHook` dans `LIFECYCLE_HOOKS` (actif par défaut). Seules les réponses sans erreur sont mises en cache.

#### Complexité de la requête

```python
# Limite les requêtes trop "coûteuses"
# Configurer MAX_QUERY_COMPLEXITY dans UNDINE settings
tasks = Entrypoint(TaskType, many=True, complexity=5)
```

#### Nullabilité et limite

```python
# Rend l'entrypoint nullable
task = Entrypoint(TaskType, nullable=True)

# Limite le nombre d'objets retournés
tasks = Entrypoint(TaskType, many=True, limit=50)
```

#### Permissions au niveau Entrypoint

```python
from undine.exceptions import GraphQLPermissionError


class Query(RootType):
    task = Entrypoint(TaskType)

    @task.permissions
    def task_permissions(self, info: GQLInfo, instance) -> None:
        if not info.context.user.is_authenticated:
            raise GraphQLPermissionError("Authentification requise.")
```

#### Custom resolver

```python
from undine.optimizer import optimize_sync


class Query(RootType):
    task_by_name = Entrypoint(TaskType, nullable=True)

    @task_by_name.resolve
    def resolve_task_by_name(self, info: GQLInfo, name: str) -> Task | None:
        return optimize_sync(Task.objects.all(), info, name=name)
```

> ⚠️ Toujours appeler `optimize_sync` (ou `optimize_async`) dans un resolver custom qui retourne un modèle lié à un `QueryType`, afin de ne pas bypasser l'optimiseur.

#### Error as Data

```python
from graphql import GraphQLError


class Query(RootType):
    @Entrypoint(errors=[GraphQLError])
    def risky_op(self) -> str:
        raise GraphQLError("Quelque chose s'est mal passé")
        return "OK"
```

L'erreur apparaît alors comme données dans la réponse au lieu de polluer le tableau `errors` de la réponse GraphQL.

#### Visibilité conditionnelle (expérimental)

```python
# Activer dans settings : "EXPERIMENTAL_VISIBILITY_CHECKS": True

class Query(RootType):
    @Entrypoint
    def admin_only(self) -> str:
        return "secret"

    @admin_only.visible
    def admin_only_visible(self, request) -> bool:
        return request.user.is_superuser
```

---

### 2.4 Export du schéma SDL

```bash
python manage.py print_schema > schema.graphql
```

---

### Mise en garde

> ⚠️ **Ne jamais utiliser `@<entrypoint>.resolve` sur un `MutationType`** — cela bypasse le processus de mutation complet et toutes les hooks (permissions, validation, after) ne seront pas exécutées.

> ⚠️ Activer `ALLOW_DID_YOU_MEAN_SUGGESTIONS: False` (valeur par défaut) quand vous utilisez la visibilité conditionnelle, sinon des champs cachés peuvent apparaître dans les suggestions d'erreurs.

---

### Exercice d'application

Créez un `RootType` Query avec :
1. Un entrypoint `echo(message: str) -> str` qui retourne le message reçu
2. Un entrypoint `server_time() -> str` caché aux utilisateurs anonymes (`visible`)
3. Un entrypoint `cached_config() -> str` mis en cache 300 secondes

---

### Ressources complémentaires

- [Schema — Undine](https://mrthearman.github.io/undine/schema/)

---

## Module 3 — QueryTypes et Fields

### Objectifs du module

- Créer des `QueryType` pour exposer des modèles Django
- Maîtriser les différents types de `Field` (model, expression, fonction, relation)
- Configurer permissions, résolveurs personnalisés et optimisations par champ
- Utiliser l'auto-génération et le registre de `QueryType`

### Durée estimée : 2h30

### Concepts clés

- `QueryType[Model]`, `Field`, `GQLInfo`
- Auto-génération (`auto=True`, `exclude`)
- Relations FK, M2M, reverse
- `__permissions__`, `__filter_queryset__`, `__optimizations__`
- `Calculation`, `CalculationArgument`
- Registre, `register=False`

---

### 3.1 Modèles fil rouge

Nous utiliserons ces modèles tout au long de la formation :

```python
# myapp/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_projects"
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255, help_text="Nom de la tâche")
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )

    def __str__(self):
        return self.name


class Step(models.Model):
    name = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="steps")
```

---

### 3.2 QueryType basique

```python
# myapp/schema.py
from undine import Entrypoint, Field, QueryType, RootType, create_schema

from .models import Project, Step, Task


class TaskType(QueryType[Task]):
    pk = Field()
    name = Field()        # Récupère `help_text` du modèle comme description
    done = Field()
    created_at = Field()
```

Cela génère le type GraphQL suivant :

```graphql
type TaskType {
  pk: Int!
  name: String!    # Description: "Nom de la tâche"
  done: Boolean!
  createdAt: DateTime!
}
```

---

### 3.3 Auto-génération

```python
# Equivalent à la définition manuelle ci-dessus
class TaskType(QueryType[Task], auto=True):
    ...

# Avec exclusion de certains champs
class TaskType(QueryType[Task], auto=True, exclude=["created_at"]):
    ...
```

Pour activer globalement :

```python
# settings.py
UNDINE = {
    "AUTOGENERATION": True,
}
```

---

### 3.4 Types de références pour Field

#### Référence par nom de champ modèle

```python
class TaskType(QueryType[Task]):
    # Implicite : nom de l'attribut = nom du champ modèle
    name = Field()

    # Explicite par string
    name = Field("name")

    # Explicite par attribut du modèle (meilleure type safety)
    name = Field(Task.name)

    # Alias : expose "title" dans le schéma mais lit "name" dans le modèle
    title = Field("name")
```

#### Référence par expression Django ORM

```python
from django.db.models.functions import Upper
from django.db.models import OuterRef
from undine.utils.model_utils import SubqueryCount


class TaskType(QueryType[Task]):
    # Annotation calculée en base
    upper_name = Field(Upper("name"))

    # Sous-requête
    copies = Field(SubqueryCount(Task.objects.filter(name=OuterRef("name"))))
```

#### Référence par fonction (resolver Python)

```python
from undine import Field, GQLInfo, QueryType

from .models import Task


class TaskType(QueryType[Task]):
    @Field
    def summary(self, info: GQLInfo) -> str:
        """Retourne un résumé de la tâche."""
        # self = instance Task
        status = "✅" if self.done else "⏳"
        return f"{status} {self.name}"

    # Avec argument
    @Field
    def greeting(self, info: GQLInfo, *, lang: str = "fr") -> str:
        return f"Tâche: {self.name}" if lang == "fr" else f"Task: {self.name}"
```

> ⚠️ Si votre resolver utilise des champs du modèle non inclus dans la requête GraphQL, ajoutez une optimisation personnalisée (`@<field>.optimize`) pour les forcer à être chargés.

#### Référence par Calculation (expression + arguments)

```python
from django.db.models import Value
from undine import Calculation, CalculationArgument, DjangoExpression, Field, GQLInfo, QueryType


class PriorityScore(Calculation[int]):
    """Calcule un score de priorité basé sur un multiplicateur."""
    multiplier = CalculationArgument(int)

    def __call__(self, info: GQLInfo) -> DjangoExpression:
        # Expression annotée en base de données
        return Value(self.multiplier * 10)


class TaskType(QueryType[Task]):
    score = Field(PriorityScore)
```

Cela génère :

```graphql
type TaskType {
  score(multiplier: Int!): Int!
}
```

---

### 3.5 Relations entre QueryTypes

Undine résout automatiquement les relations entre `QueryType` en cherchant dans son registre.

```python
class ProjectType(QueryType[Project]):
    pk = Field()
    name = Field()
    tasks = Field()      # Relation inverse (related_name="tasks") → liste de TaskType


class TaskType(QueryType[Task]):
    pk = Field()
    name = Field()
    project = Field()    # FK → ProjectType (nullable si null=True)
    steps = Field()      # Relation inverse → liste de StepType
    assignee = Field()   # FK → type User auto-généré


class StepType(QueryType[Step]):
    pk = Field()
    name = Field()
    done = Field()
    task = Field()       # FK → TaskType
```

Schéma GraphQL généré :

```graphql
type ProjectType {
  pk: Int!
  name: String!
  tasks: [TaskType!]!
}

type TaskType {
  pk: Int!
  name: String!
  project: ProjectType
  steps: [StepType!]!
}
```

---

### 3.6 Permissions

#### Au niveau QueryType (toutes les instances)

```python
from undine.exceptions import GraphQLPermissionError


class TaskType(QueryType[Task]):
    name = Field()

    @classmethod
    def __permissions__(cls, instance: Task, info: GQLInfo) -> None:
        if not info.context.user.is_authenticated:
            raise GraphQLPermissionError("Authentification requise pour accéder aux tâches.")
```

#### Filtrage silencieux (sans lever d'erreur)

```python
class TaskType(QueryType[Task]):
    @classmethod
    def __filter_queryset__(cls, queryset, info: GQLInfo):
        # Chaque utilisateur ne voit que ses tâches assignées
        if not info.context.user.is_authenticated:
            return queryset.none()
        return queryset.filter(assignee=info.context.user)
```

> ⚠️ Avec `__filter_queryset__`, les `Entrypoints` ou `Fields` utilisant ce `QueryType` doivent être marqués `nullable=True` pour les relations "to-one", car l'objet peut être filtré.

#### Au niveau Field

```python
class TaskType(QueryType[Task]):
    name = Field()

    @name.permissions
    def name_permissions(self, info: GQLInfo, value: str) -> None:
        if not info.context.user.is_authenticated:
            raise GraphQLPermissionError("Nom non accessible.")
```

---

### 3.7 Resolver et optimisation custom par Field

```python
class TaskType(QueryType[Task]):
    name = Field()

    # Override du resolver
    @name.resolve
    def resolve_name(self, info: GQLInfo) -> str:
        return self.name.strip().upper()

    # Override de l'optimisation (force le chargement du champ "name")
    @name.optimize
    def optimize_name(self, data, info: GQLInfo) -> None:
        data.only_fields.add("name")
```

---

### 3.8 QueryType : options supplémentaires

```python
class TaskType(
    QueryType[Task],
    schema_name="Task",        # Nom dans le schéma GraphQL
    auto=True,
    exclude=["created_at"],
    cache_time=30,             # Durée de cache pour ce type
    cache_per_user=True,
    extensions={"version": "1"},
):
    """Description du type Task."""
    ...
```

#### Plusieurs QueryTypes pour le même modèle

```python
class TaskType(QueryType[Task]):
    pk = Field()
    name = Field()

# Pas enregistré → ne conflicte pas avec TaskType
class TaskSummaryType(QueryType[Task], register=False):
    pk = Field()
    name = Field()
```

---

### Mise en garde

> ⚠️ **Le registre n'accepte qu'un seul `QueryType` par modèle.** Si vous en créez deux pour le même modèle sans `register=False`, une erreur sera levée au démarrage.

> ⚠️ **Un `MutationType` cherche son type de sortie dans le registre** — il faut donc toujours avoir un `QueryType` enregistré pour chaque modèle que vous mutez, même si ce `QueryType` n'est pas exposé dans un `Entrypoint`.

---

### Exercice d'application

Pour les modèles `Project`, `Task` et `Step` du fil rouge :

1. Créez un `QueryType` pour chacun avec les champs pertinents
2. Liez les relations entre eux
3. Ajoutez une permission sur `TaskType` : seuls les utilisateurs authentifiés peuvent accéder
4. Ajoutez un champ calculé `step_count` sur `TaskType` utilisant une sous-requête `SubqueryCount`
5. Exposez les entrypoints `project`, `projects`, `task`, `tasks` dans un `RootType Query`

---

### Ressources complémentaires

- [Queries — Undine](https://mrthearman.github.io/undine/queries/)

---

## Module 4 — Filtrage, tri et pagination

### Objectifs du module

- Créer des `FilterSet` pour filtrer les résultats de `QueryType`
- Utiliser les opérateurs logiques (`AND`, `OR`, `NOT`, `XOR`)
- Créer des `OrderSet` pour trier les résultats
- Implémenter la pagination par offset et par curseur (Relay Connection)

### Durée estimée : 2h

### Concepts clés

- `FilterSet[Model]`, `Filter`, `lookup`
- Opérateurs logiques `AND`, `OR`, `NOT`, `XOR`
- `OrderSet[Model]`, `Order`, `null_placement`
- `Connection`, `Node` (Relay)

---

### 4.1 FilterSet

```python
from undine import Filter, FilterSet, Field, QueryType

from .models import Task


class TaskFilterSet(FilterSet[Task]):
    # lookup correspond à un ORM lookup Django
    name = Filter(lookup="icontains")     # ?filter.name → Task.name__icontains
    done = Filter()                        # ?filter.done → Task.done (exact)
    created_after = Filter(
        lookup="gte",
        field_name="created_at",           # Champ modèle différent du nom du filtre
    )


class TaskType(QueryType[Task], filterset=TaskFilterSet):
    pk = Field()
    name = Field()
    done = Field()
    created_at = Field()
```

Schéma généré :

```graphql
input TaskFilterSet {
  name: String
  done: Boolean
  createdAfter: DateTime
  AND: TaskFilterSet
  OR: TaskFilterSet
  NOT: TaskFilterSet
  XOR: TaskFilterSet
}
```

#### Auto-génération de FilterSet

```python
class TaskFilterSet(FilterSet[Task], auto=True):
    ...
```

---

### 4.2 Utilisation dans les requêtes GraphQL

**Filtre simple :**

```graphql
query {
  tasks(filter: { name: "rapport" }) {
    pk
    name
  }
}
```

**Filtre combiné (AND implicite) :**

```graphql
query {
  tasks(filter: { name: "rapport", done: false }) {
    pk
    name
  }
}
```

**Opérateur OR :**

```graphql
query {
  tasks(filter: { OR: { name: "rapport", done: false } }) {
    pk
    name
  }
}
```

**Combinaisons imbriquées :**

```graphql
query {
  tasks(
    filter: {
      AND: {
        name: "rapport"
        OR: { done: false, assignee: null }
      }
    }
  ) {
    pk
    name
  }
}
```

---

### 4.3 OrderSet

```python
from undine import Order, OrderSet


class TaskOrderSet(OrderSet[Task]):
    id = Order()
    name = Order(null_placement="last")    # Les nulls à la fin
    created_at = Order()


class TaskType(QueryType[Task], orderset=TaskOrderSet):
    pk = Field()
    name = Field()
    created_at = Field()
```

Schéma généré :

```graphql
enum TaskOrderSet {
  idAsc
  idDesc
  nameAsc
  nameDesc
  createdAtAsc
  createdAtDesc
}
```

**Utilisation :**

```graphql
query {
  tasks(orderBy: [nameAsc, idDesc]) {
    pk
    name
  }
}
```

---

### 4.4 Pagination par curseur — Relay Connection

Undine supporte la spécification Relay Connection pour la pagination par curseur.

```python
from undine.relay import Connection, Node


# Déclarer que TaskType supporte les IDs globaux Relay
@Node
class TaskType(QueryType[Task]):
    pk = Field()
    name = Field()
    done = Field()


class Query(RootType):
    # Pagination par curseur
    tasks = Entrypoint(Connection(TaskType))

    # Pagination simple (liste)
    all_tasks = Entrypoint(TaskType, many=True)
```

**Requête paginée :**

```graphql
query {
  tasks(first: 10, after: "cursor_opaque") {
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
    edges {
      cursor
      node {
        pk
        name
      }
    }
  }
}
```

**IDs globaux Relay (`Node`) :**

```graphql
query {
  # Lookup par ID global Relay (encapsule le type + pk)
  node(id: "VGFza1R5cGU6MQ==") {
    ... on TaskType {
      pk
      name
    }
  }
}
```

---

### Mise en garde

> ⚠️ **Les opérateurs logiques (`AND`, `OR`, `NOT`, `XOR`) sont automatiquement ajoutés** à tous les `FilterSet` — pas besoin de les déclarer manuellement.

> ⚠️ Pour utiliser `Connection`, le `QueryType` doit être décoré avec `@Node` (interface Relay). Cela ajoute un champ `id` d'ID global opaque.

> ⚠️ Les valeurs vides (`None`, `""`, `[]`, `{}`) sont ignorées par défaut dans les `Filter`. Ce comportement est configurable via le paramètre `empty_values`.

---

### Exercice d'application

Pour les `Task` et `Project` du fil rouge :

1. Créez un `TaskFilterSet` avec les filtres : `name` (icontains), `done`, `project_id`, et `created_after`
2. Créez un `TaskOrderSet` avec les ordres : `pk`, `name`, `created_at`
3. Ajoutez la pagination par curseur (`Connection`) à l'entrypoint `tasks`
4. Testez dans GraphiQL :
   - Les tâches non terminées dont le nom contient "bug"
   - Triées par date décroissante

---

### Ressources complémentaires

- [Filtering — Undine](https://mrthearman.github.io/undine/filtering/)
- [Ordering — Undine](https://mrthearman.github.io/undine/ordering/)
- [Pagination — Undine](https://mrthearman.github.io/undine/pagination/)
- [Global Object IDs — Undine](https://mrthearman.github.io/undine/global-object-ids/)

---

## Module 5 — Mutations et gestion des données

### Objectifs du module

- Créer des `MutationType` pour les opérations create, update, delete
- Utiliser l'auto-génération des `Input`
- Maîtriser les mutations bulk
- Comprendre le mécanisme de détermination automatique du `kind`

### Durée estimée : 2h

### Concepts clés

- `MutationType[Model]`, `Input`, `kind`
- Conventions de nommage (create/update/delete)
- `many=True` pour les mutations bulk
- `__after__`, `__mutate__`, `__bulk_mutate__`
- `MUTATION_INSTANCE_LIMIT`

---

### 5.1 Mutations CRUD

#### Create

```python
from undine import Entrypoint, Field, Input, MutationType, QueryType, RootType, create_schema

from .models import Task


class TaskType(QueryType[Task]):
    pk = Field()
    name = Field()
    done = Field()
    created_at = Field()


# Le mot "Create" dans le nom détermine le kind automatiquement
class TaskCreateMutation(MutationType[Task]):
    name = Input()
    done = Input(default_value=False)
```

Input GraphQL généré :

```graphql
input TaskCreateMutation {
  name: String!
  done: Boolean! = false
}
```

#### Update

```python
class TaskUpdateMutation(MutationType[Task]):
    pk = Input()       # Requis : identifie l'instance à modifier
    name = Input()     # Optionnel : partial update par défaut
    done = Input()
```

Input GraphQL généré (partial update) :

```graphql
input TaskUpdateMutation {
  pk: Int!
  name: String      # Nullable = optionnel
  done: Boolean
}
```

#### Delete

```python
class TaskDeleteMutation(MutationType[Task]):
    pk = Input()
```

Input GraphQL généré :

```graphql
input TaskDeleteMutation {
  pk: Int!
}
```

---

### 5.2 Auto-génération des Inputs

```python
# Génère automatiquement tous les Inputs depuis le modèle
class TaskCreateMutation(MutationType[Task], auto=True):
    ...

# Avec exclusion
class TaskCreateMutation(MutationType[Task], auto=True, exclude=["created_at"]):
    ...
```

**Règles d'auto-génération :**
- `create` : champs non-auto, avec valeur par défaut si disponible
- `update` : pk inclus et requis, autres champs nullable (partial update)
- `delete` : uniquement pk

---

### 5.3 Enregistrement dans le schéma

```python
class Mutation(RootType):
    create_task = Entrypoint(TaskCreateMutation)
    update_task = Entrypoint(TaskUpdateMutation)
    delete_task = Entrypoint(TaskDeleteMutation)

    # Mutations bulk
    bulk_create_tasks = Entrypoint(TaskCreateMutation, many=True)
    bulk_update_tasks = Entrypoint(TaskUpdateMutation, many=True)


schema = create_schema(query=Query, mutation=Mutation)
```

**Test create :**

```graphql
mutation {
  createTask(input: { name: "Nouvelle tâche" }) {
    pk
    name
    done
  }
}
```

**Test bulk create :**

```graphql
mutation {
  bulkCreateTasks(
    input: [
      { name: "Tâche A" }
      { name: "Tâche B", done: true }
    ]
  ) {
    pk
    name
  }
}
```

> ⚠️ Le nombre maximal d'objets dans une mutation bulk est contrôlé par `MUTATION_INSTANCE_LIMIT` dans les settings (défaut : à vérifier dans votre version d'Undine).

---

### 5.4 Post-mutation avec `__after__`

```python
from typing import Any


class TaskCreateMutation(MutationType[Task]):
    name = Input()

    @classmethod
    def __after__(cls, instance: Task, info: GQLInfo, input_data: dict[str, Any]) -> None:
        # Envoi d'un email de notification, log, etc.
        print(f"Tâche créée : {instance.pk} — {instance.name}")
```

---

### 5.5 Mutation entièrement custom

```python
class TaskArchiveMutation(MutationType[Task], kind="custom"):
    pk = Input()

    @classmethod
    def __mutate__(cls, instance: Task, info: GQLInfo, input_data: dict[str, Any]) -> Task:
        # instance existe déjà car pk est présent
        instance.archived = True
        instance.save(update_fields=["archived"])
        return instance
```

> Pour les mutations `kind="custom"` :
> - L'auto-génération est désactivée
> - Si `pk` est présent dans les Inputs, la mutation se comporte comme un update (charge l'instance existante)
> - Sinon, elle se comporte comme un create (nouvelle instance)

---

### Mise en garde

> ⚠️ **Toujours créer un `QueryType` pour chaque modèle que vous mutez**, même s'il n'est pas utilisé dans des `Entrypoints` de lecture. Le `MutationType` en a besoin comme type de sortie.

> ⚠️ **Le mot-clé dans le nom du `MutationType`** (`create`, `update`, `delete`) détermine automatiquement le `kind`. En cas d'ambiguïté, utilisez toujours `kind="create"` explicitement.

---

### Exercice d'application

Pour le modèle `Project` :

1. Créez `ProjectCreateMutation`, `ProjectUpdateMutation`, `ProjectDeleteMutation`
2. Ajoutez un bulk create
3. Implémentez un `__after__` sur la création qui affiche un log
4. Testez toutes les mutations dans GraphiQL

---

### Ressources complémentaires

- [Mutations — Undine](https://mrthearman.github.io/undine/mutations/)

---

## Module 6 — Mutations avancées : relations, validation, permissions

### Objectifs du module

- Utiliser les mutations `related` pour gérer les relations
- Implémenter permissions et validation au niveau mutation et input
- Maîtriser les options avancées des `Input`

### Durée estimée : 2h

### Concepts clés

- `kind="related"`, actions (null, delete, ignore)
- `__permissions__`, `__validate__` sur `MutationType`
- `@input.permissions`, `@input.validate`
- `Input` hidden, input-only, default_value, required

---

### 6.1 Mutations liées (`related`)

```python
from undine import Input, MutationType

from .models import Project, Task


class TaskProjectInput(MutationType[Project], kind="related"):
    pk = Input()      # Optionnel : lier un projet existant
    name = Input()    # Optionnel : créer ou renommer le projet


class TaskCreateMutation(MutationType[Task]):
    name = Input()
    done = Input(default_value=False)
    project = Input(TaskProjectInput)
```

Cela permet dans une seule mutation :

**Créer tâche + nouveau projet :**

```graphql
mutation {
  createTask(input: { name: "Bug fix", project: { name: "Sprint 5" } }) {
    pk
    project { pk name }
  }
}
```

**Créer tâche + lier projet existant :**

```graphql
mutation {
  createTask(input: { name: "Bug fix", project: { pk: 3 } }) {
    pk
    project { pk name }
  }
}
```

**Créer tâche + lier ET renommer projet :**

```graphql
mutation {
  createTask(input: { name: "Bug fix", project: { pk: 3, name: "Sprint 6" } }) {
    pk
    project { pk name }
  }
}
```

---

### 6.2 Permissions sur MutationType

```python
from typing import Any

from undine import GQLInfo, Input, MutationType
from undine.exceptions import GraphQLPermissionError

from .models import Task


class TaskCreateMutation(MutationType[Task]):
    name = Input()

    @classmethod
    def __permissions__(cls, instance: Task, info: GQLInfo, input_data: dict[str, Any]) -> None:
        if not info.context.user.is_staff:
            raise GraphQLPermissionError("Seuls les membres staff peuvent créer des tâches.")
```

> **Note signature :**
> - Pour `create` : `instance` est une **nouvelle instance** sans pk
> - Pour `update`/`delete` : `instance` est l'**instance existante** chargée depuis la BDD

---

### 6.3 Validation sur MutationType

```python
from undine.exceptions import GraphQLValidationError


class TaskCreateMutation(MutationType[Task]):
    name = Input()

    @classmethod
    def __validate__(cls, instance: Task, info: GQLInfo, input_data: dict[str, Any]) -> None:
        if len(input_data.get("name", "")) < 3:
            raise GraphQLValidationError("Le nom doit contenir au moins 3 caractères.")

        if input_data.get("done") and not info.context.user.is_superuser:
            raise GraphQLValidationError(
                "Seuls les superusers peuvent créer des tâches déjà terminées."
            )
```

---

### 6.4 Permissions et validation sur Input

```python
class TaskCreateMutation(MutationType[Task]):
    name = Input()
    done = Input()

    # Permission au niveau du champ "done"
    @done.permissions
    def done_permissions(self, info: GQLInfo, value: bool) -> None:
        if not info.context.user.is_superuser:
            raise GraphQLPermissionError("Seuls les superusers peuvent définir done.")

    # Validation au niveau du champ "name"
    @name.validate
    def validate_name(self, info: GQLInfo, value: str) -> None:
        if value.startswith(" "):
            raise GraphQLValidationError("Le nom ne peut pas commencer par un espace.")
```

> ⚠️ Les permissions sur un `Input` ne sont vérifiées que lorsque la valeur est **non-default** — si l'utilisateur envoie la valeur par défaut, la permission n'est pas testée.

---

### 6.5 Options avancées des Input

```python
class TaskCreateMutation(MutationType[Task]):
    name = Input()

    # Valeur par défaut
    done = Input(default_value=False)

    # Input requis (override l'inférence)
    priority = Input(required=True)

    # Input caché (non visible dans le schéma, rempli côté serveur)
    created_by = Input(hidden=True)

    # Input seulement utilisé en entrée, pas reflété dans le type de sortie
    raw_password = Input(input_only=True)
```

**Input caché — exemple avec `__mutate__` :**

```python
class TaskCreateMutation(MutationType[Task]):
    name = Input()
    created_by = Input(hidden=True)

    @classmethod
    def __mutate__(cls, instance: Task, info: GQLInfo, input_data: dict[str, Any]) -> Task:
        input_data["created_by_id"] = info.context.user.pk
        instance.__dict__.update(input_data)
        instance.save()
        return instance
```

---

### 6.6 Réponse d'erreur type

```json
{
  "data": null,
  "errors": [
    {
      "message": "Seuls les membres staff peuvent créer des tâches.",
      "locations": [{ "line": 2, "column": 3 }],
      "path": ["createTask"],
      "extensions": {
        "status_code": 403,
        "error_code": "PERMISSION_DENIED"
      }
    }
  ]
}
```

---

### Mise en garde

> ⚠️ Pour les mutations `update` et `delete`, l'instance est chargée depuis la base avant d'appeler `__permissions__` et `__validate__` — gardez cela en tête pour les performances.

> ⚠️ Les `related` mutations supportent les mêmes hooks (`__permissions__`, `__validate__`, `__after__`) que les mutations normales.

---

### Exercice d'application

1. Créez une mutation `TaskUpdateMutation` qui :
   - Valide que le nom fait au moins 3 caractères
   - Refuse la mise à jour si `done=True` et que l'utilisateur n'est pas le propriétaire du projet
   - Accepte un input `related` `project` pour réassigner la tâche

2. Créez une mutation `StepCreateMutation` liée à `Task` via un input `related`

---

### Ressources complémentaires

- [Mutations — Undine](https://mrthearman.github.io/undine/mutations/)

---

## Module 7 — Temps réel avec les Subscriptions

### Objectifs du module

- Configurer l'environnement async et choisir le protocole de transport
- Créer des subscriptions avec `AsyncGenerator`
- Utiliser les subscriptions basées sur les signaux Django
- Gérer les permissions dans les subscriptions

### Durée estimée : 2h

### Concepts clés

- Async support (`ASYNC: True`)
- WebSockets (`django-channels`), SSE, Multipart HTTP
- `AsyncGenerator`, `AsyncIterable`
- `ModelCreateSubscription`, `ModelUpdateSubscription`, `ModelDeleteSubscription`

---

### 7.1 Configuration async

```python
# settings.py
UNDINE = {
    "ASYNC": True,
    "GRAPHIQL_ENABLED": True,
    "ALLOW_INTROSPECTION_QUERIES": True,
    "SCHEMA": "myapp.schema.schema",
}
```

Pour les WebSockets (recommandé pour la production) :

```bash
pip install django-channels channels-redis daphne
```

```python
# settings.py
INSTALLED_APPS = [
    "daphne",  # En premier pour les WebSockets
    "channels",
    "undine",
    # ...
]

ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

```python
# config/asgi.py
import os
from django.core.asgi import get_asgi_application
from undine.integrations.channels import GraphQLProtocolTypeRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = GraphQLProtocolTypeRouter(
    http=get_asgi_application(),
)
```

---

### 7.2 Subscription avec AsyncGenerator

```python
import asyncio
from collections.abc import AsyncGenerator

from undine import Entrypoint, GQLInfo, RootType, create_schema


class Subscription(RootType):
    @Entrypoint
    async def countdown(self, info: GQLInfo) -> AsyncGenerator[int, None]:
        """Compte à rebours de 10 à 0."""
        for i in range(10, -1, -1):
            yield i
            await asyncio.sleep(1)


schema = create_schema(query=Query, subscription=Subscription)
```

**Écoute dans GraphiQL :**

```graphql
subscription {
  countdown
}
```

---

### 7.3 Subscriptions basées sur les signaux Django

Undine fournit des classes prêtes à l'emploi basées sur les signaux `post_save` et `post_delete` :

```python
from undine.subscriptions import (
    ModelCreateSubscription,
    ModelDeleteSubscription,
    ModelUpdateSubscription,
)

from .schema_types import TaskType


class Subscription(RootType):
    # Notifié à chaque création de Task
    task_created = Entrypoint(ModelCreateSubscription(TaskType))

    # Notifié à chaque mise à jour de Task
    task_updated = Entrypoint(ModelUpdateSubscription(TaskType))

    # Notifié à chaque suppression de Task
    task_deleted = Entrypoint(ModelDeleteSubscription(TaskType))
```

**Utilisation :**

```graphql
subscription {
  taskCreated {
    pk
    name
    done
  }
}
```

---

### 7.4 Subscription avec AsyncIterable

```python
from collections.abc import AsyncIterable
from undine import Entrypoint, GQLInfo, RootType

from .models import Task


class Subscription(RootType):
    @Entrypoint
    async def task_feed(self, info: GQLInfo) -> AsyncIterable[Task]:
        """Flux en temps réel des tâches."""
        # Implémentation avec un canal de message (ex: Redis Pub/Sub)
        async for task in some_async_task_stream():
            yield task
```

---

### 7.5 Permissions dans les subscriptions

Les subscriptions supportent les mêmes mécanismes de permission que les queries.

```python
from undine.exceptions import GraphQLPermissionError


class Subscription(RootType):
    task_created = Entrypoint(ModelCreateSubscription(TaskType))

    @task_created.permissions
    def task_created_permissions(self, info: GQLInfo, instance: Task) -> None:
        if not info.context.user.is_authenticated:
            raise GraphQLPermissionError("Authentification requise pour les subscriptions.")
```

---

### 7.6 Choix du protocole de transport

| Protocole | Setup requis | Avantages | Inconvénients |
|---|---|---|---|
| **WebSockets** | django-channels + Redis | Bidirectionnel, large support | Plus complexe à déployer |
| **SSE Distinct** | Async seul | Simple, HTTP natif | 6 connexions max en HTTP/1.1 |
| **SSE Single** | channels + Redis | Multiplexage, une seule connexion | Auth requise |
| **Multipart HTTP** | Async seul | Compatible Apollo Router | HTTP/1.1 limité |

---

### Mise en garde

> ⚠️ **Les subscriptions nécessitent `ASYNC: True`** dans les settings Undine. Sans cela, les resolvers async ne fonctionneront pas.

> ⚠️ **SSE en Single Connection mode requiert Redis et les sessions Django**. En HTTP/1.1, les navigateurs limitent à 6 connexions SSE par domaine — utilisez HTTP/2 en production.

> ⚠️ `ModelCreateSubscription` et ses variantes se basent sur les signaux Django (`post_save`, `post_delete`). Si vous effectuez des `bulk_update` ou des `update()` sur un queryset, ces signaux ne sont pas émis.

---

### Exercice d'application

1. Configurez le support async dans votre projet
2. Créez une subscription `projectTaskCreated(project_id: Int!)` qui notifie à chaque création de `Task` dans un projet spécifique
3. Ajoutez une permission : seuls les membres authentifiés peuvent s'abonner

---

### Ressources complémentaires

- [Subscriptions — Undine](https://mrthearman.github.io/undine/subscriptions/)
- [Async Support — Undine](https://mrthearman.github.io/undine/async/)
- [Integrations — Undine](https://mrthearman.github.io/undine/integrations/)

---

## Module 8 — Optimisation des performances

### Objectifs du module

- Comprendre et résoudre le problème N+1 et le sur-fetching
- Maîtriser le fonctionnement de l'optimiseur automatique d'Undine
- Ajouter des optimisations manuelles avec `__optimizations__` et `@field.optimize`
- Utiliser les DataLoaders pour les appels externes

### Durée estimée : 2h30

### Concepts clés

- Problème N+1, sur-fetching (over-fetching)
- `OptimizationData`, `only_fields`, `select_related`, `prefetch_related`
- `optimize_sync`, `optimize_async`
- `DataLoader`, batch loading

---

### 8.1 Le problème N+1

Sans optimisation, une requête GraphQL sur 100 tâches avec leurs projets génèrerait :
- 1 requête pour les 100 tâches
- 100 requêtes pour les projets (1 par tâche)
- **Total : 101 requêtes !**

**L'optimiseur d'Undine résout cela automatiquement** en analysant la requête avant exécution et en générant les `select_related` / `prefetch_related` appropriés. Pour la requête ci-dessus, il ne ferait que **2 requêtes** au total.

---

### 8.2 L'optimiseur automatique

L'optimiseur s'active automatiquement pour tous les `Entrypoints` basés sur des `QueryType`. Il :

1. Analyse le document GraphQL entrant
2. Parcourt les champs demandés et leurs relations
3. Génère les optimisations QuerySet (`only()`, `select_related()`, `prefetch_related()`, `annotate()`)
4. Exécute la requête optimisée

**Sur-fetching** : via `QuerySet.only()`, seuls les champs effectivement demandés dans la requête GraphQL sont chargés depuis la base de données.

Pour désactiver `only()` :

```python
# settings.py
UNDINE = {
    "DISABLE_ONLY_FIELDS_OPTIMIZATION": True,
}
```

---

### 8.3 Optimisations manuelles

Nécessaires quand vos resolvers ou permissions accèdent à des champs **non demandés dans la requête GraphQL**.

#### Au niveau QueryType

```python
from undine import GQLInfo, QueryType
from undine.optimizer import OptimizationData

from .models import Task


class TaskType(QueryType[Task]):
    name = Field()

    @classmethod
    def __optimizations__(cls, data: OptimizationData, info: GQLInfo) -> None:
        # Forcer le chargement du champ "created_at" pour les permissions
        data.only_fields.add("created_at")

        # Forcer le select_related sur "project" (relation FK)
        data.add_select_related("project", query_type=ProjectType)

        # Forcer le prefetch_related sur "steps" (relation inverse)
        data.add_prefetch_related("steps", query_type=StepType)
```

#### Au niveau Field

```python
class TaskType(QueryType[Task]):
    @Field
    def display_name(self, info: GQLInfo) -> str:
        # Ce resolver a besoin des champs "name" et "done"
        return f"{'✅' if self.done else '⏳'} {self.name}"

    @display_name.optimize
    def optimize_display_name(self, data: OptimizationData, info: GQLInfo) -> None:
        data.only_fields.add("name")
        data.only_fields.add("done")
```

---

### 8.4 Structure de OptimizationData

| Attribut | Type | Utilisation |
|---|---|---|
| `only_fields` | `set[str]` | Champs à inclure dans `QuerySet.only()` |
| `annotations` | `dict` | Expressions ORM à annoter |
| `aliases` | `dict` | Expressions ORM à aliaser |
| `select_related` | `dict` | FK / One-to-One à charger en JOIN |
| `prefetch_related` | `dict` | Many-to-Many / reverse FK à prefetch |
| `filters` | liste de `Q` | Filtres à appliquer |
| `order_by` | liste | Ordres à appliquer |

---

### 8.5 Optimizer dans les resolvers custom

Quand vous écrivez un resolver `Entrypoint` custom qui retourne un modèle lié à un `QueryType`, appelez toujours l'optimiseur :

```python
from undine.optimizer import optimize_sync, optimize_async


class Query(RootType):
    task_by_name = Entrypoint(TaskType, nullable=True)

    @task_by_name.resolve
    def resolve_task_by_name(self, info: GQLInfo, name: str) -> Task | None:
        # optimize_sync analyse la requête et optimise le queryset
        return optimize_sync(Task.objects.all(), info, name=name)


# Version async
class Query(RootType):
    @Entrypoint
    async def task_by_name_async(self, info: GQLInfo, name: str) -> Task | None:
        return await optimize_async(Task.objects.all(), info, name=name)
```

---

### 8.6 DataLoaders

Les DataLoaders sont utiles pour **les appels externes** (API tierces, cache Redis, I/O asynchrone) où l'optimiseur Django ORM ne peut pas intervenir. Ils regroupent plusieurs appels individuels en un seul appel batch.

```python
from undine.dataloaders import DataLoader


class UserAvatarLoader(DataLoader):
    """Charge les avatars depuis une API externe en batch."""

    async def batch_load(self, keys: list[int]) -> list[str | None]:
        # Un seul appel API pour tous les user_ids
        avatars = await fetch_avatars_from_cdn(keys)
        return [avatars.get(key) for key in keys]


# Utilisation dans un Field
class TaskType(QueryType[Task]):
    @Field
    async def assignee_avatar(self, info: GQLInfo) -> str | None:
        if self.assignee_id is None:
            return None
        loader = UserAvatarLoader.for_request(info)
        return await loader.load(self.assignee_id)
```

**Principe de fonctionnement :**
1. Lors de la résolution de 10 tâches, chaque tâche appelle `loader.load(user_id)`
2. Le DataLoader regroupe tous les `user_id` en un batch
3. `batch_load` est appelé une seule fois avec la liste complète
4. Les résultats sont redistribués à chaque tâche

---

### Mise en garde

> ⚠️ **Ne jamais accéder à un champ d'un modèle dans un resolver custom sans s'assurer qu'il est chargé.** Si vous utilisez `Task.name` dans un resolver mais que `name` n'est pas dans la requête GraphQL, l'optimiseur ne le chargera peut-être pas → requête N+1 silencieuse.

> ⚠️ **`optimize_sync` / `optimize_async` doivent être appelés dans les resolvers custom** qui retournent des instances de modèles utilisées par des `QueryType`. Sans cela, l'optimiseur ne sera pas déclenché.

> ⚠️ Les DataLoaders ne s'appliquent qu'aux contextes **async**. Pour un projet entièrement synchrone, utilisez `select_related` / `prefetch_related` manuels.

---

### Exercice d'application

1. Activez `django-debug-toolbar` et observez les requêtes générées par votre API sans optimisation
2. Vérifiez que l'optimiseur automatique réduit les requêtes
3. Créez un `Field` `display_name` avec optimisation manuelle sur `TaskType`
4. Implémentez un DataLoader pour charger les emails des assignees depuis un service externe simulé

---

### Ressources complémentaires

- [Optimizer — Undine](https://mrthearman.github.io/undine/optimizer/)
- [DataLoaders — Undine](https://mrthearman.github.io/undine/dataloaders/)
- [Async Support — Undine](https://mrthearman.github.io/undine/async/)

---

## Module 9 — Sécurité, documents persistés et bonnes pratiques

### Objectifs du module

- Sécuriser les endpoints GraphQL contre les attaques courantes
- Utiliser les documents persistés (persisted queries)
- Appliquer le pattern "Error as Data"
- Adopter les bonnes pratiques de nommage et de documentation

### Durée estimée : 2h

### Concepts clés

- CSRF, `ALLOW_INTROSPECTION_QUERIES`, complexité max
- Documents persistés, mode "allow-list"
- `errors` (Error as Data), `GraphQLPermissionError`, `GraphQLValidationError`
- Visibilité conditionnelle (`EXPERIMENTAL_VISIBILITY_CHECKS`)

---

### 9.1 Sécurisation de l'endpoint

#### Configuration de sécurité minimale en production

```python
# settings.py
UNDINE = {
    "SCHEMA": "myapp.schema.schema",

    # Désactiver l'introspection en production
    "ALLOW_INTROSPECTION_QUERIES": False,

    # Désactiver les suggestions "did you mean"
    "ALLOW_DID_YOU_MEAN_SUGGESTIONS": False,

    # Limiter la complexité des requêtes (prévient les attaques DoS)
    "MAX_QUERY_COMPLEXITY": 100,

    # Limiter la profondeur des requêtes imbriquées
    # (via ADDITIONAL_VALIDATION_RULES avec une règle custom)
}
```

#### CSRF pour les file uploads

```python
UNDINE = {
    "FILE_UPLOAD_ENABLED": True,
    # Activer la protection CSRF sur l'endpoint GraphQL si les uploads sont activés
}
```

---

### 9.2 Documents persistés (Persisted Documents)

Les documents persistés permettent de **pré-enregistrer les requêtes GraphQL autorisées** sur le serveur, empêchant l'exécution de requêtes arbitraires (mode "allow-list").

```python
# settings.py
UNDINE = {
    "PERSISTED_DOCUMENTS_ONLY": True,  # N'accepte que les documents persistés
}
```

**Fonctionnement :**
1. Lors du déploiement, les requêtes autorisées sont enregistrées côté serveur
2. Les clients envoient un hash au lieu du document GraphQL complet
3. Le serveur vérifie le hash et exécute la requête correspondante
4. Toute requête inconnue est rejetée

Avantages : sécurité renforcée, bandwidth réduit côté client, caching optimisé.

Pour la configuration complète : [Persisted Documents — Undine](https://mrthearman.github.io/undine/persisted-documents/)

---

### 9.3 Error as Data (pattern avancé)

Par défaut, les erreurs GraphQL "cascadent" vers le haut jusqu'à un champ nullable. Le pattern "Error as Data" encapsule l'erreur comme valeur dans le type de retour.

```python
import random
from graphql import GraphQLError
from undine import Field, QueryType
from .models import Task


class TaskNotFoundError(Exception):
    @staticmethod
    def graphql_fields():
        from graphql import GraphQLField, GraphQLNonNull, GraphQLString
        return {"message": GraphQLField(GraphQLNonNull(GraphQLString))}

    @staticmethod
    def graphql_resolve(root, info, **kwargs):
        return {"message": str(root)}


class TaskType(QueryType[Task]):
    @Field(errors=[TaskNotFoundError])
    def external_status(self) -> str:
        """Statut depuis un service externe."""
        if random.random() > 0.8:
            raise TaskNotFoundError(f"Tâche {self.pk} introuvable dans le service externe")
        return "active"
```

Schéma généré :

```graphql
union TaskTypeExternalStatus = TaskTypeExternalStatusValue | TaskNotFoundError

type TaskType {
  externalStatus: TaskTypeExternalStatus!
}
```

**Réponse succès :**

```json
{
  "data": {
    "task": {
      "externalStatus": {
        "__typename": "TaskTypeExternalStatusValue",
        "value": "active"
      }
    }
  }
}
```

---

### 9.4 Règles de validation custom

```python
# settings.py
UNDINE = {
    "ADDITIONAL_VALIDATION_RULES": [
        "myapp.validation.MaxDepthRule",
        "myapp.validation.NoIntrospectionRule",
    ],
}
```

```python
# myapp/validation.py
from graphql.validation import ASTValidationRule
from graphql import GraphQLError


class MaxDepthRule(ASTValidationRule):
    """Limite la profondeur des requêtes à 5 niveaux."""

    def enter_field(self, node, *args):
        # Logique de vérification de profondeur
        pass
```

---

### 9.5 Bonnes pratiques

#### Nommage

| Élément | Convention | Exemple |
|---|---|---|
| QueryType | PascalCase + Type | `TaskType`, `ProjectType` |
| MutationType | PascalCase + kind + Mutation | `TaskCreateMutation` |
| FilterSet | PascalCase + FilterSet | `TaskFilterSet` |
| Entrypoints | camelCase (auto) | `createTask`, `tasks` |

#### Documentation dans le schéma

```python
class TaskType(QueryType[Task]):
    """Représente une tâche dans un projet."""

    name = Field(description="Le nom complet de la tâche.")

    @Field
    def status(self) -> str:
        """
        Statut calculé de la tâche.

        :returns: 'done', 'in_progress' ou 'todo'
        """
        return "done" if self.done else "todo"
```

#### Versionnement

GraphQL préconise une évolution non-versionnée du schéma (ajout de champs, jamais suppression). Pour déprécier des champs :

```python
class TaskType(QueryType[Task]):
    # Marquer un champ comme deprecated sans le supprimer
    old_field = Field(deprecation_reason="Utilisez `name` à la place.")
    name = Field()
```

---

### Mise en garde

> ⚠️ **Ne jamais activer `ALLOW_INTROSPECTION_QUERIES: True` en production** sans mécanisme d'authentification préalable. L'introspection expose l'intégralité de votre schéma.

> ⚠️ **Les documents persistés nécessitent une gestion du cycle de vie** : lors d'un déploiement, les anciens documents doivent rester accessibles pendant la période de transition.

---

### Exercice d'application

1. Configurez votre projet en mode production (no introspection, max complexity)
2. Implémentez le pattern "Error as Data" sur un champ `external_status` de `TaskType`
3. Ajoutez une règle de validation custom qui limite la profondeur à 7 niveaux

---

### Ressources complémentaires

- [Persisted Documents — Undine](https://mrthearman.github.io/undine/persisted-documents/)
- [Validation Rules — Undine](https://mrthearman.github.io/undine/validation-rules/)
- [Scalars — Undine](https://mrthearman.github.io/undine/scalars/)

---

## Module 10 — Intégrations et outils

### Objectifs du module

- Intégrer `django-channels` pour WebSockets et SSE
- Utiliser GraphiQL pour explorer et déboguer
- Écrire des tests avec le client de test intégré d'Undine
- Utiliser les outils de debugging

### Durée estimée : 1h30

### Concepts clés

- `GraphQLProtocolTypeRouter` (channels)
- GraphiQL, `GRAPHIQL_ENABLED`
- Client de test Undine (`pytest` integration)
- `django-debug-toolbar`

---

### 10.1 Intégration channels (WebSockets)

```python
# config/asgi.py
import os
from django.core.asgi import get_asgi_application
from undine.integrations.channels import GraphQLProtocolTypeRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()

application = GraphQLProtocolTypeRouter(
    http=django_asgi_app,
)
```

Le `GraphQLProtocolTypeRouter` route automatiquement :
- Les requêtes HTTP vers l'application Django
- Les connexions WebSocket GraphQL vers les handlers Undine
- Les connexions SSE vers les handlers Undine

---

### 10.2 GraphiQL

```python
UNDINE = {
    "GRAPHIQL_ENABLED": True,
    "ALLOW_INTROSPECTION_QUERIES": True,

    # Subscriptions via SSE dans GraphiQL (au lieu de WebSocket)
    "GRAPHIQL_SSE_ENABLED": False,
}
```

Accédez à `http://localhost:8000/graphql/` pour ouvrir GraphiQL.

**Fonctionnalités GraphiQL :**
- Autocomplétion basée sur le schéma
- Documentation intégrée
- Historique des requêtes
- Support des variables et des headers
- Visualisation des subscriptions (WebSocket ou SSE)

---

### 10.3 Tests avec le client intégré

Undine fournit un client de test basé sur `pytest` :

```python
# tests/test_schema.py
import pytest
from undine.testing import GraphQLTestClient

from myapp.schema import schema


@pytest.fixture
def client():
    return GraphQLTestClient(schema)


def test_query_tasks(client, django_user_factory):
    user = django_user_factory(is_staff=True)

    result = client.execute(
        """
        query {
          tasks {
            pk
            name
            done
          }
        }
        """,
        user=user,
    )

    assert result.errors is None
    assert len(result.data["tasks"]) >= 0


def test_create_task_permission_denied(client):
    result = client.execute(
        """
        mutation {
          createTask(input: { name: "Test" }) {
            pk
          }
        }
        """
    )

    assert result.errors is not None
    assert result.errors[0]["extensions"]["error_code"] == "PERMISSION_DENIED"


def test_create_task_success(client, django_user_factory):
    user = django_user_factory(is_staff=True)

    result = client.execute(
        """
        mutation {
          createTask(input: { name: "Nouvelle tâche" }) {
            pk
            name
            done
          }
        }
        """,
        user=user,
    )

    assert result.errors is None
    assert result.data["createTask"]["name"] == "Nouvelle tâche"
    assert result.data["createTask"]["done"] is False
```

---

### 10.4 Debug avec django-debug-toolbar

```bash
pip install django-debug-toolbar
```

```python
# settings.py
INSTALLED_APPS = [
    "debug_toolbar",
    # ...
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # ...
]

INTERNAL_IPS = ["127.0.0.1"]

# urls.py
import debug_toolbar
urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
    # ...
]
```

La toolbar affiche les requêtes SQL générées, ce qui permet de vérifier l'efficacité de l'optimiseur.

---

### Ressources complémentaires

- [Integrations — Undine](https://mrthearman.github.io/undine/integrations/)
- [Django Channels](https://channels.readthedocs.io/)

---

## Module 11 — Configuration avancée et personnalisation

### Objectifs du module

- Maîtriser le dictionnaire `UNDINE` dans son ensemble
- Comprendre et utiliser les `LifecycleHook`
- Personnaliser les scalars, directives et l'optimiseur

### Durée estimée : 2h

### Concepts clés

- `UNDINE` settings dict complet
- `LifecycleHook`, `RequestCacheHook`
- Scalars custom, Directives
- `EXECUTION_CONTEXT_CLASS`, `DOCSTRING_PARSER`

---

### 11.1 Référence des settings essentiels

```python
UNDINE = {
    # --- Schema ---
    "SCHEMA": "myapp.schema.schema",         # Chemin vers votre schéma
    "AUTOGENERATION": False,                  # Auto-génération globale
    "CAMEL_CASE_SCHEMA_FIELDS": True,        # snake_case → camelCase

    # --- Sécurité ---
    "ALLOW_INTROSPECTION_QUERIES": False,     # Introspection (dev only)
    "ALLOW_DID_YOU_MEAN_SUGGESTIONS": False, # Suggestions dans les erreurs
    "MAX_QUERY_COMPLEXITY": 100,              # Complexité max
    "PERSISTED_DOCUMENTS_ONLY": False,        # Mode allow-list strict

    # --- GraphiQL ---
    "GRAPHIQL_ENABLED": False,               # Activer GraphiQL
    "GRAPHIQL_SSE_ENABLED": False,           # SSE pour subscriptions dans GraphiQL

    # --- Performance ---
    "DISABLE_ONLY_FIELDS_OPTIMIZATION": False, # Désactiver QuerySet.only()
    "LIST_ENTRYPOINT_LIMIT": 100,              # Limite défaut des listes
    "MUTATION_INSTANCE_LIMIT": 100,            # Limite bulk mutations
    "ENTRYPOINT_DEFAULT_CACHE_TIME": 0,        # Cache défaut (0 = désactivé)

    # --- Async & Subscriptions ---
    "ASYNC": False,                             # Mode async
    "USE_SSE_DISTINCT_CONNECTIONS_FOR_HTTP_1": False,

    # --- Fichiers ---
    "FILE_UPLOAD_ENABLED": False,

    # --- Personnalisation ---
    "EXECUTION_CONTEXT_CLASS": "undine.execution.UndineExecutionContext",
    "DOCSTRING_PARSER": "undine.parsers.parse_docstring.RSTDocstringParser",
    "LIFECYCLE_HOOKS": ["undine.hooks.RequestCacheHook"],
    "ADDITIONAL_VALIDATION_RULES": [],

    # --- URL ---
    "GRAPHQL_PATH": "graphql/",
    "GRAPHQL_VIEW_NAME": "graphql",
}
```

---

### 11.2 Lifecycle Hooks

Les hooks de cycle de vie permettent d'intervenir à différentes étapes du traitement d'une requête GraphQL.

```python
from undine.hooks import LifecycleHook, LifecycleHookContext


class LoggingHook(LifecycleHook):
    """Log chaque requête GraphQL."""

    def before_execution(self, context: LifecycleHookContext) -> None:
        print(f"→ GraphQL request: {context.document}")

    def after_execution(self, context: LifecycleHookContext) -> None:
        errors = context.result.errors
        if errors:
            print(f"✗ Errors: {errors}")
        else:
            print(f"✓ Success")


class AuthenticationHook(LifecycleHook):
    """Vérifie l'authentification avant chaque requête."""

    def before_execution(self, context: LifecycleHookContext) -> None:
        if not context.request.user.is_authenticated:
            # Lever une exception pour bloquer la requête
            from undine.exceptions import GraphQLPermissionError
            raise GraphQLPermissionError("Authentification requise.")
```

```python
# settings.py
UNDINE = {
    "LIFECYCLE_HOOKS": [
        "undine.hooks.RequestCacheHook",    # Cache intégré (à garder)
        "myapp.hooks.LoggingHook",
        "myapp.hooks.AuthenticationHook",
    ],
}
```

---

### 11.3 Scalars custom

```python
from undine.scalars import GraphQLScalar


class GraphQLColor(GraphQLScalar):
    """Scalar pour les couleurs hexadécimales (#RRGGBB)."""

    @staticmethod
    def serialize(output_value):
        if not str(output_value).startswith("#"):
            raise ValueError(f"Invalid color: {output_value}")
        return str(output_value)

    @staticmethod
    def parse_value(input_value):
        if not str(input_value).startswith("#"):
            raise ValueError(f"Invalid color: {input_value}")
        return str(input_value)

    @staticmethod
    def parse_literal(value_node, variable_values=None):
        return value_node.value
```

```python
# Utilisation dans un Field
class ProjectType(QueryType[Project]):
    color = Field()  # Si le champ modèle retourne une couleur hex
```

Pour les scalars intégrés : `GraphQLDateTime`, `GraphQLDate`, `GraphQLTime`, `GraphQLJSON`, `GraphQLUUID`, `File`, `Image`.

---

### 11.4 Directives custom

```python
from graphql import DirectiveLocation
from undine.directives import Directive, DirectiveArgument


class RateLimitDirective(Directive, locations=[DirectiveLocation.FIELD_DEFINITION]):
    """Directive pour limiter le taux d'appels sur un champ."""
    max_calls = DirectiveArgument(int)
    window_seconds = DirectiveArgument(int, default_value=60)


# Utilisation
class Query(RootType):
    tasks = Entrypoint(TaskType, many=True) @ RateLimitDirective(max_calls=10)
```

---

### 11.5 Cache contextuel avancé

```python
# settings.py — Ajouter la langue acceptée dans la clé de cache
from typing import Any
from undine.hooks import LifecycleHookContext


def extra_cache_context(context: LifecycleHookContext) -> dict[str, Any]:
    return {
        "lang": context.request.headers.get("Accept-Language", "fr"),
    }


UNDINE = {
    "REQUEST_CACHE_EXTRA_CONTEXT": "myapp.cache.extra_cache_context",
    "REQUEST_CACHE_ALIAS": "graphql",  # Alias du cache Django à utiliser
}

# Cache Redis dédié
CACHES = {
    "graphql": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
```

---

### Ressources complémentaires

- [Settings — Undine](https://mrthearman.github.io/undine/settings/)
- [Lifecycle Hooks — Undine](https://mrthearman.github.io/undine/lifecycle-hooks/)
- [Scalars — Undine](https://mrthearman.github.io/undine/scalars/)
- [Directives — Undine](https://mrthearman.github.io/undine/directives/)
- [Hacking Undine](https://mrthearman.github.io/undine/hacking-undine/)

---

## Module 12 — Projet final : API de gestion de projets

### Objectifs du module

- Mettre en pratique l'ensemble des concepts de la formation
- Construire une API GraphQL complète avec tous les patterns Undine
- Valider la compréhension par un projet concret et documenté

### Durée estimée : 4h

---

### 12.1 Énoncé

Construisez une API GraphQL complète pour une application de **gestion de projets collaboratifs**. L'API doit couvrir :

**Modèles :**
- `User` (Django natif) — avec profil (avatar, bio)
- `Project` — nom, description, owner, membres (M2M), statut (active/archived), created_at
- `Task` — nom, description, done, priorité (low/medium/high), assignee, project, created_at
- `Step` — nom, done, task
- `Comment` — contenu, author, task, created_at
- `Attachment` — fichier uploadé, task, uploaded_by

**Fonctionnalités attendues :**

1. **Queries** : accès à tous les modèles avec filtres, tri, pagination
2. **Mutations** : CRUD complet sur Project, Task, Step, Comment ; upload de fichier pour Attachment
3. **Subscriptions** : notification en temps réel à la création de Task et de Comment
4. **Permissions** : lecture publique des projets actifs, écriture pour les membres, admin pour les owners
5. **Optimiseur** : toutes les relations doivent être optimisées
6. **Sécurité** : permissions au niveau mutation, pas d'introspection en "production"

---

### 12.2 Corrigé détaillé

#### Structure de fichiers

```
myproject/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
├── api/
│   ├── models.py
│   ├── schema.py
│   ├── filters.py
│   ├── orders.py
│   ├── mutations.py
│   └── subscriptions.py
└── manage.py
```

#### `api/models.py`

```python
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects")
    members = models.ManyToManyField(User, related_name="projects", blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks"
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)


class Step(models.Model):
    name = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="steps")


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)


class Attachment(models.Model):
    file = models.FileField(upload_to="attachments/")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="attachments")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### `api/filters.py`

```python
from undine import Filter, FilterSet
from .models import Project, Task


class ProjectFilterSet(FilterSet[Project]):
    name = Filter(lookup="icontains")
    status = Filter()
    owner_id = Filter(field_name="owner")


class TaskFilterSet(FilterSet[Task]):
    name = Filter(lookup="icontains")
    done = Filter()
    priority = Filter()
    project_id = Filter(field_name="project")
    assignee_id = Filter(field_name="assignee")
```

#### `api/orders.py`

```python
from undine import Order, OrderSet
from .models import Project, Task


class ProjectOrderSet(OrderSet[Project]):
    pk = Order()
    name = Order()
    created_at = Order()


class TaskOrderSet(OrderSet[Task]):
    pk = Order()
    name = Order()
    priority = Order()
    created_at = Order()
```

#### `api/schema.py`

```python
from typing import Any

from undine import (
    Entrypoint, Field, Filter, FilterSet, GQLInfo,
    Input, MutationType, Order, OrderSet, QueryType, RootType, create_schema,
)
from undine.exceptions import GraphQLPermissionError, GraphQLValidationError
from undine.relay import Connection, Node
from undine.subscriptions import ModelCreateSubscription

from .filters import ProjectFilterSet, TaskFilterSet
from .models import Attachment, Comment, Project, Step, Task
from .orders import ProjectOrderSet, TaskOrderSet


# ─── QueryTypes ────────────────────────────────────────────────────────────────

class UserType(QueryType[__import__('django').contrib.auth.get_user_model()()]):
    pk = Field()
    username = Field()
    email = Field()

    @classmethod
    def __permissions__(cls, instance, info: GQLInfo) -> None:
        if not info.context.user.is_authenticated:
            raise GraphQLPermissionError("Authentification requise.")


@Node
@ProjectFilterSet
@ProjectOrderSet
class ProjectType(QueryType[Project], schema_name="Project"):
    pk = Field()
    name = Field()
    description = Field()
    status = Field()
    created_at = Field()
    owner = Field()
    members = Field()
    tasks = Field()

    @classmethod
    def __filter_queryset__(cls, queryset, info: GQLInfo):
        # Les projets archivés ne sont visibles que par leur owner
        user = info.context.user
        if not user.is_authenticated:
            return queryset.filter(status="active")
        return queryset.filter(status="active") | queryset.filter(owner=user)


@Node
@TaskFilterSet
@TaskOrderSet
class TaskType(QueryType[Task], schema_name="Task"):
    pk = Field()
    name = Field()
    description = Field()
    done = Field()
    priority = Field()
    created_at = Field()
    project = Field()
    assignee = Field()
    steps = Field()
    comments = Field()
    attachments = Field()

    @classmethod
    def __permissions__(cls, instance: Task, info: GQLInfo) -> None:
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLPermissionError("Authentification requise.")

        # Vérifier que l'utilisateur est membre du projet
        if not instance.project.members.filter(pk=user.pk).exists():
            if instance.project.owner_id != user.pk:
                raise GraphQLPermissionError("Accès refusé à cette tâche.")


class StepType(QueryType[Step], schema_name="Step"):
    pk = Field()
    name = Field()
    done = Field()
    task = Field()


class CommentType(QueryType[Comment], schema_name="Comment"):
    pk = Field()
    content = Field()
    created_at = Field()
    author = Field()
    task = Field()


class AttachmentType(QueryType[Attachment], schema_name="Attachment"):
    pk = Field()
    file = Field()
    created_at = Field()
    uploaded_by = Field()


# ─── MutationTypes ─────────────────────────────────────────────────────────────

class ProjectCreateMutation(MutationType[Project]):
    name = Input()
    description = Input(default_value="")

    @classmethod
    def __permissions__(cls, instance, info: GQLInfo, input_data) -> None:
        if not info.context.user.is_authenticated:
            raise GraphQLPermissionError("Authentification requise.")

    @classmethod
    def __mutate__(cls, instance: Project, info: GQLInfo, input_data: dict[str, Any]) -> Project:
        instance.owner = info.context.user
        instance.__dict__.update(input_data)
        instance.save()
        # Ajouter le créateur comme membre
        instance.members.add(info.context.user)
        return instance


class ProjectUpdateMutation(MutationType[Project]):
    pk = Input()
    name = Input()
    description = Input()
    status = Input()

    @classmethod
    def __permissions__(cls, instance: Project, info: GQLInfo, input_data) -> None:
        if instance.owner_id != info.context.user.pk:
            raise GraphQLPermissionError("Seul le propriétaire peut modifier ce projet.")


class TaskCreateInput(MutationType[Project], kind="related"):
    pk = Input()
    name = Input()


class TaskCreateMutation(MutationType[Task]):
    name = Input()
    description = Input(default_value="")
    priority = Input(default_value="medium")
    project = Input(TaskCreateInput)

    @classmethod
    def __permissions__(cls, instance, info: GQLInfo, input_data) -> None:
        if not info.context.user.is_authenticated:
            raise GraphQLPermissionError("Authentification requise.")

    @classmethod
    def __validate__(cls, instance, info: GQLInfo, input_data: dict[str, Any]) -> None:
        if len(input_data.get("name", "")) < 3:
            raise GraphQLValidationError("Le nom doit contenir au moins 3 caractères.")


class TaskUpdateMutation(MutationType[Task]):
    pk = Input()
    name = Input()
    done = Input()
    priority = Input()

    @classmethod
    def __permissions__(cls, instance: Task, info: GQLInfo, input_data) -> None:
        user = info.context.user
        is_owner = instance.project.owner_id == user.pk
        is_assignee = instance.assignee_id == user.pk
        if not (is_owner or is_assignee):
            raise GraphQLPermissionError("Seuls le propriétaire du projet ou l'assigné peuvent modifier cette tâche.")


class TaskDeleteMutation(MutationType[Task]):
    pk = Input()

    @classmethod
    def __permissions__(cls, instance: Task, info: GQLInfo, input_data) -> None:
        if instance.project.owner_id != info.context.user.pk:
            raise GraphQLPermissionError("Seul le propriétaire du projet peut supprimer des tâches.")


class CommentCreateMutation(MutationType[Comment]):
    content = Input()
    task_id = Input(field_name="task")

    @classmethod
    def __permissions__(cls, instance, info: GQLInfo, input_data) -> None:
        if not info.context.user.is_authenticated:
            raise GraphQLPermissionError("Authentification requise.")

    @classmethod
    def __mutate__(cls, instance: Comment, info: GQLInfo, input_data: dict[str, Any]) -> Comment:
        instance.author = info.context.user
        instance.__dict__.update(input_data)
        instance.save()
        return instance


# ─── RootTypes ─────────────────────────────────────────────────────────────────

class Query(RootType):
    """Opérations de lecture."""

    project = Entrypoint(ProjectType, nullable=True)
    projects = Entrypoint(Connection(ProjectType))

    task = Entrypoint(TaskType, nullable=True)
    tasks = Entrypoint(Connection(TaskType))


class Mutation(RootType):
    """Opérations d'écriture."""

    create_project = Entrypoint(ProjectCreateMutation)
    update_project = Entrypoint(ProjectUpdateMutation)

    create_task = Entrypoint(TaskCreateMutation)
    update_task = Entrypoint(TaskUpdateMutation)
    delete_task = Entrypoint(TaskDeleteMutation)
    bulk_create_tasks = Entrypoint(TaskCreateMutation, many=True)

    create_comment = Entrypoint(CommentCreateMutation)


class Subscription(RootType):
    """Opérations temps réel."""

    task_created = Entrypoint(ModelCreateSubscription(TaskType))
    comment_created = Entrypoint(ModelCreateSubscription(CommentType))


schema = create_schema(query=Query, mutation=Mutation, subscription=Subscription)
```

#### `config/settings.py` (extrait)

```python
UNDINE = {
    "SCHEMA": "api.schema.schema",
    "GRAPHIQL_ENABLED": True,              # Désactiver en prod
    "ALLOW_INTROSPECTION_QUERIES": True,   # Désactiver en prod
    "CAMEL_CASE_SCHEMA_FIELDS": True,
    "ASYNC": True,
    "FILE_UPLOAD_ENABLED": True,
    "MAX_QUERY_COMPLEXITY": 100,
    "LIST_ENTRYPOINT_LIMIT": 50,
    "LIFECYCLE_HOOKS": [
        "undine.hooks.RequestCacheHook",
    ],
}
```

---

### 12.3 Exemples de requêtes de test

**Créer un projet :**

```graphql
mutation {
  createProject(input: { name: "Mon projet", description: "Description" }) {
    pk
    name
    owner { username }
  }
}
```

**Lister les tâches d'un projet avec filtres et pagination :**

```graphql
query {
  tasks(
    filter: { projectId: 1, done: false }
    orderBy: [priorityDesc]
    first: 10
  ) {
    pageInfo { hasNextPage }
    edges {
      node {
        pk
        name
        priority
        assignee { username }
        steps { name done }
      }
    }
  }
}
```

**S'abonner aux nouvelles tâches :**

```graphql
subscription {
  taskCreated {
    pk
    name
    project { name }
  }
}
```

---

### 12.4 Points de vérification

Avant de valider votre projet, assurez-vous que :

- [ ] Toutes les relations sont accessibles via le schéma GraphQL
- [ ] Les filtres et tris fonctionnent sur les listes paginées
- [ ] Les permissions bloquent les accès non autorisés
- [ ] La validation retourne des erreurs compréhensibles
- [ ] L'optimiseur génère au maximum 3-4 requêtes SQL pour une requête GraphQL imbriquée
- [ ] Les subscriptions notifient en temps réel
- [ ] Les tests couvrent les cas nominaux et d'erreur

---

## Récapitulatif des concepts Undine

| Concept | Classe | Utilisation |
|---|---|---|
| Type de sortie pour modèle | `QueryType[Model]` | Exposer un modèle en lecture |
| Champ de sortie | `Field` | Champ sur un `QueryType` |
| Type de mutation | `MutationType[Model]` | Créer/modifier/supprimer |
| Champ d'entrée | `Input` | Argument d'une mutation |
| Filtre | `FilterSet[Model]`, `Filter` | Filtrer les listes |
| Tri | `OrderSet[Model]`, `Order` | Trier les listes |
| Point d'entrée | `Entrypoint` | "Endpoint dans le schéma" |
| Type racine | `RootType` | Query / Mutation / Subscription |
| Info de contexte | `GQLInfo` | Accès au user, request |
| Pagination curseur | `Connection`, `Node` | Relay pagination |
| Temps réel | `ModelCreateSubscription` | Subscriptions sur signaux |
| Optimiseur | `OptimizationData` | Personnaliser les QuerySets |
| DataLoader | `DataLoader` | Batching appels externes |
| Hooks | `LifecycleHook` | Intercepter le cycle de vie |

---

## Références complètes

| Section | URL |
|---|---|
| Documentation officielle | https://mrthearman.github.io/undine/ |
| Getting Started | https://mrthearman.github.io/undine/getting-started/ |
| Tutorial | https://mrthearman.github.io/undine/tutorial/ |
| Schema | https://mrthearman.github.io/undine/schema/ |
| Queries | https://mrthearman.github.io/undine/queries/ |
| Mutations | https://mrthearman.github.io/undine/mutations/ |
| Filtering | https://mrthearman.github.io/undine/filtering/ |
| Ordering | https://mrthearman.github.io/undine/ordering/ |
| Pagination | https://mrthearman.github.io/undine/pagination/ |
| Subscriptions | https://mrthearman.github.io/undine/subscriptions/ |
| Optimizer | https://mrthearman.github.io/undine/optimizer/ |
| DataLoaders | https://mrthearman.github.io/undine/dataloaders/ |
| Lifecycle Hooks | https://mrthearman.github.io/undine/lifecycle-hooks/ |
| Persisted Documents | https://mrthearman.github.io/undine/persisted-documents/ |
| Settings | https://mrthearman.github.io/undine/settings/ |
| File Upload | https://mrthearman.github.io/undine/file-upload/ |
| Async Support | https://mrthearman.github.io/undine/async/ |
| Integrations | https://mrthearman.github.io/undine/integrations/ |
| Global Object IDs | https://mrthearman.github.io/undine/global-object-ids/ |
| Scalars | https://mrthearman.github.io/undine/scalars/ |
| Directives | https://mrthearman.github.io/undine/directives/ |
| Hacking Undine | https://mrthearman.github.io/undine/hacking-undine/ |
| FAQ | https://mrthearman.github.io/undine/faq/ |

---

*Formation rédigée d'après la documentation officielle d'Undine — https://mrthearman.github.io/undine/*
