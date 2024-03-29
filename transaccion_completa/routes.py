from transaccion_completa import bp
from flask import render_template, request
from transbank.webpay.transaccion_completa.transaction import Transaction
from datetime import datetime as dt
from datetime import timedelta


@bp.route('create', methods=['GET'])
def show_create():
    return render_template('transaccion_completa/create.html', dt=dt, timedelta=timedelta)


@bp.route('create', methods=['POST'])
def send_create():
    buy_order = request.form.get('buy_order')
    session_id = request.form.get('session_id')
    amount = request.form.get('amount')
    card_number = request.form.get('card_number')
    cvv = request.form.get('cvv')
    card_expiration_date = request.form.get('card_expiration_date')

    tx = Transaction()
    resp = tx.create(
        buy_order=buy_order, session_id=session_id, amount=amount,
        card_number=card_number, cvv=cvv, card_expiration_date=card_expiration_date
    )

    return render_template('transaccion_completa/created.html', resp=resp, req=request.form.values, dt=dt)


@bp.route('installments', methods=['POST'])
def installments():
    req = request.form
    token = request.form.get('token')
    installments_number = request.form.get('installments_number')
    tx = Transaction()
    resp = tx.installments(token=token, installments_number=installments_number)
    return render_template('transaccion_completa/installments.html', req=req, resp=resp)


@bp.route('commit', methods=['POST'])
def commit():
    req = request.form
    token = request.form.get('token')
    id_query_installments = request.form.get('id_query_installments')
    deferred_period_index = request.form.get('deferred_period_index')
    grace_period = request.form.get('grace_period') != 'false'

    tx = Transaction()
    resp = tx.commit(token=token,
                              id_query_installments=id_query_installments,
                              deferred_period_index=deferred_period_index,
                              grace_period=grace_period)
    return render_template('transaccion_completa/transaction_committed.html', req=req, resp=resp)

@bp.route('status-form', methods=['GET'])
def status_form():
    return render_template('transaccion_completa/status-form.html')

@bp.route('status', methods=['POST'])
def status():
    req = request.form
    token = req.get('token_ws')
    tx = Transaction()
    resp = tx.status(token=token)
    return render_template('transaccion_completa/transaction_status.html', req=req, resp=resp)


@bp.route('refund-form', methods=['GET'])
def refund_form():
    return render_template('transaccion_completa/refund-form.html')


@bp.route('refund', methods=['POST'])
def refund():
    req = request.form
    token = req.get('token')
    amount = req.get('amount')    
    tx = Transaction()
    resp = tx.refund(token=token, amount=amount)
    return render_template('transaccion_completa/transaction_refunded.html', req=req, resp=resp, token=token, amount=amount)
