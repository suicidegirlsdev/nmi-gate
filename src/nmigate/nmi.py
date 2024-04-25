from urllib.parse import parse_qsl

import requests
import xmltodict


class Nmi:
    # Can set these on the class at app init to avoid passing on every use.
    security_key = None
    payment_api_url = None
    query_api_url = None

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
        return requests.post(url=url, data=data)

    def _post_payment_api_request(self, data):
        response = self._post_request(self.payment_api_url, data)
        return self._parse_payment_api_response(response)

    def _post_query_api_request(self, data):
        response = self._post_request(self.query_api_url, data)
        return self._parse_query_api_response(response)

    def _parse_payment_api_response(self, response):
        """convert to dict and add a "successful" key based on response code."""
        response_dict = dict(parse_qsl(response.text)) if response.text else {}
        response_dict["successful"] = response_dict["response_code"] == "100"
        return response_dict

    def _parse_query_api_response(self, response):
        # Copied from original wrappers, largely left as is.
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
        return response_dict.get("nm_response", response_dict)


def config_gateway(security_key, payment_api_url, query_api_url):
    Nmi.security_key = security_key
    Nmi.payment_api_url = payment_api_url
    Nmi.query_api_url = query_api_url
