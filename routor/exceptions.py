class RoutorException(Exception):
    pass


class GraphException(RoutorException):
    pass


class NodeDoesNotExist(GraphException):
    pass


class EdgeDoesNotExist(GraphException):
    pass
