
from undine import QueryType, OrderSet, FilterSet
from api import models
class UserFilter(FilterSet[models.User]):
    class Meta:
        exclude = ["password","bio","profile_picture"]

class UserOrder(OrderSet[models.User]):
    pass

class UserType(QueryType[models.User],filterset=UserFilter,orderset= UserOrder, auto=True):
    pass