from api.models import Product,Category
import undine

class CategoryType(undine.QueryType[Category], auto=True):
    pk = undine.Field(schema_name="id")
    name = undine.Field()
    description = undine.Field()



class ProductFilterSet(undine.FilterSet[Product], auto=True):
    category = undine.Filter(field_name="category__name", lookup_expr="icontains")

class ProductOrderSet(undine.OrderSet[Product], auto=True):
    pass
@undine.relay.Node
class ProductType(undine.QueryType[Product], orderset=ProductOrderSet, filterset=ProductFilterSet, auto=True):
    pk = undine.Field(schema_name="id")

