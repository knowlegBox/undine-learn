from api.models import Product,Category
import undine

class CategoryType(undine.QueryType[Category]):
    pass


class ProductFilterSet(undine.FilterSet[Product]):
    class Meta:
        fields = ["pk", "name", "category__name", "category__id"]

class ProductOrderSet(undine.OrderSet[Product]):
    pass

class ProductType(undine.QueryType[Product], orderset=ProductOrderSet, filterset=ProductFilterSet):
    pk = undine.Field(schema_name="id")