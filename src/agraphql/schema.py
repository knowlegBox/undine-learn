from typing import Any

from undine import Entrypoint, QueryType, RootType, create_schema, FilterSet, OrderSet, MutationType, GQLInfo
from undine.exceptions import GraphQLValidationError
from undine.typing import TModel

from api import models


# Déclaration automatique des types GraphQL à partir des modèles
class UserType(QueryType[models.User]):
    pass  # Undine générera les champs du modèle (id, username, ...)

# class PostType(QueryType[models.Post]):
#     pass  # champs : id, author, content, created_at, etc.

class CommentType(QueryType[models.Comment]):
    pass

class LikeType(QueryType[models.Like]):
    pass

class PostFilterSet(FilterSet[models.Post]):
    pass

class PostOrderSet(OrderSet[models.Post]):
    pass

class PostType(QueryType[models.Post], filterset=PostFilterSet, orderset=PostOrderSet):
    pass


class CreatePost(MutationType[models.Post]):
    # Exemple : validation personnalisée (titre non vide)
    @classmethod
    def __validate__(cls, instance: TModel, info: GQLInfo, input_data: dict[str, Any]) -> None:
        if not input_data.get("content"):
            raise GraphQLValidationError("Le contenu ne peut pas être vide.")

class CreateUser(MutationType[models.User]):
    pass

class Mutation(RootType):
    create_post = Entrypoint(CreatePost)
    # bulk_create_posts = Entrypoint(CreatePost, many=True)
    create_user = Entrypoint(CreateUser)

# Définir les points d'entrée de la requête (Root Query)
class Query(RootType):
    user = Entrypoint(UserType)        # requête d'un seul utilisateur
    users = Entrypoint(UserType, many=True)  # requête de liste
    post = Entrypoint(PostType)
    posts = Entrypoint(PostType, many=True)
    comment = Entrypoint(CommentType)
    comments = Entrypoint(CommentType, many=True)
    like = Entrypoint(LikeType)
    likes = Entrypoint(LikeType, many=True)

schema = create_schema(query=Query, mutation=Mutation)  # Génère le schéma GraphQL
