from api import models
import undine

class OrderItemFilter(undine.FilterSet[models.OrderItem], auto=True):
    pass
class OrderItemOrdering(undine.OrderSet[models.OrderItem], auto=True):
    pass
class OrderItemType(undine.QueryType[models.OrderItem],filterset=OrderItemFilter, orderset=OrderItemOrdering, auto=True):
    pass

# ===============================================================================

class OrderFilter(undine.FilterSet[models.Order], auto=True):
    pass

class OrderOrdering(undine.OrderSet[models.Order], auto=True):
    pass


class OrderType(undine.QueryType[models.Order],filterset=OrderFilter, orderset=OrderOrdering, auto=True):
    pk = undine.Field(schema_name="id")
