from datetime import datetime
from urllib.parse import parse_qs, urlparse

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

    def _parse_query_api_response(self, response):
        # Moved from wrappers (decorators)

        # clean logging data
        if "req" in response and "security_key" in response["req"]:
            response["req"].pop("security_key")

        # pre process nmi_detail
        nmi_response = response.pop("response")
        nmi_response_parsed_url = urlparse(nmi_response.text)
        nmi_response_cleared = parse_qs(nmi_response_parsed_url.path)

        # create new dictionary with all the data
        response["nm_response"] = nmi_response_cleared
        response["date"] = datetime.now()

        # Validate if nmi response is successful
        if nmi_response_cleared["response_code"][0] == "100":
            response["successful"] = True
        else:
            response["successful"] = False

        new_res = {}
        try:
            for key in response["nm_response"]:
                new_res[key] = response["nm_response"][key][0]
        except KeyError:
            pass
        response["nm_response"] = new_res
        return response

    def _parse_payment_api_response(self, response):
        xml_string = response.text.replace('<?xml version="1.0" encoding="UTF-8"?>', "")
        # xml_string = op_result.text.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
        # Define custom entities for é, ï, and ü characters
        entity_definitions = "<!DOCTYPE root [\n"
        entity_definitions += '<!ENTITY eacute "&#233;">\n'
        entity_definitions += '<!ENTITY iuml "&#239;">\n'
        entity_definitions += '<!ENTITY uuml "&#252;">\n'
        entity_definitions += '<!ENTITY rsquo "&#x2019;">\n'
        entity_definitions += "]>\n"
        # Parse XML string into an Element object
        response_dict = xmltodict.parse(entity_definitions + xml_string)
        return response_dict


def config_gateway(security_key, payment_api_url, query_api_url):
    Nmi.security_key = security_key
    Nmi.payment_api_url = payment_api_url
    Nmi.query_api_url = query_api_url
