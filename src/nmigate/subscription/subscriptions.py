from typing import Any, Dict, Union

from ..nmi import Nmi
from .plans import Plans


class Subscriptions(Nmi):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plans = Plans(*args, **kwargs)

    def custom_sale_using_vault(
        self, plan_id, customer_vault_id, transaction_id, create_customer_vault=False
    ) -> Dict[str, Union[Any, str]]:
        plan = self.plans.get_plan(plan_id)

        plan_amount = plan["plan_amount"] if plan else None

        data = {
            "type": "sale",
            "recurring": "add_subscription",
            "initiated_by": "merchant",
            "stored_credential_indicator": "used",
            "initial_transaction_id": transaction_id,
            "security_key": self.security_key,
            "amount": str(plan_amount),
            "customer_vault_id": customer_vault_id,
            "plan_id": plan_id,
        }
        data["customer_vault"] = "add_customer" if create_customer_vault else None

        return self._post_payment_api_request(data)

    """  if amount = 0 then its a simple subscription, if amount = 1 then its a subscription with sale """

    def custom_sale_using_vault_month_frequency(
        self, request_sub
    ) -> Dict[str, Union[Any, str]]:
        data = {
            "type": "sale",
            "recurring": "add_subscription",
            "billing_method": "recurring",
            "initiated_by": "merchant",
            "stored_credential_indicator": "used",
            "initial_transaction_id": request_sub["transaction_id"],
            "security_key": self.security_key,
            "customer_vault_id": request_sub["user_id"],
            "amount": request_sub["total_amount"],
            "plan_payments": request_sub["custom_subscription_info"]["plan_payments"],
            "plan_amount": request_sub["custom_subscription_info"]["plan_amount"],
            "month_frequency": request_sub["custom_subscription_info"][
                "month_frequency"
            ],
            "day_of_month": request_sub["custom_subscription_info"]["day_of_month"],
        }

        if float(request_sub["total_amount"]) == 0:
            del data["type"]
            del data["amount"]

        return self._post_payment_api_request(data)

    def custom_with_sale_and_vault_day_frequency(
        self, request_sub
    ) -> Dict[str, Union[Any, str]]:
        data = {
            "type": "sale",
            "recurring": "add_subscription",
            "billing_method": "recurring",
            "initiated_by": "merchant",
            "stored_credential_indicator": "used",
            "initial_transaction_id": request_sub["transaction_id"],
            "security_key": self.security_key,
            "amount": request_sub["total_amount"],
            "customer_vault_id": request_sub["user_id"],
            "plan_payments": request_sub["custom_subscription_info"]["plan_payments"],
            "plan_amount": request_sub["custom_subscription_info"]["plan_amount"],
            "day_frequency": request_sub["custom_subscription_info"]["day_frequency"],
        }

        if float(request_sub["total_amount"]) == 0:
            del data["type"]
            del data["amount"]

        return self._post_payment_api_request(data)

    def get_info(self, id) -> Any:
        query = {
            "report_type": "recurring",
            "security_key": self.security_key,
            "subscription_id": id,
        }
        return self._post_query_api_request(query)

    def delete(self, subscription_id):
        data = {
            "recurring": "delete_subscription",
            "security_key": self.security_key,
            "subscription_id": subscription_id,
        }
        return self._post_payment_api_request(data)

    def pause(self, subscription_id, pause):
        data = {
            "recurring": "update_subscription",
            "security_key": self.security_key,
            "subscription_id": subscription_id,
            "paused_subscription": str(pause).lower(),
        }
        return self._post_payment_api_request(data)

    def update_month_subscription(
        self,
        subscription_id: str,
        customer_vault_id: str,
        billing_id: str,
        billing_info,
        plan_payments: str,
        plan_amount: str,
        day_of_month: str,
        month_frequency: str,
        start_date: str,
    ):
        data = {
            "recurring": "update_subscription",
            "security_key": self.security_key,
            "subscription_id": subscription_id,
            "customer_vault_id": customer_vault_id,
            "billing_id": billing_id,
            "plan_payments": plan_payments,
            "plan_amount": plan_amount,
            "day_of_month": day_of_month,
            "month_frequency": month_frequency,
            "start_date": start_date,  # YYYYMMDD
        }
        data.update(billing_info)

        return self._post_payment_api_request(data)

    def update_day_subscription(
        self,
        subscription_id: str,
        customer_vault_id: str,
        billing_id: str,
        billing_info,
        plan_payments: str,
        plan_amount: str,
        day_frequency: str,
        start_date: str,
    ):
        data = {
            "recurring": "update_subscription",
            "security_key": self.security_key,
            "subscription_id": subscription_id,
            "customer_vault_id": customer_vault_id,
            "billing_id": billing_id,
            "plan_payments": plan_payments,
            "plan_amount": plan_amount,
            "day_frequency": day_frequency,
            "start_date": start_date,  # YYYYMMDD
        }
        data.update(billing_info)

        return self._post_payment_api_request(data)

    def change_subscription_billing(self, billing_id, subscription_id):
        # This should prob be in subscriptions.py
        data = self._create_data(
            "",
            billing_id,
            recurring="update_subscription",
            subscription_id=subscription_id,
        ).pop("type")

        return self._post_payment_api_request(data)
