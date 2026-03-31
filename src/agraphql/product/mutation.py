import decimal

from _decimal import Decimal

from api import models
from api.models import Product
from typing import Any

import undine

from graphql import (
    GraphQLBoolean,
    GraphQLField,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLString,
)
from undine.utils.graphql.type_registry import get_or_create_graphql_object_type

class CreateCategory(undine.MutationType[models.Category],auto=False, kind="related"):
    name = undine.Input(str)
    description = undine.Input(str)


class CreateProduct(undine.MutationType[Product], auto=False):

    """
    Mutation pour créer un nouveau produit.
    """

    name = undine.Input(str)
    description = undine.Input(str)
    price = undine.Input(float)
    category = undine.Input(CreateCategory, required=False)

    @classmethod
    def __before_mutate__(cls, instance: Product, info: undine.GQLInfo, input_data: dict[str, Any]) -> dict[str, Any]:
        pass

    @classmethod
    def __mutate__(cls, instance: Product, info: undine.GQLInfo, input_data: dict[str, Any]) -> dict[str, Any]:
        # print("input_data:",input_data)
        category = input_data.pop("category") if "category" in input_data else None
        if category:
            instance.category,created = models.Category.objects.get_or_create(name=category["name"], description=category["description"])
            input_data["category"] = instance.category
        try:
                create_product = models.Product.objects.create(**input_data)
                
                # instance.category =instance.category
                # instance.save()
                # print("create_product: ",create_product)
                return {
                    "success": True,
                    "message": "Product created successfully",
                    "instance": create_product,
                }
                # return create_product


        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "instance": None,
            }

    @classmethod
    def __output_type__(cls)->GraphQLObjectType:
        from agraphql.product.types import ProductType

        # On récupère le GraphQLObjectType généré par ProductType (classe QueryType d'undine)
        product_gql_type = ProductType.__output_type__()

        fields = {
            "success": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
            "message": GraphQLField(GraphQLNonNull(GraphQLString)),
            "instance": GraphQLField(product_gql_type),  # Utilisation du type mapping correct
        }

        return get_or_create_graphql_object_type(
            name="ProductPayload",
            fields=fields,
        )



class UpdateProduct(undine.MutationType[Product], auto=False):
    pk = undine.Input(str,schema_name="id",required=True)
    category = undine.Input(CreateCategory, required=False)
    name = undine.Input(str)
    description = undine.Input(str)
    price = undine.Input(float)
    is_active = undine.Input(bool)
    is_deleted = undine.Input(bool)
    metas = undine.Input(dict, required=False)

    @classmethod
    def __mutate__(cls, instance: Product, info: undine.GQLInfo, input_data: dict[str, Any]) -> dict[str, Any]:
        category = input_data.pop("category") if "category" in input_data else None
        if category:
            category.update(**category)
        try:
            product = models.Product.objects.get(id=input_data["id"])
            product.update(**input_data)
            print("product: ",product)
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "instance": None,
            }
    #
    # @classmethod
    # def __output_type__(cls)->GraphQLObjectType:
    #     from agraphql.product.types import ProductType