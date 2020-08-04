from typing import Optional
from uuid import uuid4

from bank_api import models


def generate_random_account_number() -> str:
    """Generate a pseudo random number from uuid4, trucated to 20 digits"""
    return str(uuid4().int)[0:20]


def create_account(customer: models.Customer, balance: Optional[float] = 0) -> models.Account:
    account_number = generate_random_account_number()
    if models.Account.query.filter_by(account_number=account_number).first() is not None:
        raise ValueError("An account with that number already exists")
    data = {
        'account_number': account_number,
        'balance': balance,
        'customer_id': customer.id
    }
    return models.Account().import_data(data)
