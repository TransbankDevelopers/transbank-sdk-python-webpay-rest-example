import random

from flask import render_template, request
from transbank.error.transbank_error import TransbankError
from datetime import datetime as dt
from datetime import timedelta
from webpay_plus_mall_deferred import bp
from transbank.webpay.webpay_plus import mall_deferred_default_child_commerce_codes
from transbank.webpay.webpay_plus.mall_deferred_transaction import MallDeferredTransaction
from transbank.webpay.webpay_plus.request import MallTransactionCreateDetails


@bp.route('create', methods=['GET'])
def show_create():
    return render_template('/webpay/plus_mall_deferred/create.html', dt=dt, timedelta=timedelta,
                           child_commerce_codes=mall_deferred_default_child_commerce_codes)

@bp.route('create', methods=['POST'])
def send_create():
    buy_order = request.form.get('buy_order')
    session_id = request.form.get('session_id')
    return_url = request.url_root + 'webpay-plus-mall-deferred/commit'
    
    commerce_code_child_1 = request.form.get('details[0][commerce_code]')
    buy_order_child_1= request.form.get('details[0][buy_order]')
    amount_child_1 = request.form.get('details[0][amount]')

    commerce_code_child_2 = request.form.get('details[1][commerce_code]')
    buy_order_child_2 = request.form.get('details[1][buy_order]')
    amount_child_2 = request.form.get('details[1][amount]')

    details = MallTransactionCreateDetails(amount_child_1, commerce_code_child_1, buy_order_child_1) \
            .add(amount_child_2, commerce_code_child_2, buy_order_child_2)

    response = MallDeferredTransaction.create(
        buy_order=buy_order,
        session_id=session_id,
        return_url=return_url,
        details = details,
    )
    
    print (response)
    return render_template('/webpay/plus_mall_deferred/created.html', details=details,
                           response=response)


@bp.route("commit", methods=["POST"])
def webpay_plus_commit():
    token = request.form.get("token_ws")
    print("commit for token_ws: {}".format(token))

    response = MallDeferredTransaction.commit(token=token)
    print("response: {}".format(response))

    return render_template('/webpay/plus_mall_deferred/commit.html', token=token, response=response)

@bp.route('refund-form', methods=['GET'])
def refund_form():
    return render_template('/webpay/plus_mall_deferred/refund-form.html')

@bp.route("capture", methods=["POST"])
def webpay_plus__mall_refund():
    token = request.form.get("token_ws")
    amount = request.form.get("amount")
    buy_order = request.form.get("buy_order")
    commerce_code = request.form.get("commerce_code")
    authorization_code = request.form.get("authorization_code")
    response = '123'
    print("capture for token_ws: {} amount: {} buy_order: {} commerce_code: {} authorization_code: {} ".format(
        token, amount,buy_order, commerce_code,authorization_code))

    response = MallDeferredTransaction.capture(token=token, capture_amount=amount, commerce_code=commerce_code,
                            buy_order=buy_order, authorization_code=authorization_code)

    return render_template("webpay/plus_mall_deferred/capture.html", token=token, amount=amount, response=response)


# @bp.route("status-form", methods=["GET"])
# def patpass_webpay_status_form():
#     return render_template("webpay/plus_mall_deferred/status-form.html")


# @bp.route("status", methods=["POST"])
# def patpass_webpay_status():
#     token = request.form.get("token_ws")
#     try:
#         response = MallDeferredTransaction.status(token)
#         return render_template("webpay/plus_mall_deferred/status.html", token=token, response=response)
#     except TransbankError as e:
#         print(e.message)