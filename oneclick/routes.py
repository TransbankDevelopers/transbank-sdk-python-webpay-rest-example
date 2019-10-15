from transbank.oneclick.request import MallTransactionAuthorizeDetails

from oneclick import bp
from flask import render_template, request
from transbank.oneclick.inscription_mall import Inscription
from transbank.oneclick.transaction_mall import Transaction
import random


@bp.route('start-form', methods=['GET'])
def show_start():
    return render_template('/oneclick/start.html')


@bp.route('status-form', methods=['GET'])
def show_status():
    return render_template('/oneclick/status_form.html')


@bp.route('start', methods=['POST'])
def start():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    response_url = request.form.get('response_url')

    resp = Inscription.start(
        user_name=user_name,
        email=email,
        response_url=response_url)

    return render_template('oneclick/started.html', resp=resp, req=request.form)


@bp.route('finish', methods=['POST'])
def finish():
    req = request.form
    token = request.form.get('TBK_TOKEN')

    resp = Inscription.finish(token=token)
    buy_order_1 = str(random.randrange(1000000, 99999999))
    buy_order_2 = str(random.randrange(1000000, 99999999))
    buy_order = str(random.randrange(1000000, 99999999))
    return render_template('oneclick/authorize.html', req=req, resp=resp, buy_order_1=buy_order_1,
                           buy_order_2=buy_order_2, buy_order=buy_order, token=token)


@bp.route('authorize', methods=['POST'])
def authorize():
    req = request.form
    token = request.form.get('token')
    user_name = request.form.get('user_name')
    buy_order = request.form.get('buy_order')
    token_inscription = request.form.get('token_inscription')

    commerce_code = request.form.get('details[0][commerce_code]')
    buy_order_child = request.form.get('details[0][buy_order]')
    installments_number = request.form.get('details[0][installments_number]')
    amount = request.form.get('details[0][amount]')

    commerce_code2 = request.form.get('details[1][commerce_code]')
    buy_order_child2 = request.form.get('details[1][buy_order]')
    installments_number2 = request.form.get('details[1][installments_number]')
    amount2 = request.form.get('details[1][amount]')

    details = MallTransactionAuthorizeDetails(commerce_code, buy_order_child, installments_number, amount) \
        .add(commerce_code2, buy_order_child2, installments_number2, amount2)

    resp = Transaction.authorize(user_name=user_name, token=token, buy_order=buy_order, details=details)
    return render_template('oneclick/refund.html', req=req, resp=resp, details=details.details, buy_order=buy_order,
                           token_inscription=token_inscription)


@bp.route('refund', methods=['POST'])
def refund():
    req = request.form
    buy_order = request.form.get('buy_order')
    child_commerce_code = request.form.get('child_commerce_code')
    child_buy_order = request.form.get('child_buy_order')
    amount = request.form.get('amount')
    token_inscription = request.form.get('token_inscription')

    resp = Transaction.refund(buy_order, child_commerce_code, child_buy_order, amount)
    return render_template('oneclick/delete.html', req=req, resp=resp, token_inscription=token_inscription)


@bp.route('delete', methods=['POST'])
def delete():
    req = request.form

    token = request.form.get('token')
    user_name = request.form.get('user_name')
    resp = Inscription.delete(token, user_name)
    return render_template('oneclick/deleted.html', req=req, resp=resp)


@bp.route('status', methods=['POST'])
def status():
    buy_order = request.form.get('buy_order')

    resp = Transaction.status(buy_order)

    return render_template('oneclick/status.html', resp=resp, req=request.form)
