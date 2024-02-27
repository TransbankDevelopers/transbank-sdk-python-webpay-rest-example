from urllib import response
from transaccion_completa_deferred import bp
from flask import render_template, request
from transbank.webpay.transaccion_completa.transaction import Transaction
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.options import WebpayOptions
from datetime import datetime as dt
from datetime import timedelta

@bp.route('create', methods=['GET'])
def show_create():
    return render_template('transaccion_completa/deferred/create.html', dt=dt, timedelta=timedelta)

@bp.route('create', methods=['POST'])
def create():
    print("Full transaction deferred create")
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    buy_order = request.form.get('buy_order')
    session_id = request.form.get('session_id')
    amount = request.form.get('amount')
    card_number = request.form.get('card_number')
    cvv = request.form.get('cvv')
    card_expiration_date = request.form.get('card_expiration_date')
    response = tx.create(buy_order, session_id, amount, cvv, card_number, card_expiration_date)

    request_data = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "card_number": card_number,
        "cvv": cvv,
        "card_expiration_date": card_expiration_date
    }
    return render_template('transaccion_completa/deferred/created.html', request= request_data, response=response)

@bp.route('installments', methods=['POST'])
def installments():
    installments_number = request.form.get('installments')
    token = request.form.get('token')
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    installments = tx.installments(token, 2)
    id_query_installments = installments['id_query_installments']
    deferred_period_index = 1
    grace_period = 'false'
    commit = tx.commit(token, id_query_installments, deferred_period_index, grace_period)
    request_data = {
        "token": token,
        "id_query_installments": id_query_installments,
        "deferred_period_index": deferred_period_index,
        "grace_period": grace_period
    }   
    return render_template('transaccion_completa/deferred/commit.html', request=request_data, response=commit, token=token)

@bp.route('status', methods=['POST'])
def status():
    token = request.form.get('token')
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.status(token)
    request_data = {
        "token": token
    }
    return render_template('transaccion_completa/deferred/status.html', request= request_data, response=response)

@bp.route('capture', methods=['POST'])
def capture():
    req = request.form
    token = req.get('token')
    buy_order = req.get('buy_order')
    authorization_code = req.get('authorization_code')
    capture_amount = req.get('capture_amount')
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.TRANSACCION_COMPLETA_DEFERRED, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    response = tx.capture(token, buy_order, authorization_code, capture_amount)
    request_data = {
        "token": token,
        "buy_order": buy_order,
        "authorization_code": authorization_code,
        "capture_amount": capture_amount
    }
    return render_template('transaccion_completa/deferred/capture.html', request= request_data, response=response)
    
