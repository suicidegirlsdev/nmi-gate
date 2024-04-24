import unittest

from nmigate import Plans, config_gateway


class TestPlans(unittest.TestCase):
    def setUp(self):
        config_gateway(
            "6457Thfj624V5r7WUwc5v6a68Zsd6YEm",
            "https://ecsuite.transactiongateway.com/api/transact.php",
            "https://ecsuite.transactiongateway.com/api/query.php",
        )

    def test_get_plans(self):
        plansObj = Plans()
        response = plansObj.get_all_plans()
        plans = response["plan"]
        self.assertGreater(len(plans), 0)

    def test_get_plan(self):
        plans = Plans()
        response = plans.get_plan("swzshoppingonly")
        self.assertEqual(response["plan_id"], "swzshoppingonly")

    def test_add_plan_by_day_frequency(self):
        plans = Plans()
        response = plans.add_plan_by_day_frequency(
            {
                "plan_amount": "10.00",
                "plan_name": "test",
                "plan_id": "test",
                "day_frequency": "1",
                "plan_payments": "0",
            }
        )
        self.assertEqual(response["response_code"], "100")
        self.assertEqual(response["successfull"], True)

    def test_edit_plan_by_day_frequency(self):
        plans = Plans()
        response = plans.edit_plan_by_day_frequency(
            {
                "recurring": "edit_plan",
                "plan_amount": "10.00",
                "plan_name": "test",
                "plan_id": "test",
                "day_frequency": "2",
                "plan_payments": "0",
            }
        )
        self.assertEqual(response["response_code"], "100")
        self.assertEqual(response["successfull"], True)

    def test_add_plan_by_month_config(self):
        plans = Plans()
        response = plans.add_plan_by_month_config(
            {
                "plan_amount": "10.00",
                "plan_name": "test",
                "plan_id": "test1",
                "month_frequency": "1",
                "day_of_month": "1",
                "plan_payments": "0",
            }
        )

        self.assertEqual(response["response_code"], "100")
        self.assertEqual(response["successfull"], True)

    def test_edit_plan_by_month_config(self):
        plans = Plans()
        response = plans.edit_plan_by_month_config(
            {
                "plan_amount": "10.00",
                "plan_name": "test",
                "plan_id": "test1",
                "month_frequency": "1",
                "day_of_month": "10",
                "plan_payments": "0",
            }
        )

        self.assertEqual(response["response_code"], "100")
        self.assertEqual(response["successfull"], True)


if __name__ == "__main__":
    unittest.main()
