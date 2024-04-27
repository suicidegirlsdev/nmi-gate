from urllib.parse import parse_qsl

import requests
import xmltodict

from . import exceptions, response_codes
from .utils import card_expiration_as_date


class Nmi:
    # Can set these on the class at app init to avoid passing on every use.
    security_key = None
    payment_api_url = None
    query_api_url = None

    # Will raise on anything that isn't an "approved" response code.
    # Can grab the parsed response from the exception if needed.
    raise_response_errors = True

    def __init__(self, security_key=None, payment_api_url=None, query_api_url=None):
        if security_key:
            self.security_key = security_key
        if payment_api_url:
            self.payment_api_url
        if query_api_url:
            self.query_api_url

        # Ensure minimum required values are set.
        if not self.security_key:
            raise ValueError("NMI gateway requires the security token (key) to be set.")
        if not self.payment_api_url:
            raise ValueError("NMI gateway requires the payment API URL to be set.")
        # This is not used with many of the API calls, but keeping it consistent for simplicity.
        if not self.query_api_url:
            raise ValueError("NMI gateway requires the query API URL to be set.")

    def _post_request(self, url, data):
        response = None
        try:
            response = requests.post(url=url, data=data)
            if response.status_code == 429:
                # Note: there can be other rate limit errors in the
                # response payload, with 200 status. Checked later, after parsing.
                raise exceptions.SystemWideRateLimitError(
                    "Too many requests (system)",
                    response=response,
                )
            # The API should return 200 on transaction errors and failures,
            # and only 429 is documented as non-200 response.
            # So assume any non-200 means there will not be a usable response payload
            # and raise.
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise exceptions.HTTPError(
                f"API returned unexpected status: {e}",
                response=getattr(e, "response", response),
                request=getattr(e, "request", None),
            ) from e
        except requests.exceptions.ConnectionError as e:
            raise exceptions.ConnectionError(
                f"Connection to gateway failed: {e}",
                response=getattr(e, "response", response),
                request=getattr(e, "request", None),
            ) from e
        except requests.exceptions.RequestException as e:
            raise exceptions.APIException(
                f"API request failed: {e}",
                response=getattr(e, "response", response),
                request=getattr(e, "request", None),
            ) from e

        return response

    def _post_payment_api_request(self, data):
        response = self._post_request(self.payment_api_url, data)
        return self._parse_payment_api_response(response)

    def _post_query_api_request(self, data):
        response = self._post_request(self.query_api_url, data)
        return self._parse_query_api_response(response)

    def _parse_payment_api_response(self, response):
        """convert to dict and add a "successful" key based on response code."""
        response_dict = dict(parse_qsl(response.text)) if response.text else {}
        self._normalize_response_dict(response_dict)
        if self.raise_response_errors:
            self._raise_response_errors(response_dict, response)

        return response_dict

    def _parse_query_api_response(self, response):
        # Copied from original wrappers, XML parsing largely left as is.
        xml_string = response.text.replace('<?xml version="1.0" encoding="UTF-8"?>', "")
        # Define custom entities for é, ï, and ü characters
        entity_definitions = (
            "<!DOCTYPE root [\n"
            '<!ENTITY eacute "&#233;">\n'
            '<!ENTITY iuml "&#239;">\n'
            '<!ENTITY uuml "&#252;">\n'
            '<!ENTITY rsquo "&#x2019;">\n'
            "]>\n"
        )
        # Parse XML string into an Element object
        response_dict = xmltodict.parse(entity_definitions + xml_string)
        response_dict = response_dict.get("nm_response", response_dict)
        self._normalize_response_dict(response_dict)
        if self.raise_response_errors:
            self._raise_response_errors(response_dict, response)
        return response_dict

    def _normalize_response_dict(self, response_dict):
        if "response" in response_dict:
            response_dict["response"] == int(response_dict["response"]) or 0

        if "response_code" in response_dict:
            response_dict["response_code"] = int(response_dict["response_code"]) or 0

        if "acu_enabled" in response_dict:
            response_dict["acu_enabled"] = (
                response_dict["acu_enabled"].lower() == "true"
            )

        if "cc_exp" in response_dict:
            response_dict["cc_exp_date"] = (
                card_expiration_as_date(response_dict["cc_exp"])
                if response_dict["cc_exp"]
                else None
            )

        if "cc_number" in response_dict:
            response_dict["cc_last4"] = (
                response_dict["cc_number"][-4:] if response_dict["cc_number"] else ""
            )
        return response_dict

    def _raise_response_errors(self, parsed_response, response):
        response_code = parsed_response.get("response_code")
        if not response_code or response_code == response_codes.TRANSACTION_APPROVED:
            return

        trans_response_code_messages_dict = dict(response_codes.Transaction)
        if response_code == response_codes.TRANSACTION_RATE_LIMITED:
            raise exceptions.APIRateLimitError(
                # Favor our message for this one
                trans_response_code_messages_dict(response_code),
                response=response,
                parsed_response=parsed_response,
            )

        message = parsed_response.get(
            "responsetext"
        ) or trans_response_code_messages_dict(response_code)

        exception_kwargs = {
            "response": response,
            "parsed_response": parsed_response,
        }

        if response_code == response_codes.TRANSACTION_DUPLICATE:
            raise exceptions.TransactionDeclinedDuplicateError(
                message,
                **exception_kwargs,
            )

        if response_code in response_codes.retryable_failure_response_codes:
            raise exceptions.TransactionDeclinedRetryableError(
                message,
                **exception_kwargs,
            )

        if response_code in response_codes.non_retryable_failure_response_codes:
            raise exceptions.TransactionDeclinedNotRetryableError(
                message,
                **exception_kwargs,
            )

        if response_code in response_codes.processing_error_response_codes:
            raise exceptions.TransactionDeclinedProcessingError(
                message,
                **exception_kwargs,
            )

        raise exceptions.TransactionDeclinedError(
            message,
            **exception_kwargs,
        )


def config_gateway(security_key, payment_api_url, query_api_url):
    Nmi.security_key = security_key
    Nmi.payment_api_url = payment_api_url
    Nmi.query_api_url = query_api_url
