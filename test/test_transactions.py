import unittest

from nmigate import config_gateway
from nmigate.payment import Transactions


class TestTransactions(unittest.TestCase):
    def setUp(self):
        config_gateway(
            "6457Thfj624V5r7WUwc5v6a68Zsd6YEm",
            "https://ecsuite.transactiongateway.com/api/transact.php",
            "https://ecsuite.transactiongateway.com/api/query.php",
        )

    def test_charge_token(self):
        transactions = Transactions()
        result = transactions.charge_token(
            "00000000-000000-000000-000000000000",
            5,
            {
                "first_name": "test",
                "last_name": "test",
                "company": "test",
                "address1": "test",
                "city": "test",
                "state": "test",
                "zip": "test",
                "country": "test",
                "phone": "test",
                "email": "test",
            },
        )
        self.assertEqual(result["response_code"], "100")

    def test_refund(self):
        transactions = Transactions("8926614344")
        result = transactions.refund()
        self.assertEqual(result["response_code"], "100")

    def test_get_billing_info_by_transaction_id(self):
        transactions = Transactions("8926649228")
        result = transactions.get_info()
        self.assertEqual(result["transaction"]["transaction_id"], "8926649228")
