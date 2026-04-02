
import typing
import undine
import graphql

from api import models
from . import types as user_types

from undine.utils.graphql.type_registry import get_or_create_graphql_object_type


class UserCreation(undine.MutationType[models.User],kind="create"):
    username = undine.Input(required=True)
    email = undine.Input()
    password = undine.Input()

    @classmethod
    def __mutate__(cls, instance:models.User, info: undine.GQLInfo, input_data: dict[str, typing.Any]) -> dict[str, typing.Any]:

        user, created = models.User.objects.get_or_create(**input_data)
        if not created:
            return  {
                "success": False,
                "message": f"User with username {input_data['username']} already exists",
                "instance": None
            }
        return  {
            "success": True,
            "message": f"User created successfully {user.username}",
            "instance": user
        }
    
    @classmethod
    def __output_type__(cls) -> graphql.GraphQLObjectType:
        product_gql_type = user_types.UserType.__output_type__()
        fields = {
            "success": graphql.GraphQLField(graphql.GraphQLNonNull(graphql.GraphQLBoolean)),
            "message": graphql.GraphQLField(graphql.GraphQLNonNull(graphql.GraphQLString)),
            "instance": graphql.GraphQLField(product_gql_type),
        }
        return get_or_create_graphql_object_type(
            name = "UserPayload",
            fields = fields
        )

class UserUpdate(undine.MutationType[models.User]):
    pk = undine.Input(str,schema_name="id",required=True)
    username = undine.Input()
    email = undine.Input()
    password = undine.Input()
    is_active = undine.Input()
    is_deleted = undine.Input()

    @classmethod
    def __mutate__(cls,instance:models.User, info:undine.GQLInfo, input_data:dict[str,typing.Any]) -> dict[str,typing.Any]:
      user = models.User.objects.get(id=input_data["pk"])
      for field, value in input_data.items():
          if field != "pk":
              setattr(user, field, value)
      user.save()
      return {
        "success": True,
        "message": f"User updated successfully {user.username}",
        "instance": user
      }

    @classmethod
    def __output_type__(cls):
        user_gql_type = user_types.UserType.__output_type__()
        fields = {
            "success": graphql.GraphQLField(graphql.GraphQLNonNull(graphql.GraphQLBoolean)),
            "message":graphql.GraphQLField(graphql.GraphQLNonNull(graphql.GraphQLString)),
            "instance": graphql.GraphQLField(user_gql_type),
        }
        return get_or_create_graphql_object_type(
            name = "userPayload",
            fields = fields
        )