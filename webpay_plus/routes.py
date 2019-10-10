import random

from flask import render_template, request
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction

from webpay_plus import bp


@bp.route("create", methods=["GET"])
def webpay_plus_create():
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = random.randrange(10000, 1000000)
    return_url = request.url_root + 'webpay-plus/commit'

    create_request = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    response = Transaction.create(buy_order, session_id, amount, return_url)

    print(response)

    return render_template('webpay/plus/create.html', request=create_request, response=response)


@bp.route("commit", methods=["POST"])
def webpay_plus_commit():
    token = request.form.get("token_ws")
    print("commit for token_ws: {}".format(token))

    response = Transaction.commit(token=token)
    print("response: {}".format(response))

    return render_template('webpay/plus/commit.html', token=token, response=response)


@bp.route("refund", methods=["POST"])
def webpay_plus_refund():
    token = request.form.get("token_ws")
    amount = request.form.get("amount")
    print("refund for token_ws: {} by amount: {}".format(token, amount))

    try:
        response = Transaction.refund(token, amount)
        print("response: {}".format(response))

        return render_template("webpay/plus/refund.html", token=token, amount=amount, response=response)
    except TransbankError as e:
        print(e.message)


@bp.route("refund-form", methods=["GET"])
def webpay_plus_refund_form():
    return render_template("webpay/plus/refund-form.html")