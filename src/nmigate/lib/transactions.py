from typing import Any, Dict, Union

from nmigate.lib.nmi import Nmi


class Transactions(Nmi):
    def pay_with_token(self, payment_request) -> Dict[str, Union[Any, str]]:
        data = {
            "type": "sale",
            "security_key": self.security_key,
            "payment_token": payment_request["token"],
            "amount": payment_request["total"],
        }
        data.update(payment_request["billing_info"])
        return self._post_payment_api_request(data)

    def pay_with_customer_vault(self, payment_request) -> Dict[str, Union[Any, str]]:
        data = {
            "security_key": self.security_key,
            "customer_vault_id": payment_request["user_id"],
            "amount": payment_request["total"],
            "initiated_by": "merchant",
            "stored_credential_indicator": "used",
            "initial_transaction_id": payment_request["transaction_id"],
        }
        return self._post_payment_api_request(data)

    def refund(self, transaction_id) -> Dict[str, Union[Any, str]]:
        data = {
            "type": "refund",
            "payment": "creditcard",
            "amount": 0,
            "security_key": self.security_key,
            "transactionid": transaction_id,
        }

        return self._post_payment_api_request(data)
