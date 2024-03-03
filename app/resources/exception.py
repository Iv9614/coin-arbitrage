__all__ = [
    "BuildChartError",
    "ContainerMissingError",
    "ContainerGetLogError",
    "ApiResponseError",
]


class BaseException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


def __init__(self, message, status_code):
    self.__class__.__bases__[0]().__init__(message, status_code)


def __str__(self):
    return f"{self.__class__.__name__}({self.message})"


# BuildChartError = type(
#     "BuildChartError", (BaseException,), {"init": __init__, "__str__": __str__}
# )
# ContainerMissingError = type(
#     "ContainerMissingError", (BaseException,), {"init": __init__, "__str__": __str__}
# )
# ContainerGetLogError = type(
#     "ContainerGetLogError", (BaseException,), {"init": __init__, "__str__": __str__}
# )

# ApiResponseError = type(
#     "ApiResponseError", (BaseException,), {"init": __init__, "__str__": __str__}
# )
