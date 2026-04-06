
from api import models
import undine
from django.db.models import Value, Sum, OuterRef,DecimalField
from django.db.models.functions import Coalesce

class UserCartTotalPrice(undine.Calculation[float]):

    def __call__(self, info: undine.GQLInfo) -> undine.DjangoExpression:
        return Coalesce(
            models.Order.objects.filter(
                user=OuterRef("pk"),
                is_active=True,
                is_deleted=False,
            ).values("user").annotate(total=Sum("total_price")).values("total"), Value(0.0),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )


class UserFilter(undine.FilterSet[models.User], auto=True):
    pass

class UserOrder(undine.OrderSet[models.User], auto=True):
    pass
#@undine.relay.Node
class UserType(undine.QueryType[models.User],filterset=UserFilter, orderset=UserOrder, auto=True):
    cart_total = undine.Field(UserCartTotalPrice)
    pk = undine.Field(schema_name="id")