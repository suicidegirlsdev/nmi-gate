from ..nmi import Nmi


class Transaction(Nmi):
    def __init__(self, transaction_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If no transaction_id passed then only "pay_with_token" can be used
        # and it will generate one.
        # For paying with customer vault, transaction_id should be the appropriate
        # initial transaction id from when the card was first used/stored.
        self.transaction_id = transaction_id

    def charge_token(self, payment_token, amount, billing_info):
        data = {
            "type": "sale",
            "security_key": self.security_key,
            "payment_token": payment_token,
            "amount": amount,
            **billing_info,
        }
        response = self._post_payment_api_request(data)
        self.transaction_id = response.get("transactionid")
        return response

    def partial_refund(self, amount):
        data = {
            "type": "refund",
            "payment": "creditcard",
            "amount": amount,
            "security_key": self.security_key,
            "transactionid": self.transaction_id,
        }
        return self._post_payment_api_request(data)

    def refund(self):
        # 0.00 indicates full refund
        return self.partial_refund("0.00")

    def get_info(self):
        query = {
            "security_key": self.security_key,
            "transaction_id": self.transaction_id,
        }
        return self._post_query_api_request(query)
