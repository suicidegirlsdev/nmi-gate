import unittest

from nmigate import config_gateway
from nmigate.customer import BillingRecord


class TestBilling(unittest.TestCase):
    def setUp(self):
        config_gateway(
            "6457Thfj624V5r7WUwc5v6a68Zsd6YEm",
            "https://ecsuite.transactiongateway.com/api/transact.php",
            "https://ecsuite.transactiongateway.com/api/query.php",
        )

    def test_add(self):
        billing = BillingRecord("1", "132")
        res = billing.add(
            "00000000-000000-000000-000000000000",
            {
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
        )
        self.assertEqual(res["response_code"], "100")

    def test_update(self):
        billing = BillingRecord("1", "132")
        res = billing.add(
            "00000000-000000-000000-000000000000",
            {
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
        )
        print(res)
        self.assertEqual(res["response_code"], "100")

    def test_delete(self):
        billing = BillingRecord("1", "132")
        res = billing.delete()
        self.assertEqual(res["response_code"], "100")

    def test_set_priority(self):
        billing = BillingRecord("1", "132")
        res = billing.set_priority("1")
        print(res)
        self.assertEqual(res["response_code"], "100")
