import uuid

from ..nmi import Nmi


class CustomerVault(Nmi):
    def __init__(self, customer_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If no customer_id passed then only "create" can be used
        # and it will generate one.
        self.customer_id = customer_id

        # This will only get set if "create" is called
        self.billing_id = None

    def _create_data(self, vault_action, **extra):
        if not self.customer_id:
            raise ValueError("Customer ID is required")
        return {
            "security_key": self.security_key,
            "customer_vault": vault_action,
            "customer_vault_id": self.customer_id,
            **extra,
        }

    def create(
        self,
        payment_token,
        billing_info,
        # Generated if not passed
        billing_id=None,
    ):
        if not self.customer_id:
            self.customer_id = uuid.uuid4().hex

        self.billing_id = billing_id or uuid.uuid4().hex

        data = self._create_data(
            "add_customer",
            type="validate",
            initiated_by="customer",
            stored_credential_indicator="stored",
            payment_token=payment_token,
            billing_id=self.billing_id,
            **billing_info,
        )
        response = self._post_payment_api_request(data)
        # Make sure the billing_id used gets returned
        if "billing_id" not in response:
            response["billing_id"] = self.billing_id
        return response

    def charge(self, amount, initial_transaction_id, initiated_by_customer=False):
        if not self.customer_id:
            self.customer_id = uuid.uuid4().hex

        data = {
            "security_key": self.security_key,
            "customer_vault_id": self.customer_id,
            "amount": amount,
            "initiated_by": "customer" if initiated_by_customer else "merchant",
            "stored_credential_indicator": "used",
            "initial_transaction_id": initial_transaction_id,
        }
        return self._post_payment_api_request(data)

    def validate(self):
        if not self.customer_id:
            raise ValueError("Customer ID is required")
        data = {
            "type": "validate",
            "security_key": self.security_key,
            "customer_vault_id": self.customer_id,
            "amount": "0.00",
        }
        return self._post_payment_api_request(data)

    def delete(self):
        data = {
            "customer_vault": "delete_customer",
            "security_key": self.security_key,
            "customer_vault_id": self.customer_id,
        }
        return self._post_payment_api_request(data)

    def get_info(self):
        if not self.customer_id:
            raise ValueError("Customer ID is required")
        data = {
            "report_type": "customer_vault",
            "security_key": self.security_key,
            "customer_vault_id": self.customer_id,
        }
        return self._post_query_api_request(data)
