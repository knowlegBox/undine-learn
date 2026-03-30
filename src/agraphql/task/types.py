
import undine

from api import models


class PostType(undine.QueryType[models.Post]):
    pass



class TaskQueries(undine.QueryType):
    pass