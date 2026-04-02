
from api import models
import undine


class UserFilter(undine.FilterSet[models.User], auto=True):
    pass

class UserOrder(undine.OrderSet[models.User], auto=True):
    pass
@undine.relay.Node
class UserType(undine.QueryType[models.User],filterset=UserFilter, orderset=UserOrder, auto=True):
    pk = undine.Field(schema_name="id")