from nmigate.lib.nmi import Nmi


class Billing(Nmi):
    def validate_billing_id(self, customer_vault_id, billing_id):
        data = {
            "type": "validate",
            "security_key": self.security_key,
            "customer_vault_id": customer_vault_id,
            "billing_id": billing_id,
        }

        return self._post_payment_api_request(data)

    def add(self, billing_req):
        data = {
            "customer_vault": "add_billing",
            "payment": "creditcard",
            "security_key": self.security_key,
            "payment_token": billing_req["token"],
            "customer_vault_id": billing_req["user_id"],
            "billing_id": billing_req["billing_id"],
        }
        data.update(billing_req["billing_info"])
        return self._post_payment_api_request(data)

    def update(self, billing_req):
        data = {
            "customer_vault": "update_billing",
            "payment": "creditcard",
            "security_key": self.security_key,
            "payment_token": billing_req["token"],
            "customer_vault_id": billing_req["user_id"],
            "billing_id": billing_req["billing_id"],
        }
        data.update(billing_req["billing_info"])
        return self._post_payment_api_request(data)

    def delete(self, user_id, billing_id):
        data = {
            "customer_vault": "delete_billing",
            "security_key": self.security_key,
            "customer_vault_id": user_id,
            "billing_id": billing_id,
        }
        return self._post_payment_api_request(data)

    def change_subscription_billing(self, request):
        data = {
            "recurring": "update_subscription",
            "security_key": self.security_key,
            "customer_vault_id": request.get("user_id"),
            "subscription_id": request.get("subscription_id"),
            "billing_id": request.get("billing_id"),
        }

        return self._post_payment_api_request(data)

    def set_priority(self, user_id, billing_id, priority):
        data = {
            "customer_vault": "update_billing",
            "security_key": self.security_key,
            "customer_vault_id": user_id,
            "billing_id": billing_id,
            "priority": priority,
        }
        return self._post_payment_api_request(data)
