from transaccion_completa_mall_deferred import bp
from flask import render_template, request
from transbank.webpay.transaccion_completa.mall_transaction import MallTransaction
from datetime import datetime as dt
from datetime import timedelta
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.options import WebpayOptions

@bp.route('create', methods=['GET'])
def show_create():
    child_codes = [IntegrationCommerceCodes.TRANSACCION_COMPLETA_MALL_DEFERRED_CHILD1, IntegrationCommerceCodes.TRANSACCION_COMPLETA_MALL_DEFERRED_CHILD2]
    return render_template('/transaccion_completa_mall/deferred/create.html', dt=dt, timedelta=timedelta,
                           child_commerce_codes = child_codes)


@bp.route('create', methods=['POST'])
def send_create():
    print("Create method POST")
    buy_order = request.form.get('buy_order')
    session_id = request.form.get('session_id')
    card_number = request.form.get('card_number')
    card_expiration_date = request.form.get('card_expiration_date')

    details = [
        {
            'commerce_code': request.form.get('child_commerce_1'),
            'buy_order': request.form.get('buy_order_1'),
            'amount': request.form.get('amount_1')
        },
        {
            'commerce_code': request.form.get('child_commerce_2'),
            'buy_order': request.form.get('buy_order_2'),
            'amount': request.form.get('amount_2')
        }
    ]
    tx = MallTransaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    resp = tx.create(
        buy_order=buy_order,
        session_id=session_id,
        card_number=card_number, card_expiration_date=card_expiration_date, details=details, cvv=123
    )

    return render_template('transaccion_completa_mall/deferred/created.html', resp=resp, req=request.form, dt=dt,
                           details=details)


@bp.route('installments', methods=['POST'])
def installments():
    req = request.form
    token = request.form.get('token')
    details = [
        {
            'commerce_code': request.form.get('details[0][commerce_code]'),
            'buy_order': request.form.get('details[0][buy_order]'),
            'amount': request.form.get('details[0][amount]'),
            'installments_number': request.form.get('details[0][installments_number]')
        },
        {
            'commerce_code': request.form.get('details[1][commerce_code]'),
            'buy_order': request.form.get('details[1][buy_order]'),
            'amount': request.form.get('details[1][amount]'),
            'installments_number': request.form.get('details[1][installments_number]')
        }
    ]
    tx = MallTransaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    resp = tx.installments(token=token, details=details)
    return render_template('/transaccion_completa_mall/deferred/installments.html', req=req, resp=resp, details=details)


@bp.route('commit', methods=['POST'])
def commit():
    req = request.form
    token = request.form.get('token')
    details = [
        {
            'commerce_code': request.form.get('details[0][commerce_code]'),
            'buy_order': request.form.get('details[0][buy_order]'),
            'id_query_installments': request.form.get('details[0][id_query_installments]'),
            'deferred_period_index': request.form.get('details[0][deferred_period_index]'),
            'grace_period': request.form.get('details[0][grace_period]')

        },
        {
            'commerce_code': request.form.get('details[1][commerce_code]'),
            'buy_order': request.form.get('details[1][buy_order]'),
            'id_query_installments': request.form.get('details[1][id_query_installments]'),
            'deferred_period_index': request.form.get('details[1][deferred_period_index]'),
            'grace_period': request.form.get('details[1][grace_period]')
        }
    ]
    tx = MallTransaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    resp = tx.commit(token=token,
                              details=details)
    return render_template('/transaccion_completa_mall/deferred/transaction_committed.html', req=req, resp=resp)


@bp.route('status', methods=['POST'])
def status():
    token = request.form.get("token")
    tx = MallTransaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.status(token=token)
    request_data = {
        "token": token
    }
    return render_template('/transaccion_completa_mall/deferred/status.html', request=request_data, response=response)


@bp.route('refund', methods=['POST'])
def refund():
    req = request.form
    token = req.get('token')
    amount = req.get('amount')
    print("TOKEN \n")
    print(token)
    child_buy_order = req.get('child_buy_order')
    child_commerce_code = req.get('child_commerce_code')
    tx = MallTransaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    resp = tx.refund(token=token, amount=amount, child_commerce_code=child_commerce_code,
                              child_buy_order=child_buy_order)

    return render_template('/transaccion_completa_mall/deferred/transaction_refunded.html', req=req, resp=resp)

@bp.route('increase_amount', methods=['POST'])
def increase_amount():
    token = request.form.get("token")
    buy_order = request.form.get("buy_order")
    authorization_code = request.form.get("authorization_code")
    amount = request.form.get("amount")
    commerce_code = request.form.get("commerce_code")

    tx = MallTransaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.increaseAmount(token, buy_order, authorization_code, amount, commerce_code)
    request_data = {
        "token": token,
        "buy_order": buy_order,
        "authorization_code": authorization_code,
        "amount": amount,
        "commerce_code": commerce_code
    }
    return render_template('/transaccion_completa_mall/deferred/increase_amount.html', request=request_data, response=response)

@bp.route('reverse_amount', methods=['POST'])
def reverse_amount():
    token = request.form.get("token")
    buy_order = request.form.get("buy_order")
    authorization_code = request.form.get("authorization_code")
    amount = request.form.get("amount")
    commerce_code = request.form.get("commerce_code")

    tx = MallTransaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.reversePreAuthorizedAmount(token, buy_order, authorization_code, amount, commerce_code)
    request_data = {
        "token": token,
        "buy_order": buy_order,
        "authorization_code": authorization_code,
        "amount": amount,
        "commerce_code": commerce_code
    }
    return render_template('/transaccion_completa_mall/deferred/reverse_amount.html', request=request_data, response=response)

@bp.route('increase_date', methods=['POST'])
def increase_date():
    token = request.form.get("token")
    buy_order = request.form.get("buy_order")
    authorization_code = request.form.get("authorization_code")
    commerce_code = request.form.get("commerce_code")
    tx = MallTransaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.increaseAuthorizationDate(token, buy_order, authorization_code, commerce_code)
    request_data = {
        "token": token,
        "buy_order": buy_order,
        "authorization_code": authorization_code,
        "commerce_code": commerce_code
    }
    return render_template('/transaccion_completa_mall/deferred/increase_date.html', request=request_data, response=response)

@bp.route('history', methods=['POST'])
def history():
    token = request.form.get("token")
    buy_order = request.form.get("buy_order")
    commerce_code = request.form.get("commerce_code")
    tx = MallTransaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.deferredCaptureHistory(token, buy_order,commerce_code)
    request_data = {
        "token": token,
        "buy_order": buy_order,
        "commerce_code": commerce_code
    }
    return render_template('/transaccion_completa_mall/deferred/history.html', request=request_data, response=response)

@bp.route('capture', methods=['POST'])
def capture():
    token = request.form.get("token")
    buy_order = request.form.get("buy_order")
    authorization_code = request.form.get("authorization_code")
    capture_amount = request.form.get("capture_amount")
    commerce_code = request.form.get("commerce_code")
    tx = MallTransaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_MALL_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.capture(token, commerce_code, buy_order, authorization_code, capture_amount)
    request_data = {
        "token": token,
        "buy_order": buy_order,
        "commerce_code": commerce_code
    }
    return render_template('/transaccion_completa_mall/deferred/capture.html', request=request_data, response=response)