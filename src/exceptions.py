class RequestError(Exception):
    status_code: int
    message: str

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class ServerError(RequestError):

    def __init__(self, message):
        super().__init__(500, message)


class UnauthorizedError(RequestError):

    def __init__(self, message):
        super().__init__(401, message)


class ForbiddenError(RequestError):

    def __init__(self, message):
        super().__init__(403, message)


class ValidationError(RequestError):

    def __init__(self, message):
        super().__init__(400, message)
