# From:
# https://docs.nmi.dev/reference/response-codes


# Constants for some important ones
TRANSACTION_DUPLICATE = 430
TRANSACTION_RATE_LIMITED = 301
TRANSACTION_APPROVED = 100

Transaction = (
    (TRANSACTION_APPROVED, "Transaction was approved"),
    (200, "Transaction was declined by processor"),
    (201, "Do not honor"),
    (202, "Insufficient funds"),
    (203, "Over limit"),
    (204, "Transaction not allowed"),
    (220, "Incorrect payment information"),
    (221, "No such card issuer"),
    (222, "No card number on file with issuer"),
    (223, "Expired card"),
    (224, "Invalid expiration date"),
    (225, "Invalid card security code"),
    (226, "Invalid PIN"),
    (240, "Call issuer for further information"),
    (250, "Pick up card"),
    (251, "Lost card"),
    (252, "Stolen card"),
    (253, "Fraudulent card"),
    (260, "Declined with further instructions available (See response text)"),
    (261, "Declined-Stop all recurring payments"),
    (262, "Declined-Stop this recurring program"),
    (263, "Declined-Update cardholder data available"),
    (264, "Declined-Retry in a few days"),
    (300, "Transaction was rejected by gateway"),
    (TRANSACTION_RATE_LIMITED, "Too many requests (API)"),
    (400, "Transaction error returned by processor"),
    (410, "Invalid merchant configuration"),
    (411, "Merchant account is inactive"),
    (420, "Communication error"),
    (421, "Communication error with issuer"),
    (TRANSACTION_DUPLICATE, "Duplicate transaction at processor"),
    (440, "Processor format error"),
    (441, "Invalid transaction information"),
    (460, "Processor feature not available"),
    (461, "Unsupported card type"),
)

# These should generally be ones that can be retried without changing anything
# after an appropriate delay (ie, at least a day for most).
# Other declines may also be retryable if auto-card update happens, etc.
retryable_failure_response_codes = {
    202,
    203,
    263,
    264,
    300,
    TRANSACTION_RATE_LIMITED,
    400,
    410,
    411,
    420,
    421,
    TRANSACTION_DUPLICATE,
    440,
    441,
    460,
}

# Hard declines
non_retryable_failure_response_codes = (
    set(dict(Transaction).keys())
    - retryable_failure_response_codes
    - {TRANSACTION_APPROVED}
)

# These are issues with the gateway or processor.
# Note: use response = '3' as authority on error status, not these.
processing_error_response_codes = (300, 400, 410, 411, 420, 421, 440, 441, 460)

Avs = (
    ("X", "Exact match, 9-character numeric ZIP"),
    ("Y", "Exact match, 5-character numeric ZIP"),
    ("D", "Exact match, 5-character numeric ZIP"),
    ("M", "Exact match, 5-character numeric ZIP"),
    ("2", "Exact match, 5-character numeric ZIP, customer name"),
    ("6", "Exact match, 5-character numeric ZIP, customer name"),
    ("A", "Address match only"),
    ("B", "Address match only"),
    ("3", "Address, customer name match only"),
    ("7", "Address, customer name match only"),
    ("W", "9-character numeric ZIP match only"),
    ("Z", "5-character ZIP match only"),
    ("P", "5-character ZIP match only"),
    ("L", "5-character ZIP match only"),
    ("1", "5-character ZIP, customer name match only"),
    ("5", "5-character ZIP, customer name match only"),
    ("N", "No address or ZIP match only"),
    ("C", "No address or ZIP match only"),
    ("4", "No address or ZIP or customer name match only"),
    ("8", "No address or ZIP or customer name match only"),
    ("U", "Address unavailable"),
    ("G", "Non-U.S. issuer does not participate"),
    ("I", "Non-U.S. issuer does not participate"),
    ("R", "Issuer system unavailable"),
    ("E", "Not a mail/phone order"),
    ("S", "Service not supported"),
    ("0", "AVS not available"),
    ("O", "AVS not available"),
    ("B", "AVS not available"),
)


Cvv = (
    ("M", "CVV2/CVC2 match"),
    ("N", "CVV2/CVC2 no match"),
    ("P", "Not processed"),
    ("S", "Merchant has indicated that CVV2/CVC2 is not present on card"),
    ("U", "Issuer is not certified and/or has not provided Visa encryption keys"),
)

Response = (
    (0, ""),
    (1, "approved"),
    (2, "declined"),
    (3, "error"),
)
