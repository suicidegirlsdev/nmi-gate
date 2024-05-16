import uuid

from ..nmi import Nmi
from ..utils import normalize_merchant_defined_fields


class CustomerVault(Nmi):
    def __init__(self, customer_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If no customer_id passed then only "create" can be used
        # and it will generate one.
        self.customer_id = customer_id

        # This will only get set if "create" is called
        self.billing_id = None

    def _create_data(self, vault_action, ip_address="", is_recurring=True, **extra):
        if not self.customer_id:
            raise ValueError("Customer ID is required")
        data = {
            "security_key": self.security_key,
            "customer_vault": vault_action,
            "customer_vault_id": self.customer_id,
            **extra,
        }
        if ip_address:
            data["ipaddress"] = ip_address
        if is_recurring:
            data["billing_method"] = "recurring"
        return data

    def init_credentials_on_file(
        self,
        billing_id,
        ip_address="",
        is_recurring=True,
        amount=None,
        order_id="",
        order_description="",
        merchant_defined_fields=None,
        **extra,
    ):
        """
        Special case for when cards where stored into the vault but were
        not setup to work with Credentials on File/don't have a stored
        initial_transaction_id. Per support, they should be initialized
        into the CoF system before they being used for merchant initiated
        transactions.

        Can pass no amount to allow initialization without a charge.
        Make sure to save the transaction_id for future use.

        Billing_id is mandatory arg since will usually want it, but can pass
        None if sure you don't need it.
        """
        data = {
            "security_key": self.security_key,
            "customer_vault_id": self.customer_id,
            "stored_credential_indicator": "stored",
            "initiated_by": "customer",
            **extra,
        }
        if billing_id:
            data["billing_id"] = billing_id

        if ip_address:
            data["ipaddress"] = ip_address

        if amount:
            data["amount"] = amount
            data["type"] = "sale"
        else:
            data["type"] = "validate"

        if order_id:
            data["orderid"] = order_id

        if is_recurring:
            data["billing_method"] = "recurring"

        if order_description:
            data["order_description"] = order_description

        if merchant_defined_fields:
            data.update(normalize_merchant_defined_fields(merchant_defined_fields))

        return self._post_payment_api_request(data)

    def _create(
        self,
        payment_token,
        billing_info,
        # "sale" or "validate". Former should include amount
        trans_type,
        amount=None,
        ip_address="",
        # Generated if not passed
        billing_id="",
        order_id="",
        order_description="",
        **extra,
    ):
        if not self.customer_id:
            self.customer_id = uuid.uuid4().hex

        self.billing_id = billing_id or uuid.uuid4().hex

        data = self._create_data(
            "add_customer",
            ip_address=ip_address,
            # Even support didn't seem 100% certain, but it seems like
            # if we are ever going to want to do a recurring charge then
            # this should be true during initial setup.
            is_recurring=True,
            type=trans_type,
            initiated_by="customer",
            stored_credential_indicator="stored",
            payment_token=payment_token,
            billing_id=self.billing_id,
            **billing_info,
            **extra,
        )
        if amount:
            data["amount"] = amount
        if order_id:
            data["orderid"] = order_id
        if order_description:
            data["order_description"] = order_description

        response = self._post_payment_api_request(data)
        # Make sure the billing_id used gets returned
        if "billing_id" not in response:
            response["billing_id"] = self.billing_id
        return response

    def create(
        self,
        payment_token,
        billing_info,
        ip_address="",
        # Generated if not passed
        billing_id="",
        **extra,
    ):
        return self._create(
            payment_token,
            billing_info,
            ip_address=ip_address,
            trans_type="validate",
            billing_id=billing_id,
            **extra,
        )

    def charge_and_create(
        self,
        payment_token,
        amount,
        billing_info,
        ip_address="",
        # Generated if not passed
        billing_id="",
        order_id="",
        order_description="",
        merchant_defined_fields=None,
        **extra,
    ):
        if merchant_defined_fields:
            extra.update(normalize_merchant_defined_fields(merchant_defined_fields))

        return self._create(
            payment_token,
            billing_info,
            ip_address=ip_address,
            trans_type="sale",
            amount=amount,
            billing_id=billing_id,
            order_id=order_id,
            order_description=order_description,
            **extra,
        )

    def charge(
        self,
        amount,
        initial_transaction_id,
        initiated_by_customer=False,
        is_recurring=True,
        order_description="",
        merchant_defined_fields=None,
        # Only used with customer initiated.
        ip_address="",
        order_id="",
        **extra,
    ):
        # Pass merchant_defined_fields as a sparse array-like dict: {1: 'value', ...}
        # Where the number corresponds to the configured Merchant Defined Field <number>
        # the gateway merchant console. Can be 1-20.
        if not self.customer_id:
            self.customer_id = uuid.uuid4().hex

        data = {
            "type": "sale",
            "security_key": self.security_key,
            "customer_vault_id": self.customer_id,
            "amount": amount,
            "initiated_by": "customer" if initiated_by_customer else "merchant",
            "stored_credential_indicator": "used",
            "initial_transaction_id": initial_transaction_id,
            "order_description": order_description,
            **extra,
        }

        if is_recurring:
            data["billing_method"] = "recurring"

        if initiated_by_customer and ip_address:
            data["ipaddress"] = ip_address

        if merchant_defined_fields:
            data.update(normalize_merchant_defined_fields(merchant_defined_fields))

        if order_id:
            data["orderid"] = order_id

        return self._post_payment_api_request(data)

    def delete(self):
        data = {
            "customer_vault": "delete_customer",
            "security_key": self.security_key,
            "customer_vault_id": self.customer_id,
        }
        return self._post_payment_api_request(data)

    def get_info(self):
        if not self.customer_id:
            raise ValueError("Customer ID is required")
        data = {
            "report_type": "customer_vault",
            "security_key": self.security_key,
            "customer_vault_id": self.customer_id,
        }
        return self._post_query_api_request(data)
