from undine import create_schema, RootType, Entrypoint
from undine.relay import Connection

from agraphql.order import types
from agraphql.user.mutation import UserMutation
from agraphql.user.type import UserType

from .order import mutation as order_mutation
from .product import types as product_types, mutation as product_mutation


class Queries(RootType):
    users = Entrypoint(Connection(UserType))# Pagination par curseur
    user_liste = Entrypoint(UserType, many=True) # Pagination simple (liste)
    order = Entrypoint(types.OrderType)
    product = Entrypoint(Connection(product_types.ProductType))

class Mutation(RootType):
    add_user = Entrypoint(UserMutation)
    create_order = Entrypoint(order_mutation.CreateOrder, description="mutation de creation d'un order")
    update_order = Entrypoint(order_mutation.UpdateOrder, description="mutation de modification d'un order")
    delete_order = Entrypoint(order_mutation.DeleteOrder, description="mutation de suppression d'un order")

    add_product = Entrypoint(product_mutation.CreateProduct, description="mutation de creation d'un product")
    update_product = Entrypoint(product_mutation.UpdateProduct, description="mutation de modification d'un product")

schema = create_schema(query=Queries,  mutation=Mutation)