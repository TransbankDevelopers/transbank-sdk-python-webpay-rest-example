import string
import random
from patpass_by_webpay import bp
from flask import render_template, request
from transbank.patpass_by_webpay.transaction import Transaction


@bp.route('create')
def patpass_webpay_create():
    print("Patpass Webpay Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    return_url = request.url_root + 'patpass-webpay/commit'
    service_id = random_string(20)
    card_holder_id = random_string(20)
    card_holder_name = random_string(20)
    card_holder_last_name1 = random_string(20)
    card_holder_last_name2 = random_string(20)
    card_holder_mail = '{}@{}.com'.format(random_string(10), random_string(7))
    commerce_mail = '{}@{}.com'.format(random_string(10), random_string(7))
    cellphone_number = random.randrange(1000000, 99999999)
    expiration_date = '2222-11-11'

    create_request = {
        'buy_order': buy_order,
        'session_id': session_id,
        'return_url': return_url,
        'service_id': service_id,
        'card_holder_id': card_holder_id,
        'card_holder_name': card_holder_name,
        'card_holder_last_name1': card_holder_last_name1,
        'card_holder_last_name2': card_holder_last_name2,
        'card_holder_mail': card_holder_mail,
        'commerce_mail': commerce_mail,
        'cellphone_number': cellphone_number,
        'expiration_date': expiration_date,
    }

    response = Transaction.create(buy_order, session_id, 1000, return_url, service_id, card_holder_id, card_holder_name,
                                  card_holder_last_name1, card_holder_last_name2, card_holder_mail, cellphone_number,
                                  expiration_date, commerce_mail, False)

    print(response)

    return render_template('webpay/patpass/create.html', request=create_request, response=response)


@bp.route('commit', methods=["POST"])
def patpass_webpay_commit():
    token = request.form.get("token_ws")
    print("commit for token_ws: {}".format(token))

    response = Transaction.commit(token=token)
    print("response: {}".format(response))

    return render_template('webpay/patpass/commit.html', token=token, response=response)


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))
