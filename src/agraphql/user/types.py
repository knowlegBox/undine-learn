
from api import models
import undine

class UserCartTotalPrice(undine.Calculation):

    def __call__(self, *args, **kwargs):
        pass


class UserFilter(undine.FilterSet[models.User], auto=True):
    pass

class UserOrder(undine.OrderSet[models.User], auto=True):
    pass
@undine.relay.Node
class UserType(undine.QueryType[models.User],filterset=UserFilter, orderset=UserOrder, auto=True):
    cart_total = undine.Field(UserCartTotalPrice)
    pk = undine.Field(schema_name="id")