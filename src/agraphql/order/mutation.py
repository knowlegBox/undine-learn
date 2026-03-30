
import undine

from api import models

class CreateOrderItem(undine.MutationType[models.OrderItem], kind="related"):
    pass

class UpdateOrderItem(undine.MutationType[models.OrderItem]):
    pass

class DeleteOrderItem(undine.MutationType[models.OrderItem]):
    pass

class CreateOrder(undine.MutationType[models.Order]):
        items = undine.Input(CreateOrderItem, many=True)


class UpdateOrder(undine.MutationType[models.Order]):
    user = undine.Input()
    total_price = undine.Input()
    is_active = undine.Input()
    is_deleted = undine.Input()

class DeleteOrder(undine.MutationType[models.Order]):
    id = undine.Input(str)

    @classmethod
    def __mutat__(cls,root, info, input_data):
        order = models.Order.objects.get(input_data['id'])
        print(order)
