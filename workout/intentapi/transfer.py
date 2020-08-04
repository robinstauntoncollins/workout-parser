from flask import request, current_app

from bank_api.models import Account, Transaction, db
from bank_api.errors import make_error

from . import intent_api_bp


@intent_api_bp.route('/transfer', methods=['POST'])
def transfer():
    if not request.json:
        return make_error(400, "Missing required parameters")

    # Parse Input
    json = request.get_json()
    if 'senderAccount' not in json or type(json['senderAccount']) != str:
        current_app.logger.info(f"'senderAccount' not found in {json}")
        return make_error(404, f"Missing 'senderAccount'. Expected 'str' got {type(json.get('senderAccount'))}")
    if 'receiverAccount' not in json or type(json['receiverAccount']) != str:
        current_app.logger.info(f"'receiverAccount' not found in {json}")
        return make_error(404, f"Missing 'receiverAccount'. Expected 'str' got {type(json.get('receiverAccount'))}")
    if 'amount' not in json or type(json['amount']) != str:
        current_app.logger.info(f"'amount' not found in {json} or type of 'amount' != str: {type(json.get('amount'))}")
        return make_error(404, f"Missing 'amount'. Expected 'str' got {type(json.get('amount'))}")

    s_an = str(json['senderAccount'])
    r_an = str(json['receiverAccount'])
    amount = float(json['amount'])

    # Retrieve Resources
    s = Account.query.filter_by(account_number=s_an).first()
    if not s:
        return make_error(404, f"Couldn't find account: {s_an}")
    r = Account.query.filter_by(account_number=r_an).first()
    if not r:
        return make_error(404, f"Couldn't find account: {r_an}")

    # Check sufficient balance
    if s.balance - amount < 0:
        return make_error(403, "Insufficient balance")

    # Generate transactions
    s_transaction = Transaction(account_id=s.id, amount=-amount)
    db.session.add(s_transaction)

    r_transaction = Transaction(account_id=r.id, amount=amount)
    db.session.add(r_transaction)

    # Perform operations
    s.balance -= amount
    db.session.add(s)

    r.balance += amount
    db.session.add(r)

    # Commit results
    db.session.commit()

    return {'result': True}
