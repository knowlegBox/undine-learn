import undine

from api.models import Order, OrderItem


class OrderFilterSet(undine.FilterSet[Order]):
    class Meta:
        fields = ["id", "name"]

class OrderOrderSet(undine.OrderSet[Order]):
    pass

class OrderType(undine.QueryType[Order]):
    class Meta:
        orderset = OrderOrderSet
        filterset = OrderFilterSet

class OrderItemFilterSet(undine.FilterSet[OrderItem]):
    class Meta:
        fields = ["id", "name"]

class OrderItemOrderSet(undine.OrderSet[OrderItem]):
    pass

class OrderItemType(undine.QueryType[OrderItem]):
    class Meta:
        orderset = OrderItemOrderSet
        filterset = OrderItemFilterSet