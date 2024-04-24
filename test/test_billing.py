import unittest

from nmigate import Billing, config_gateway


class TestBilling(unittest.TestCase):
    def setUp(self):
        config_gateway(
            "6457Thfj624V5r7WUwc5v6a68Zsd6YEm",
            "https://ecsuite.transactiongateway.com/api/transact.php",
            "https://ecsuite.transactiongateway.com/api/query.php",
        )

    def test_add(self):
        billing = Billing()
        res = billing.add(
            {
                "user_id": "1",
                "billing_id": "132",
                "token": "00000000-000000-000000-000000000000",
                "billing_info": {
                    "first_name": "1",
                    "last_name": "1",
                    "address1": "1",
                    "city": "1",
                    "state": "1",
                    "zip": "1",
                    "country": "1",
                    "phone": "1",
                    "email": "1",
                },
            }
        )
        self.assertEqual(res["response_code"], "100")

    def test_update(self):
        billing = Billing()
        res = billing.update(
            {
                "user_id": "1",
                "billing_id": "132",
                "token": "00000000-000000-000000-000000000000",
                "billing_info": {
                    "first_name": "Peter",
                    "last_name": "1",
                    "address1": "1",
                    "city": "12",
                    "state": "1",
                    "zip": "1",
                    "country": "1",
                    "phone": "1",
                    "email": "1",
                },
            }
        )
        print(res)
        self.assertEqual(res["response_code"], "100")

    def test_delete(self):
        billing = Billing()
        res = billing.delete("1", "132")
        self.assertEqual(res["response_code"], "100")

    def test_change_subscription_billing(self):
        billing = Billing()
        res = billing.change_subscription_billing(
            {
                "user_id": "1",
                "billing_id": "12",
                "subscription_id": "8965562207",
            }
        )
        print(res)
        self.assertEqual(res["response_code"], "100")

    def test_set_priority(self):
        billing = Billing()
        res = billing.set_priority("1", "f00da1e2689d4dbca6d8c611e62e824d", "1")
        print(res)
        self.assertEqual(res["response_code"], "100")
