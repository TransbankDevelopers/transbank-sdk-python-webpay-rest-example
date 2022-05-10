import random

from flask import render_template, request
from transbank.error.transbank_error import TransbankError
from datetime import datetime as dt
from datetime import timedelta
from webpay_plus_mall import bp
from transbank.webpay.webpay_plus.mall_transaction import MallTransaction
from transbank.webpay.webpay_plus.request import MallTransactionCreateDetails
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes

@bp.route('create', methods=['GET'])
def show_create():
    return render_template('/webpay/plus_mall/create.html', dt=dt, timedelta=timedelta,
                           child_commerce_codes=IntegrationCommerceCodes.WEBPAY_PLUS_MALL_CHILD_COMMERCE_CODES)

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

    response = (MallTransaction()).create(
        buy_order=buy_order,
        session_id=session_id,
        return_url=return_url,
        details = details,
    )
    
    print (response)
    return render_template('/webpay/plus_mall/created.html', details=details,
                           response=response)

@bp.route("commit", methods=["GET"])
def webpay_plus_commit():
    token = request.args.get("token_ws")
    print("commit for token_ws: {}".format(token))

    response = (MallTransaction()).commit(token=token)
    print("response: {}".format(response))

    return render_template('/webpay/plus_mall/commit.html', token=token, response=response)

@bp.route("commit", methods=["POST"])
def webpay_plus_commit_error():
    token = request.form.get("token_ws")
    print("commit for token_ws: {}".format(token))

    response = (MallTransaction()).commit(token=token)
    print("response: {}".format(response))

    return render_template('/webpay/plus_mall/commit.html', token=token, response=response)    

@bp.route('refund-form', methods=['GET'])
def refund_form():
    return render_template('/webpay/plus_mall/refund-form.html')

@bp.route("refund", methods=["POST"])
def webpay_plus__mall_refund():
    token = request.form.get("token_ws")
    amount = request.form.get("amount")
    buy_order = request.form.get("buy_order")
    commerce_code = request.form.get("commerce_code")
    print("refund for token_ws: {} by amount: {} buy_order: {} commerce_code: {}".format(token, amount,buy_order, commerce_code))

    try:
        response = (MallTransaction()).refund(token=token, amount=amount, child_commerce_code=commerce_code,
                              child_buy_order=buy_order)
        print("response: {}".format(response))

        return render_template("webpay/plus_mall/refund.html", token=token, amount=amount, response=response)
    except TransbankError as e:
        print(e.message)

@bp.route("status-form", methods=["GET"])
def patpass_webpay_status_form():
    return render_template("webpay/plus_mall/status-form.html")


@bp.route("status", methods=["POST"])
def patpass_webpay_status():
    token = request.form.get("token_ws")
    try:
        response = (MallTransaction()).status(token)
        return render_template("webpay/plus_mall/status.html", token=token, response=response)
    except TransbankError as e:
        print(e.message)