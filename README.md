# NMI Gateway

## This fork has a LOT of major breaking changes.
The main goal was to allow the fork to work with other NMI-like,
gateways since NMI seems to offer their API as a white label service with different
URLs. Just need to use the correct API urls (maybe? It will probably work at the nmi
URLs, too). This fork makes the URLs requisite, but can set them on the Nmi class.

This fork makes a lot of other changes as well, such as doing some quick ruff formatting
and other tweaks to make it more compatible with our own specific usage (and not
necessarily of value to anyone else), including removing the "org" concept entirely
(not used by the API AFAIK or us, separate concern). It also removes the response
"wrapper" from responses, changes the arguments to most of the class inits, etc, etc.

No attempt was made to maintain typing, and minimal effort was put into updating
subscription/plans, since no intent to use it at this point.

The original examples below were quickly updated but are not guaranteed
(some seemed outdated in original).

## Original Heading:

This is a nmi handy package to interact with the nmi gateway endpoints, you can find the original documentation here:
https://secure.networkmerchants.com/gw/merchants/resources/integration/integration_portal.php#cv_variables

This package was build with the unique intention to make the integration with the gateway easy.

## Examples

### Init the gateway settings (new for fork).

This needs to be done before any API requests are made, or can
be passed in when creating each instance (ie, the secret_key is passed in the examples still).
```python
from nmigate import config_gateway
config_gateway(
    '<your security key>',
    'https://<whitelabel>.transactiongateway.com/api/transact.php',
    'https://<whitelabel>.transactiongateway.com/api/query.php'
)
```

### Customer Vault methods

#### Create customer vault

```python
from nmigate.customer import CustomerVault

payment_token = 'your test token here' # test token "00000000-000000-000000-000000000000"

customer_vault = CustomerVault()
    result = customer_vault.create(
        token,
        {
            "first_name": "1",
            "last_name": "1",
            "address1": "1",
            "city": "1",
            "state": "1",
            "zip": "1",
            "country": "1",
            "phone": "1",
            "email": "1"
        }
    })
```

#### Get billing info by transaction id

```python
from nmigate.payment import Transaction

secret_key = 'your secret key'
transaction_id = 'transaction id '

trans = Transaction(transaction_id)
result = trans.get_info()
```

### Plan

### Get all plans

```python
from nmigate.subscription import Plan

secret_key = 'your secret key'

plansObj = Plan(secret_key)
response = plansObj.get_all_plans()
plans = response['plan']

```

### Get plan

```python
from nmigate.subscription import Plan

secret_key = 'your secret key'
plan_id = 'your plan id'

plans = Plan(secret_key)
response = plans.get_plan(plan_id)

```

### Add plan using frequency configuration

```python
from nmigate.subscription import Plan

secret_key = 'your secret key'

plans = Plan(secret_key)
response = plans.add_plan_by_day_frequency({
    'plan_amount': '10.00',
    'plan_name': 'test',
    'plan_id': 'test',
    'day_frequency': '1',
    'plan_payments': '0'
})

```

### Edit day frequency plan

```python
from nmigate.subscription import Plan

secret_key = 'your secret key'

plans = Plan(secret_key)
response = plans.edit_plan_by_day_frequency({
    "recurring": "edit_plan",
    'plan_amount': '10.00',
    'plan_name': 'test',
    'plan_id': 'test',
    'day_frequency': '2',
    'plan_payments': '0'
})

```

### Add plan using month config

```python
from nmigate.subscription import Plan

secret_key = 'your secret key'

plans = Plan(secret_key)
response = plans.add_plan_by_month_config({
    'plan_amount': '10.00',
    'plan_name': 'test',
    'plan_id': 'test1',
    'month_frequency': '1',
    "day_of_month": '1',
    'plan_payments': '0'
})

```

### Edit plan using month config

```python
from nmigate.subscription import Plan

secret_key = 'your secret key'

plans = Plan(secret_key)
response = plans.edit_plan_by_month_config({
    'plan_amount': '10.00',
    'plan_name': 'test',
    'plan_id': 'test1',
    'month_frequency': '1',
    "day_of_month": '10',
    'plan_payments': '0'
})
```

### Subscription

#### Get Subscription

```python
from nmigate.customer import CustomerVault

secret_key = 'your secret key'
subscription_id='customer vault id'

subscriptions = Subscription(secret_key)
info = subscriptions.get_info(subscription_id)
print(result)
```

#### Subscription + sale, using plan_id and customer vault

If total_amount = 0 then its a simple subscription, if total_amount > 0 then its a subscription with sale

```python
from nmigate.customer import CustomerVault

secret_key = 'your secret key'
customer_vault_id='customer vault id'

subscriptions = Subscription(secret_key)
result = subscriptions.custom_sale_using_vault(plan_id = customer_vault_id, customer_vault_id=customer_vault_id, create_customer_vault=False)
print(result)
```

#### Custome Subscription + sale, using vault number and month frequency configuration

```python
from nmigate.subscription import Subscription

secret_key = 'your secret key'

subscriptions = Subscription(secret_key)
result = subscriptions.custom_sale_using_vault_month_frequency(request_sub = {
    "user_id": "1",
    "total_amount": "11",
    "custom_subscription_info": {
        "plan_payments": "13",
        "plan_amount": "12",
        "month_frequency": "1",
        "day_of_month": "1"
    }
})
print(result)

```

#### Custome Subscription + sale, using vault number and day frequency configuration

```python
from nmigate.subscription import Subscription

secret_key = 'your secret key'

subscriptions = Subscription(secret_key)
result = subscriptions.custom_with_sale_and_vault_day_frequency(request_sub = {
    "user_id": "1",
    "total_amount": "14",
    "custom_subscription_info": {
        "plan_payments": "15",
        "plan_amount": "6",
        "day_frequency": "1"
    }
})
print(result)
```

#### Delete subscription

```python
from nmigate.subscription import Subscription

secret_key = 'your secret key'
subscription_id = 'your subscription_id'

subscriptions = Subscription(secret_key)
info = subscriptions.delete_subscription(subscription_id)
```

#### Pause/resume Subscription

```python
from nmigate.subscription import Subscription

secret_key = 'your secret key'
subscription_id = 'your subscription_id'
pause=True # True to pause, False to unpause

transactions = Subscription(secret_key)
result = transactions.pause_subscription(subscription_id, pause)
```


#### Tests (new for fork):
To run tests in a cloned directory, you will need to set an appropriate PYTHONPATH env
pointed at the "src" dir for the imports to work:
```bash
PYTHONPATH="${PYTHONPATH}:/path/to/cloned/nmigate/src"
```
Note that the project is "nmi-gate" so make sure the above is correct if used that for
the dir.
Warning: tests run against the live API. They are set to use the "demo" key now but
still don't pass for various reasons, some seem outdated. Left for now.
