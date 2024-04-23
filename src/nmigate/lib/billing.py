
from nmigate.lib.nmi import Nmi
from nmigate.util.wrappers import postProcessingOutput


class Billing(Nmi):
    @postProcessingOutput
    def validate_billing_id(self, customer_vault_id, billing_id):
        data = {
            "type": "validate",
            "security_key": self.security_key,
            "customer_vault_id": customer_vault_id,
            "billing_id": billing_id,
        }

        response = self._post_payment_api_request(data)
        return {"response": response, "type": "validate_billing_id"}

    @postProcessingOutput
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
        res = self._post_payment_api_request(data)
        return {"response": res, "type": "add_billing_info"}

    @postProcessingOutput
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
        response = self._post_payment_api_request(data)
        return {"response": response, "type": "update_billing_info"}

    @postProcessingOutput
    def delete(self, user_id, billing_id):
        data = {
            "customer_vault": "delete_billing",
            "security_key": self.security_key,
            "customer_vault_id": user_id,
            "billing_id": billing_id,
        }
        response = self._post_payment_api_request(data)
        return {"response": response, "type": "delete_billing_info"}

    @postProcessingOutput
    def change_subscription_billing(self, request):
        data = {
            "recurring": "update_subscription",
            "security_key": self.security_key,
            "customer_vault_id": request.get("user_id"),
            "subscription_id": request.get("subscription_id"),
            "billing_id": request.get("billing_id"),
        }

        response = self._post_payment_api_request(data)
        return {
            "response": response,
            "req": request,
            "type": "update_subscription_billing",
        }

    @postProcessingOutput
    def set_priority(self, user_id, billing_id, priority):
        data = {
            "customer_vault": "update_billing",
            "security_key": self.security_key,
            "customer_vault_id": user_id,
            "billing_id": billing_id,
            "priority": priority,
        }
        response = self._post_payment_api_request(data)
        return {"response": response, "type": "set_priority"}
