from undine import create_schema, RootType, Entrypoint
from undine.relay import Connection

from agraphql.user.mutation import UserMutation
from agraphql.user.type import UserType


class Queries(RootType):
    users = Entrypoint(Connection(UserType))# Pagination par curseur
    user_liste = Entrypoint(UserType, many=True) # Pagination simple (liste)

class Mutation(RootType):
    add_user = Entrypoint(UserMutation)

schema = create_schema(query=Queries,  mutation=Mutation)