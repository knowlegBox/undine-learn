from api import models
from api.models import Product
from typing import Any

import undine


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
    def __mutate__(cls, instance: Product, info: undine.GQLInfo, input_data: dict[str, Any]) -> dict[str, Any]:
        print("input_data:",input_data)
        category = input_data.pop("category") if "category" in input_data else None
        if category:
            instance.category,created = models.Category.objects.get_or_create(name=category["name"], description=category["description"])

        instance.category =instance.category
        instance.save()
        print("instance:",instance)
        return instance


class UpdateProduct(undine.MutationType[Product]):
    pass

