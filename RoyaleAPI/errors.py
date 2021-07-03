__all__ = [
    'RequestError', 'StatusError', 'NotResponding', 'NetworkError',
    'BadRequest', 'NotFoundError', 'ServerError', 'Unauthorized',
    'NotTrackedError', 'RatelimitError', 'UnexpectedError',
    'RatelimitErrorDetected'
]


class RequestError(Exception):
    """Base class for all errors"""
    pass


class StatusError(RequestError):
    """Base class for all errors except NotResponding and RatelimitDetectedError"""
    def __init__(self, resp, data):
        self.response = resp
        self.code = getattr(resp, 'status', None) or getattr(resp, 'status_code')
        self.method = getattr(resp, 'method', None)
        self.reason = resp.reason
        if isinstance(data, dict):
            self.error = data.get('error')
            if 'message' in data:
                self.error = data.get('message')
        else:
            self.error = data
        self.fmt = '{0.reason} ({0.code}): {0.error}'.format(self)
        super().__init__(self.fmt)


class NotResponding(RequestError):
    """Raised if the API request timed out"""
    def __init__(self):
        self.code = 504
        self.error = 'API request timed out, please be patient.'
        super().__init__(self.error)


class NetworkError(RequestError):
    """Raised if there is an issue with the network
    (i.e. aiohttp.ServerDisconnectedError or requests.ConnectionError)
    """
    def __init__(self):
        self.code = 503
        self.error = 'Network down.'
        super().__init__(self.error)


class BadRequest(StatusError):
    """Raised when status code 400 is returned.
    Typically when at least one search parameter
    was not provided
    """
    pass


class NotFoundError(StatusError):
    """Raised if the player/clan is not found"""
    pass


class ServerError(StatusError):
    """Raised if the api service is having issues"""
    pass


class Unauthorized(StatusError):
    """Raised if you passed an invalid token."""
    pass


class NotTrackedError(StatusError):
    """Raised if the requested clan is not tracked (RoyaleAPI)"""
    pass


class RatelimitError(StatusError):
    """Raised if ratelimit is hit"""
    pass


class UnexpectedError(StatusError):
    """Raised if the error was not caught"""
    pass


class RatelimitErrorDetected(RequestError):
    """Raised when a ratelimit error is detected"""
    def __init__(self, retry_when):
        self.code = 429
        self.retry_when = retry_when
        self.reason = self.error = 'Too many requests detected, retry in ' + str(self.retry_when)
        self.fmt = '{0.reason} ({0.code}): {0.error}'.format(self)
        super().__init__(self.fmt)