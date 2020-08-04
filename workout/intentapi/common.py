from flask_restful import fields

account_fields = {
    'account_number': fields.Integer,
    'balance': fields.Float,
    'customer_id': fields.Integer,
    'uri': fields.Url('intent.get_customer_info')
}

transaction_fields = {
    'amount': fields.Float,
    'account_id': fields.Integer,
    'time': fields.DateTime(dt_format='iso8601'),
}

account_fields_with_transactions = {
    'account_number': fields.Integer,
    'balance': fields.Float,
    'customer_id': fields.Integer,
    'transactions': fields.List(fields.Nested(transaction_fields))
}

customer_info_fields = {
    'name': fields.String,
    'surname': fields.String,
    'accounts': fields.List(fields.Nested(account_fields_with_transactions))
}
