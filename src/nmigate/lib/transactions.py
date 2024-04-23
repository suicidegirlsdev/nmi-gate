from typing import Any, Dict, Union

import requests

from nmigate.lib.nmi import Nmi
from nmigate.util.wrappers import log, postProcessingOutput


class Transactions(Nmi):
    @postProcessingOutput
    def pay_with_token(self, payment_request) -> Dict[str, Union[Any, str]]:
        data = {
            "type": "sale",
            "security_key": self.security_key,
            "payment_token": payment_request["token"],
            "amount": payment_request["total"],
        }
        data.update(payment_request["billing_info"])
        response = requests.post(self.payment_api_url, data=data)
        return {
            "response": response,
            "req": payment_request,
            "type": "pay_with_token",
        }

    @postProcessingOutput
    def pay_with_customer_vault(self, payment_request) -> Dict[str, Union[Any, str]]:
        data = {
            "security_key": self.security_key,
            "customer_vault_id": payment_request["user_id"],
            "amount": payment_request["total"],
            "initiated_by": "merchant",
            "stored_credential_indicator": "used",
            "initial_transaction_id": payment_request["transaction_id"],
        }
        response = requests.post(self.payment_api_url, data=data)
        return {
            "response": response,
            "req": payment_request,
            "type": "pay_with_customer_vault",
        }

    @postProcessingOutput
    def refund(self, transaction_id) -> Dict[str, Union[Any, str]]:
        data = {
            "type": "refund",
            "payment": "creditcard",
            "amount": 0,
            "security_key": self.security_key,
            "transactionid": transaction_id,
        }

        response = requests.post(url=self.payment_api_url, data=data)
        return {
            "response": response,
            "req": {"transaction_id": transaction_id},
            "type": "refund",
        }
