import random

from flask import render_template, request
from transbank.error.transbank_error import TransbankError
from datetime import datetime as dt
from datetime import timedelta
from webpay_plus_mall_deferred import bp
from transbank.webpay.webpay_plus.mall_transaction import MallTransaction
from transbank.webpay.webpay_plus.request import MallTransactionCreateDetails

from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.options import WebpayOptions


@bp.route('create', methods=['GET'])
def show_create():
    return render_template('/webpay/plus_mall_deferred/create.html', dt=dt, timedelta=timedelta,
                           child_commerce_codes=IntegrationCommerceCodes.WEBPAY_PLUS_MALL_DEFERRED_CHILD_COMMERCE_CODES)

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

    tx = (MallTransaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
    response = tx.create(
        buy_order=buy_order,
        session_id=session_id,
        return_url=return_url,
        details = details,
    )
    
    print (response)
    return render_template('/webpay/plus_mall_deferred/created.html', details=details,
                           response=response)

@bp.route("commit", methods=["GET"])
def webpay_plus_commit():
    token = request.args.get("token_ws")
    print("commit for token_ws: {}".format(token))

    tx = (MallTransaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
    response = tx.commit(token=token)
    print("response: {}".format(response))

    return render_template('/webpay/plus_mall_deferred/commit.html', token=token, response=response)

@bp.route("commit", methods=["POST"])
def webpay_plus_commit_error():
    token = request.form.get("token_ws")
    print("commit for token_ws: {}".format(token))

    tx = (MallTransaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
    response = tx.commit(token=token)
    print("response: {}".format(response))

    return render_template('/webpay/plus_mall_deferred/commit.html', token=token, response=response)


@bp.route("capture", methods=["POST"])
def webpay_plus__mall_capture():
    token = request.form.get("token_ws")
    amount = request.form.get("amount")
    buy_order = request.form.get("buy_order")
    commerce_code = request.form.get("commerce_code")
    authorization_code = request.form.get("authorization_code")
    print("Capture for token_ws: {} amount: {} buy_order: {} commerce_code: {} authorization_code: {} ".format(
        token, amount,buy_order, commerce_code,authorization_code))

    tx = MallTransaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.capture(token=token, capture_amount=amount, child_commerce_code=commerce_code,
                            buy_order=buy_order, authorization_code=authorization_code)

    return render_template("webpay/plus_mall_deferred/capture.html", token=token, amount=amount, response=response)

@bp.route("status", methods=["POST"])
def webpay_plus_deferred_status():
    token = request.form.get("token_ws")
    commerce_code = request.form.get("commerce_code")
    print("commit for token_ws: {}, token_ws: {}".format(token, commerce_code))
    tx = (MallTransaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
    response = tx.status(token=token)
    print("response: {}".format(response))

    return render_template('webpay/plus_mall_deferred/status.html', token=token, response=response)

@bp.route("status-form", methods=["GET"])
def patpass_webpay_status_form():
    return render_template("webpay/plus_mall_deferred/status-form.html")

@bp.route('refund-form', methods=['GET'])
def refund_form():
    return render_template('/webpay/plus_mall_deferred/refund-form.html')

@bp.route("refund", methods=["POST"])
def webpay_plus_refund():
    token = request.form.get("token_ws")
    amount = request.form.get("amount")
    commerce_code = request.form.get("commerce_code")
    buy_order = request.form.get("buy_order")
    print("Refund for token_ws: {} by amount: {}".format(token, amount))
    try:
        tx = (MallTransaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
        response = tx.refund(token, buy_order, commerce_code, amount)
        print("response: {}".format(response))
        return render_template("webpay/plus_mall_deferred/refund.html", token=token, amount=amount, response=response)
    except TransbankError as e:
        print(e.message)