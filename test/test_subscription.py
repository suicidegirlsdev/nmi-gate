import unittest

from nmigate import config_gateway
from nmigate.subscription import Subscription


class TestSubs(unittest.TestCase):
    def setUp(self):
        config_gateway(
            "6457Thfj624V5r7WUwc5v6a68Zsd6YEm",
            "https://ecsuite.transactiongateway.com/api/transact.php",
            "https://ecsuite.transactiongateway.com/api/query.php",
        )

    def test_get_plans(self):
        subscriptions = Subscription()
        info = subscriptions.get_info("8462293105")
        self.assertEqual(info["subscription"]["subscription_id"], "8462293105")

    def test_custom_sale_using_vault(self):
        subscriptions = Subscription()
        result = subscriptions.custom_sale_using_vault(
            plan_id="swzpremiumyear", customer_vault_id="1", create_customer_vault=False
        )
        self.assertEqual(result["response_code"], "100")

    def test_custom_sale_using_vault_month_frequency(self):
        subscriptions = Subscription()
        result = subscriptions.custom_sale_using_vault_month_frequency(
            request_sub={
                "user_id": "1",
                "total_amount": "11",
                "custom_subscription_info": {
                    "plan_payments": "13",
                    "plan_amount": "12",
                    "month_frequency": "1",
                    "day_of_month": "1",
                },
            }
        )
        print(result)
        self.assertEqual(result["response_code"], "100")

    def test_custom_with_sale_and_vault_day_frequency(self):
        subscriptions = Subscription()
        result = subscriptions.custom_with_sale_and_vault_day_frequency(
            request_sub={
                "user_id": "1",
                "total_amount": "14",
                "custom_subscription_info": {
                    "plan_payments": "15",
                    "plan_amount": "6",
                    "day_frequency": "1",
                },
            }
        )
        print(result)
        self.assertEqual(result["response_code"], "100")

    def test_delete_subscription(self):
        subscriptions = Subscription()
        info = subscriptions.delete("8462218027")
        self.assertEqual(info["response_code"], 100)

    def test_pause_subscription(self):
        transactions = Subscription()
        result = transactions.pause("8926648990", True)
        print(result)
        self.assertEqual(result["response_code"], "100")


if __name__ == "__main__":
    unittest.main()
