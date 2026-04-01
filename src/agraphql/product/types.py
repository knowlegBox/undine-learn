from api.models import Product,Category
import undine

class CategoryType(undine.QueryType[Category], auto=True):
    pk = undine.Field(schema_name="id")
    



class ProductFilterSet(undine.FilterSet[Product], auto=True):
    category = undine.Filter(field_name="category__name", lookup_expr="icontains")

class ProductOrderSet(undine.OrderSet[Product], auto=True):
    pass

class ProductType(undine.QueryType[Product], orderset=ProductOrderSet, filterset=ProductFilterSet, auto=True):
    pk = undine.Field(schema_name="id")

