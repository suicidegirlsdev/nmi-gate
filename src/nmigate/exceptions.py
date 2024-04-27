from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import HTTPError as RequestsHTTPError
from requests.exceptions import RequestException

""" Custom exceptions for the NMI gateway, based on requests exceptions. """


class APIException(RequestException):
    pass


class ConnectionError(APIException, RequestsConnectionError):
    """
    Connection issues with the API.
    """


class HTTPError(APIException, RequestsHTTPError):
    """
    HTTP error status code returned by the API.

    All responses should return 200 except some rate limit
    issues, so this shouldn't generally occur.
    """


class ResponseError(APIException):
    """
    Error found in the response data.
    """

    def __init__(self, *args, parsed_response=None, **kwargs):
        # Requests exceptions support passing in the response.
        # This adds support for passing the parsed response.
        self.parsed_response = parsed_response
        super().__init__(*args, **kwargs)


class TransactionDeclinedError(ResponseError):
    """
    Transaction was declined. Used if retrying is
    indeterminate.
    """


class TransactionDeclinedDuplicateError(TransactionDeclinedError):
    """
    Transaction was declined due to being a duplicate transaction.
    """


class TransactionDeclinedNotRetryableError(TransactionDeclinedError):
    """
    Transaction was declined and should not be retried due
    to the nature of the decline type.
    """


class TransactionDeclinedRetryableError(TransactionDeclinedError):
    """
    Transaction was declined and should be retried,
    specifically suggested by the code.
    """


class TransactionProcessingError(APIException):
    """
    Transaction failed due to a processor or gateway error.
    """


class RateLimitError(TransactionProcessingError):
    """
    Base for any rate limit being exceeded.
    These can be trigger from the HTTP status or from the
    parsed response data.
    """


class SystemWideRateLimitError(RateLimitError, HTTPError):
    """Raised when the rate limit across all APIs exceeded"""


class APIRateLimitError(RateLimitError, ResponseError):
    """Raised when the rate limit for a single API is exceeded"""
