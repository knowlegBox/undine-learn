import decimal
from typing import Any

import graphql
import undine
from undine import GQLInfo
from undine.typing import TModel

from api import models
from .types import OrderType
from undine.utils.graphql.type_registry import get_or_create_graphql_object_type

def calculation_total_price(order_items:dict[str,Any], order:models.Order = None)->decimal.Decimal:
    amount = 0
    for order_item in order_items:
        product = models.Product.objects.get(pk=order_item["product"].pk)
        total_price = order_item["quantity"] * order_item["price"]
        models.OrderItem.objects.create(
            order=order,
            product=product,
            quantity=order_item["quantity"],
            price=order_item["price"],
            total_price=total_price
        )
        amount += total_price
    return amount


class  OrderItemInput(undine.MutationType[models.OrderItem], kind="related"):
    pk = undine.Input(schema_name="id", hidden=True)
    product = undine.Input()
    quantity = undine.Input()
    price = undine.Input()


class OrderCreate(undine.MutationType[models.Order]):
    pk = undine.Input(schema_name="id", hidden=True)
    user = undine.Input(str,required=True,)
    date = undine.Input()
    items = undine.Input(OrderItemInput, required=True, many=True)

    @classmethod
    def __mutate__(cls, instance: models.Order, info: GQLInfo, input_data: dict[str, Any]) -> Any:
        try:
            # Récupérer les items (doit être une liste car many=True ajouté)
            order_items = input_data.pop("items", None)
            # print("order_items: ",order_items)
            
            # Récupérer l'utilisateur (on s'assure d'avoir l'instance)
            user_id = input_data.pop("user", None)
            user_instance = None
            if user_id:
                user_instance = models.User.objects.get(pk=user_id)
            
            # Créer la commande
            # print("input_data: ",input_data)
            order = models.Order.objects.create(user=user_instance, **input_data)
            # print(input_data)
            if not order_items:
                raise ValueError("Une commande doit contenir au moins un article.")
            
            # Calculer le prix total et créer les OrderItems
            total_price = calculation_total_price(order_items, order)
            order.total_price = total_price
            order.save()

            return {
                "success": True,
                "message": "Commande créée avec succès",
                "instance": order
            }

        except (models.User.DoesNotExist):
            return {
                "success": False,
                "message": "Utilisateur non trouvé",
                "instance": None
            }
        except  models.Product.DoesNotExist:
            return {
                "success": False,
                "message": " Produit non trouvé",
                "instance": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la création de la commande : {str(e)}",
                "instance": None
            }
    @classmethod
    def __output_type__(cls):
        order_gpl_type = OrderType.__output_type__()
        fields ={
            "success": graphql.GraphQLField(graphql.GraphQLNonNull(graphql.GraphQLBoolean)),
            "message": graphql.GraphQLField(graphql.GraphQLNonNull(graphql.GraphQLString)),
            "instance": graphql.GraphQLField(order_gpl_type),
        }

        return get_or_create_graphql_object_type(
            name="OrderPayload",
            fields=fields
        )



class OrderUpdate(undine.MutationType[models.Order]):
    pk = undine.Input(str,schema_name="id",required=True)
    is_active = undine.Input()
    is_deleted = undine.Input()

    @classmethod
    def __mutate__(cls, instance: TModel, info: GQLInfo, input_data: dict[str, Any]) -> Any:
        try:
            # print("input_data: ",input_data)
            order = models.Order.objects.get(pk=input_data["pk"])
            items = models.OrderItem.objects.filter(order=order)
            for item in items:
                # print("item: ",item)
                item.is_deleted = True
                item.is_active = False
                item.save()
            return {
                "success": True,
                "message": f"Commande mise à jour avec succès {order.id}",
                "instance": order
            }

        except models.OrderItem.DoesNotExist:
            return{
                "success": False,
                "message": f"Aucun article trouvé pour la commande {order.id}"
            }
        except models.Order.DoesNotExist:
            return{
                "success": False,
                "message": f"Commande non trouvée avec l'ID {input_data['pk']}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la mise à jour {e}",
                "instance": None
            }

    @classmethod
    def __output_type__(cls):
        order_gpl_type = OrderType.__output_type__()
        fields ={
            "success": graphql.GraphQLField(graphql.GraphQLNonNull(graphql.GraphQLBoolean)),
            "message": graphql.GraphQLField(graphql.GraphQLNonNull(graphql.GraphQLString)),
            "instance": graphql.GraphQLField(order_gpl_type),
        }
        return graphql.GraphQLObjectType(
            name="UpdateOrderResponse",
            fields=fields
        )