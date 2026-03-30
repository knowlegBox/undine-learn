from api.models import Product,Category
import undine

class CategoryType(undine.QueryType[Category]):
    pass


class ProductFilterSet(undine.FilterSet[Product]):
    class Meta:
        fields = ["id", "name", "category__name", "category__id"]

class ProductOrderSet(undine.OrderSet[Product]):
    pass

class ProductType(undine.QueryType[Product]):
    class Meta:

        orderset = ProductOrderSet
        filterset = ProductFilterSet