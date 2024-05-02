import uuid

from ..nmi import Nmi


class BillingRecord(Nmi):
    def __init__(self, customer_id, billing_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer_id = customer_id
        # If no billing_id passed then only "add" can be used
        # and it will generate one.
        self.billing_id = billing_id

    def _create_data(self, payment_action, **extra):
        if not self.billing_id:
            raise ValueError("Billing ID is required")
        return {
            "security_key": self.security_key,
            "type": payment_action,
            "customer_vault_id": self.customer_id,
            "billing_id": self.billing_id,
            **extra,
        }

    def validate(self):
        data = self._create_data("validate")
        return self._post_payment_api_request(data)

    def add(self, payment_token, billing_info, **extra):
        if not self.billing_id:
            # API does not state a max, but including hyphens failed with "too long".
            # The hex version appears to work, though.
            self.billing_id = uuid.uuid4().hex

        data = self._create_data(
            "add_billing",
            payment="creditcard",
            payment_token=payment_token,
            **billing_info,
            **extra,
        )
        return self._post_payment_api_request(data)

    def update(self, payment_token, billing_info=None, **extra):
        data = self._create_data(
            "update_billing",
            payment="creditcard",
            payment_token=payment_token,
            **(billing_info or {}),
            **extra,
        )
        return self._post_payment_api_request(data)

    def delete(self):
        data = self._create_data("delete_billing")
        return self._post_payment_api_request(data)

    def set_priority(self, priority):
        if not self.billing_id:
            raise ValueError("Billing ID is required")
        data = {
            "customer_vault": "update_billing",
            "security_key": self.security_key,
            "customer_vault_id": self.customer_id,
            "billing_id": self.billing_id,
            "priority": priority,
        }
        return self._post_payment_api_request(data)

    def _post_payment_api_request(self, data):
        """
        The API docs suggest the billing id isn't returned in responses,
        even when the API creates the billing id. For consistency,
        include the one passed-in or created by us in every response.
        """
        response = super()._post_payment_api_request(data)
        if "billing_id" not in response:
            response["billing_id"] = self.billing_id
        return response
