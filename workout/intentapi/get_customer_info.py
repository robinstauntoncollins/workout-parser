from flask import current_app, request
from flask_restful import marshal

from bank_api.errors import make_error
from bank_api.models import Customer

from . import intent_api_bp
from .common import customer_info_fields


@intent_api_bp.route('/getCustomerInfo', methods=['GET'])
def get_customer_info():
    current_app.logger.info(f"Request parameters: {request.args}")
    current_app.logger.info(f"Request data: {request.json}")
    if not request.json and not request.args:
        return make_error(400, "Missing required parameters")

    c_id = request.args.get('customerID') or request.json.get('customerID')
    if not c_id or type(c_id) != str:
        return make_error(404, f"Missing 'customerID'. Expected 'str' got {type(c_id)}")

    # page = request.args.get('page', 1, type=int)

    c = Customer.query.get_or_404(c_id)
    return {'customer': marshal(c, customer_info_fields)}
