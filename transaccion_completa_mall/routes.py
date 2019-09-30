from transaccion_completa_mall import bp
from flask import render_template, request
from transbank.transaccion_completa_mall.transaction import Transaction
from transbank.transaccion_completa_mall import child_commerce_codes
from datetime import datetime as dt
from datetime import timedelta


@bp.route('create', methods=['GET'])
def show_create():
    return render_template('/transaccion_completa_mall/create.html', dt=dt, timedelta=timedelta,
                           child_commerce_codes=child_commerce_codes)


@bp.route('create', methods=['POST'])
def send_create():
    buy_order = request.form.get('buy_order')
    session_id = request.form.get('session_id')
    card_number = request.form.get('card_number')
    card_expiration_date = request.form.get('card_expiration_date')

    details = [
        {
            'commerce_code': request.form.get('details[0][commerce_code]'),
            'buy_order': request.form.get('details[0][buy_order]'),
            'amount': request.form.get('details[0][amount]')
        },
        {
            'commerce_code': request.form.get('details[1][commerce_code]'),
            'buy_order': request.form.get('details[1][buy_order]'),
            'amount': request.form.get('details[1][amount]')
        }
    ]

    resp = Transaction.create(
        buy_order=buy_order,
        session_id=session_id,
        card_number=card_number, card_expiration_date=card_expiration_date, details=details
    )

    return render_template('transaccion_completa_mall/created.html', resp=resp, req=request.form, dt=dt, details=details)


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

    resp = Transaction.installments(token=token, details=details)
    return render_template('/transaccion_completa_mall/installments.html', req=req, resp=resp, details=details)


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
    resp = Transaction.commit(token=token,
                              details=details)
    return render_template('/transaccion_completa_mall/transaction_committed.html', req=req, resp=resp)


@bp.route('status/<token>', methods=['GET'])
def status(token):
    req = request.form
    resp = Transaction.status(token=token)
    return render_template('/transaccion_completa_mall/transaction_status.html', req=req, resp=resp)


@bp.route('refund', methods=['POST'])
def refund():
    req = request.form
    token = req.get('token')
    amount = req.get('amount')
    resp = Transaction.refund(token=token, amount=amount)
    return render_template('/transaccion_completa_mall/transaction_refunded.html', req=req, resp=resp)
