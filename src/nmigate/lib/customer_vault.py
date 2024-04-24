import uuid
from typing import Any, Dict, Union

from nmigate.lib.nmi import Nmi


class CustomerVault(Nmi):
    def create(self, vault_request) -> Dict[str, Union[Any, str]]:
        uid = (uuid.uuid4().hex,)

        data = {
            "customer_vault": "add_customer",
            "type": "validate",
            "initiated_by": "customer",
            "stored_credential_indicator": "stored",
            "security_key": self.security_key,
            "customer_vault_id": vault_request["id"] if vault_request["id"] else uid,
            "payment_token": vault_request["token"],
            "billing_id": vault_request["billing_id"],
        }
        data.update(vault_request["billing_info"])
        return self._post_payment_api_request(data)

    def update(self, id: str, billing_info) -> Dict[str, Union[Any, str]]:
        data = {
            "customer_vault": "update_customer",
            "security_key": self.security_key,
            "customer_vault_id": id,
        }
        data.update(billing_info)
        return self._post_payment_api_request(data)

    def validate(self, user_id: str) -> Dict[str, Union[Any, str]]:
        query = {
            "security_key": self.security_key,
            "customer_vault_id": user_id,
            "amount": "0.00",
            "type": "validate",
        }
        return self._post_payment_api_request(query)

    def get_billing_info_by_transaction_id(self, transaction_id) -> Any:
        query = {
            "security_key": self.security_key,
            "transaction_id": transaction_id,
        }
        return self._post_query_api_request(query)

    def get_customer_info(self, id) -> Any:
        query = {
            "report_type": "customer_vault",
            "security_key": self.security_key,
            "customer_vault_id": id,
        }
        return self._post_query_api_request(query)

    def delete(self, id: str) -> Dict[str, Union[Any, str]]:
        data = {
            "customer_vault": "delete_customer",
            "security_key": self.security_key,
            "customer_vault_id": id,
        }
        return self._post_payment_api_request(data)
