
import undine
from api import models
from . import types as user_types
class UserCreation(undine.MutationType[models.User],kind="create"):
    username = undine.Input(required=True)
    email = undine.Input()
    password = undine.Input()

    @classmethod
    def __mutate__(cls, instance:models.User, info: undine.GQLInfo, input_data: dict[str, Any]) -> dict[str, Any]:
        return  {
            "success": True,
            "message": "User created successfully",
            "instance": "instance"
        }
    
    @classmethod
    def __output_type__(cls) -> undine.GraphQLObjectType:
        product_gql_type = user_types.UserType.__output_type__()
        fields = {
            "success": undine.GraphQLField(undine.GraphQLNonNull(undine.GraphQLBoolean)),
            "message": undine.GraphQLField(undine.GraphQLNonNull(undine.GraphQLString)),
            "instance": undine.GraphQLField(product_gql_type),
        }
        return undine.get_or_create_graphql_object_type(
            name = "UserPayload",
            fields = fields
        )