import unittest

from nmigate.lib.customer_vault import CustomerVault


class TestCustomerVault(unittest.TestCase):
    def test_create_customer_vault(self):
        customer_vault = CustomerVault("6457Thfj624V5r7WUwc5v6a68Zsd6YEm")
        result = customer_vault.create(
            {
                "id": "51asdfsf234asdfasfasfsa",
                "token": "00000000-000000-000000-000000000000",
                "billing_id": "51asdfsf234asdfasfasfsa",
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
        self.assertEqual(result["response_code"][0], 100)

    def test_get_billing_info_by_transaction_id(self):
        customer_vault = CustomerVault("6457Thfj624V5r7WUwc5v6a68Zsd6YEm")
        result = customer_vault.get_billing_info_by_transaction_id("8926649228")
        self.assertEqual(result["transaction"]["transaction_id"], "8926649228")

    def test_get_customer_info(self):
        customer_vault = CustomerVault("6457Thfj624V5r7WUwc5v6a68Zsd6YEm")
        result = customer_vault.get_customer_info("1")
        self.assertEqual(
            result["customer_vault"]["customer"]["customer_vault_id"],
            "1",
        )

    def test_validate_customer_id(self):
        customer_vault = CustomerVault("6457Thfj624V5r7WUwc5v6a68Zsd6YEm")
        result = customer_vault.validate_customer_vault("1")
        print(result)
