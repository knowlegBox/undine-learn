from undine import create_schema, RootType, Entrypoint
from undine.relay import Connection


from .product import types as product_types, mutation as product_mutation, product_doc
from .user import types as user_types, mutation as user_mutation


class Queries(RootType):
    users = Entrypoint(Connection(user_types.UserType))# Pagination par curseur
    # user_liste = Entrypoint(UserType, many=True) # Pagination simple (liste)
    # order = Entrypoint(types.OrderType)

    product = Entrypoint(Connection(product_types.ProductType),description= product_doc.get_product_connection)
    product_liste = Entrypoint(product_types.ProductType, many=True,description= product_doc.get_products)

class Mutation(RootType):
    add_user = Entrypoint(user_mutation.UserCreation)
    update_user = Entrypoint(user_mutation.UserUpdate)
    # create_order = Entrypoint(order_mutation.CreateOrder, description="mutation de creation d'un order")
    # update_order = Entrypoint(order_mutation.UpdateOrder, description="mutation de modification d'un order")
    # delete_order = Entrypoint(order_mutation.DeleteOrder, description="mutation de suppression d'un order")

    add_product = Entrypoint(product_mutation.CreateProduct, description=product_doc.add_product)
    update_product = Entrypoint(product_mutation.UpdateProduct, description=product_doc.update_product)

schema = create_schema(query=Queries,  mutation=Mutation)