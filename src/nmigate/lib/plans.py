from typing import Any, Dict, Union

from nmigate.lib.nmi import Nmi
from nmigate.util.wrappers import postProcessingOutput, postProcessXml


class Plans(Nmi):
    @postProcessingOutput
    def add_plan_by_month_config(self, data) -> Dict[str, Union[Any, str]]:
        data = {
            "recurring": "add_plan",
            "security_key": self.security_key,
            "plan_amount": data["plan_amount"],
            "plan_name": data["plan_name"],
            "plan_id": data["plan_id"],
            "month_frequency": data["month_frequency"],
            "day_of_month": data["day_of_month"],
            "plan_payments": data["plan_payments"],
        }
        response = self._post_payment_api_request(data)
        return {
            "response": response,
            "req": data,
            "type": "add_plan_by_month_config",
        }

    @postProcessingOutput
    def edit_plan_by_month_config(self, data) -> Dict[str, Union[Any, str]]:
        data = {
            "recurring": "edit_plan",
            "security_key": self.security_key,
            "plan_amount": data["plan_amount"],
            "plan_name": data["plan_name"],
            "current_plan_id": data["plan_id"],
            "month_frequency": data["month_frequency"],
            "day_of_month": data["day_of_month"],
            "plan_payments": data["plan_payments"],
        }
        response = self._post_payment_api_request(data)
        return {
            "response": response,
            "req": data,
            "type": "edit_plan_by_month_config",
        }

    @postProcessingOutput
    def add_plan_by_day_frequency(self, data) -> Dict[str, Union[Any, str]]:
        data = {
            "recurring": "add_plan",
            "security_key": self.security_key,
            "plan_amount": data["plan_amount"],
            "plan_name": data["plan_name"],
            "plan_id": data["plan_id"],
            "day_frequency": data["day_frequency"],
            "plan_payments": data["plan_payments"],
        }
        response = self._post_payment_api_request(data)
        return {
            "response": response,
            "req": data,
            "type": "add_plan_by_day_frequency",
        }

    @postProcessingOutput
    def edit_plan_by_day_frequency(self, data) -> Dict[str, Union[Any, str]]:
        data = {
            "recurring": "edit_plan",
            "security_key": self.security_key,
            "plan_amount": data["plan_amount"],
            "plan_name": data["plan_name"],
            "current_plan_id": data["plan_id"],
            "day_frequency": data["day_frequency"],
            "plan_payments": data["plan_payments"],
        }
        response = self._post_payment_api_request(data)
        return {
            "response": response,
            "req": data,
            "type": "edit_plan_by_day_frequency",
        }

    @postProcessXml
    def get_all_plans(self) -> Any:
        query = {
            "security_key": self.security_key,
            "report_type": "recurring_plans",
        }
        return self._post_query_api_request(query)

    # @postProcessXml
    def get_plan(self, id) -> Union[None, Dict[str, Any]]:
        plans = self.get_all_plans()
        for plan in plans["nm_response"]["plan"]:
            if plan["plan_id"] == id:
                return plan

        return None
