import unittest

from nmigate import config_gateway
from nmigate.customer import CustomerVault


class TestCustomerVault(unittest.TestCase):
    def setUp(self):
        config_gateway(
            "6457Thfj624V5r7WUwc5v6a68Zsd6YEm",
            "https://ecsuite.transactiongateway.com/api/transact.php",
            "https://ecsuite.transactiongateway.com/api/query.php",
        )

    def test_create_customer_vault(self):
        customer_vault = CustomerVault("51asdfsf234asdfasfasfsa")
        result = customer_vault.create(
            "00000000-000000-000000-000000000000",
            billing_id="51asdfsf234asdfasfasfsa",
            billing_info={
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
        self.assertEqual(result["response_code"], 100)

    def test_pay_with_customer_vault(self):
        # The original test is broken requires an initial trans id
        # but wasn't supplied
        customer_vault = CustomerVault("1")
        result = customer_vault.charge(
            10,
            "8926614344",
        )
        self.assertEqual(result["response_code"], "100")

    def test_get_customer_info(self):
        customer_vault = CustomerVault("1")
        result = customer_vault.get_info()
        self.assertEqual(
            result["customer_vault"]["customer"]["customer_vault_id"],
            "1",
        )
