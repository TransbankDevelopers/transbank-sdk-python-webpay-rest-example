import random

from flask import render_template, request
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


@bp.route('commit', methods=["POST"])
def webpay_plus_commit():
    token = request.form.get("token_ws")
    print("commit for token_ws: {}".format(token))

    response = Transaction.commit(token=token)
    print("response: {}".format(response))

    return render_template('webpay/plus/commit.html', token=token, response=response)