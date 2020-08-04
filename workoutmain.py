#!/usr/bin/env python3
import os
import click
from workout import create_app, db, models

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


# @app.shell_context_processor
# def make_shell_context():
#     return {
#         'db': db,
#         'Account': models.Account,
#         'Customer': models.Customer,
#         'Transaction': models.Transaction}


# @app.cli.command('createdb')
# @click.option('--test-data', type=bool, default=True, help="Initializes database with pre-loaded data")
# def createdb(test_data):
#     db.drop_all()
#     db.create_all()
#     if test_data:
#         customer_data = [
#             {'name': "Robin", 'surname': "Staunton-Collins"},
#             {'name': "Matin", 'surname': "Abbasi"},
#             {'name': "Rodrigo", 'surname': "Hammerly"},
#             {'name': "Monty", 'surname': "Python"}
#         ]
#         account_data = [
#             {'customer_id': 1, 'balance': 50, 'account_number': utils.generate_random_account_number()},
#             {'customer_id': 1, 'balance': 40, 'account_number': utils.generate_random_account_number()},
#             {'customer_id': 2, 'balance': 450, 'account_number': utils.generate_random_account_number()},
#         ]

#         transaction_data = [
#             {'account_id': 1, 'amount': 50},
#             {'account_id': 2, 'amount': 40},
#             {'account_id': 3, 'amount': 450},
#         ]

#         customers = [models.Customer().import_data(c) for c in customer_data]
#         db.session.add_all(customers)

#         accounts = [models.Account().import_data(a) for a in account_data]
#         db.session.add_all(accounts)

#         transactions = [models.Transaction().import_data(t) for t in transaction_data]
#         db.session.add_all(transactions)

#         db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
