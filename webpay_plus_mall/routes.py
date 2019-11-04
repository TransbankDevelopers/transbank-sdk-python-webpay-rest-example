import random

from flask import render_template, request
from transbank.error.transbank_error import TransbankError
from datetime import datetime as dt
from datetime import timedelta
from webpay_plus_mall import bp
from transbank.transaccion_completa_mall import child_commerce_codes
from transbank.webpay.webpay_plus.mall_transaction import MallTransaction
from transbank.webpay.webpay_plus.request import MallTransactionCreateDetails


@bp.route('create', methods=['GET'])
def show_create():
    print('123123123123131231231231312')
    return render_template('/webpay/plus_mall/create.html', dt=dt, timedelta=timedelta,
                           child_commerce_codes=child_commerce_codes)

@bp.route('create', methods=['POST'])
def send_create():
    buy_order = request.form.get('buy_order')
    session_id = request.form.get('session_id')
    return_url = request.url_root + 'webpay-plus-mall/commit'
    
    commerce_code_child_1 = request.form.get('details[0][commerce_code]')
    buy_order_child_1= request.form.get('details[0][buy_order]')
    amount_child_1 = request.form.get('details[0][amount]')

    commerce_code_child_2 = request.form.get('details[1][commerce_code]')
    buy_order_child_2 = request.form.get('details[1][buy_order]')
    amount_child_2 = request.form.get('details[1][amount]')

    details = MallTransactionCreateDetails(amount_child_1, commerce_code_child_1, buy_order_child_1) \
            .add(amount_child_2, commerce_code_child_2, buy_order_child_2)

    resp = MallTransaction.create(
        buy_order=buy_order,
        session_id=session_id,
        return_url=return_url,
        details = details,
    )
    
    print (resp)
    return render_template('/webpay/plus_mall/created.html', details=details,
                           resp=resp)

@bp.route("commit", methods=["POST"])
def webpay_plus_commit():
    token = request.form.get("token_ws")
    print("commit for token_ws: {}".format(token))

    response = MallTransaction.commit(token=token)
    print("response: {}".format(response))

    return render_template('/webpay/plus_mall/commit.html', token=token, response=response)