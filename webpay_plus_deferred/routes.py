import random
from urllib import response

from flask import render_template, request
from transbank.error.transbank_error import TransbankError
from webpay_plus_deferred import bp

from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.options import WebpayOptions
from transbank.webpay.webpay_plus.transaction import Transaction

@bp.route("create", methods=["GET"])
def webpay_plus_deferred_create():
    print("Webpay Plus DeferredTransaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = random.randrange(10000, 1000000)
    return_url = request.url_root + 'webpay-plus-deferred/commit'

    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    tx = (Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
    response = tx.create(buy_order, session_id, amount, return_url)

    print(response)
    return render_template('webpay/plus_deferred/create.html', request=create_request, response=response)

@bp.route("commit", methods=["GET"])
def webpay_plus_deferred_commit():
    token = request.args.get("token_ws")
    print("commit for token_ws: {}".format(token))
    tx = (Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
    response = tx.commit(token)
    print("response: {}".format(response))

    return render_template('webpay/plus_deferred/commit.html', token=token, response=response)

@bp.route("commit", methods=["POST"])
def webpay_plus_deferred_commit_error():
    token = request.form.get("token_ws")
    print("commit for token_ws: {}".format(token))
    tx = (Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
    response = tx.commit(token)
    print("response: {}".format(response))

    return render_template('webpay/plus_deferred/commit.html', token=token, response=response)    

@bp.route("status", methods=["POST"])
def webpay_plus_deferred_status():
    token = request.form.get("token_ws")
    print("commit for token_ws: {}".format(token))
    tx = (Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
    response = tx.status(token)
    print("response: {}".format(response))

    return render_template('webpay/plus_deferred/status.html', token=token, response=response)

@bp.route('status-form', methods=['GET'])
def show_create():
    return render_template('webpay/plus_deferred/status-form.html')

@bp.route("capture", methods=["POST"])
def webpay_plus_deferred_capture():
    token = request.form.get("token_ws")
    buy_order = request.form.get("buy_order")
    authorization_code = request.form.get("authorization_code")
    capture_amount = request.form.get("capture_amount")
    print("capture for token_ws: {} , buy_order: {}, authorization_code: {}, capture_amount: {}".format(token,
                                                                buy_order, authorization_code, capture_amount))
    tx = (Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))                                                            
    response = tx.capture(token = token, buy_order = buy_order, authorization_code = authorization_code,
                                            capture_amount = capture_amount)
    print("response: {}".format(response))

    return render_template('webpay/plus_deferred/capture.html', token=token, response=response)

@bp.route("increase_amount", methods=["POST"])
def webpay_plus_deferred_increase_amount():
    token = request.form.get("token_ws")
    buy_order = request.form.get("buy_order")
    authorization_code = request.form.get("authorization_code")
    amount = 10000
    print("increase amount for token_ws: {} , buy_order: {}, authorization_code: {}, amount: {}".format(token,
                                                                buy_order, authorization_code, amount))
    tx = (Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
    response = tx.increaseAmount(token, buy_order, authorization_code, amount, IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED)
    print("response: {}".format(response))
    request_data = {
        "token": token,
        "buy_order": buy_order,
        "authorization_code": authorization_code,
        "amount": amount
    }

    return render_template('webpay/plus_deferred/increase_amount.html', request=request_data, response=response, action = "Incrementar monto", step = "Increase Amount")

@bp.route("reverse_amount", methods=["POST"])
def webpay_plus_deferred_reverse_amount():
    token = request.form.get("token_ws")
    buy_order = request.form.get("buy_order")
    authorization_code = request.form.get("authorization_code")
    amount = 10000
    print("increase amount for token_ws: {} , buy_order: {}, authorization_code: {}, amount: {}".format(token,
                                                                buy_order, authorization_code, amount))
    tx = (Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
    response = tx.reversePreAuthorizedAmount(token, buy_order, authorization_code, amount, IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED)
    print("response: {}".format(response))
    request_data = {
        "token": token,
        "buy_order": buy_order,
        "authorization_code": authorization_code,
        "amount": amount
    }

    return render_template('webpay/plus_deferred/reverse_amount.html', request=request_data, response=response, action = "Reversar monto pre-autorizado", step = "Reverse Pre-Authorized Amount")


@bp.route("increase_date", methods=["POST"])
def webpay_plus_deferred_increase_date():
    token = request.form.get("token_ws")
    buy_order = request.form.get("buy_order")
    authorization_code = request.form.get("authorization_code")
    print("increase auth date for token_ws: {} , buy_order: {}, authorization_code: {}".format(token,
                                                                buy_order, authorization_code))
    tx = (Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
    response = tx.increaseAuthorizationDate(token, buy_order, authorization_code, IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED)
    print("response: {}".format(response))
    request_data = {
        "token": token,
        "buy_order": buy_order,
        "authorization_code": authorization_code,
    }

    return render_template('webpay/plus_deferred/increase_date.html', request=request_data, response=response, action = "Incrementar fecha de autorizacion", step = "Increase Authorization Date")

@bp.route("history", methods = ["POST"])
def webpay_plus_deferred_history():
    token = request.form.get("token_ws")
    print("increase history for token_ws: {}".format(token))
    tx = (Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
    response = tx.deferredCaptureHistory(token)
    print("response: {}".format(response))
    request_data = {
        "token": token,
    }
    return render_template('webpay/plus_deferred/history.html', request=request_data, response=response, action = "Historial de la transccion", step = "Transaction history")

@bp.route("refund", methods=["POST"])
def webpay_plus_refund():
    token = request.form.get("token_ws")
    amount = request.form.get("amount")
    print("refund for token_ws: {} by amount: {}".format(token, amount))
    try:
        tx = (Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)))
        response = tx.refund(token, amount)
        print("response: {}".format(response))
        return render_template("webpay/plus_deferred/refund.html", token=token, amount=amount, response=response)
    except TransbankError as e:
        print(e.message)

@bp.route("refund-form", methods=["GET"])
def webpay_plus_refund_form():
    
    return render_template("webpay/plus_deferred/refund-form.html")
