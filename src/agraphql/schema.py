from undine import create_schema, RootType, Entrypoint
from undine.relay import Connection


from .product import types as product_types, mutation as product_mutation, product_doc
from .user import types as user_types, mutation as user_mutation, user_doc
from .order import types as order_types, mutation as order_mutation


class Queries(RootType):
    users = Entrypoint(Connection(user_types.UserType), description=user_doc.get_users)# Pagination par curseur
    # user_liste = Entrypoint(UserType, many=True) # Pagination simple (liste)
    # order = Entrypoint(types.OrderType)
    orders = Entrypoint(Connection(order_types.OrderType))
    product = Entrypoint(Connection(product_types.ProductType),description= product_doc.get_product_connection)
    product_liste = Entrypoint(product_types.ProductType, many=True,description= product_doc.get_products)

class Mutation(RootType):
    add_user = Entrypoint(user_mutation.UserCreation, description=user_doc.add_user)
    update_user = Entrypoint(user_mutation.UserUpdate, description=user_doc.update_user)
    create_order = Entrypoint(order_mutation.OrderCreate, description="mutation de creation d'un order")
    update_order = Entrypoint(order_mutation.OrderUpdate, description="mutation de modification d'un order")

    add_product = Entrypoint(product_mutation.CreateProduct, description=product_doc.add_product)
    update_product = Entrypoint(product_mutation.UpdateProduct, description=product_doc.update_product)

schema = create_schema(query=Queries,  mutation=Mutation)