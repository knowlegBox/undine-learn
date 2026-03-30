
from undine import QueryType, OrderSet, FilterSet
from api import models
class UserFilter(FilterSet[models.User]):
    class Meta:
        exclude = ["password","bio","profile_picture"]

class UserOrder(OrderSet[models.User]):
    class Meta:
        fields = ["username","first_name","last_name","email","created_at", "updated_at"]


class UserType(QueryType[models.User],filterset=UserFilter,orderset= UserOrder, auto=True):
    pass