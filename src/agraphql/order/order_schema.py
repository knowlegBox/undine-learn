import undine

from . import types

class OrderQueries(undine.RootType):
    order = undine.Entrypoint(types.OrderType)