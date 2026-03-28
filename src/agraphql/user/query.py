
from undine import QueryType
from api import models


class UserQuery(QueryType[models.User], auto=True):
    pass