
from api import models
import undine
from django.db.models import Value, Sum, OuterRef, DecimalField
from django.db.models.functions import Coalesce



class UserCartTotal(undine.Calculation[float]):
    """Calcule le total de toutes les commandes pour l'utilisateur lié à cette commande."""
    def __call__(self, info:undine.GQLInfo)->undine.DjangoExpression:
        return Coalesce(
            models.Order.objects.filter(
                user=OuterRef("user"),
                is_active=True,
                is_deleted=False,
            ).values("user").annotate( total=Sum("total_price")).values("total"),Value(0.0),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
#========================================================================
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
    cart_total = undine.Field(UserCartTotal)
