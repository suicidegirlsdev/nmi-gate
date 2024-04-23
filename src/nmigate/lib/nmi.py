class Nmi:
    # Can set these on the class at app init to avoid passing on every use.
    security_token = None
    payment_api_url = None
    query_api_url = None

    def __init__(self, security_token=None, payment_api_url=None, query_api_url=None):
        if security_token:
            self.security_token = security_token
        if payment_api_url:
            self.payment_api_url
        if query_api_url:
            self.query_api_url

        # Ensure minimum required values are set.
        if not self.security_token:
            raise ValueError("NMI gateway requires the security token (key) to be set.")
        if not self.payment_api_url:
            raise ValueError("NMI gateway requires the payment API URL to be set.")
        # This is not used with many of the API calls, but keeping it consistent for simplicity.
        if not self.query_api_url:
            raise ValueError("NMI gateway requires the query API URL to be set.")
