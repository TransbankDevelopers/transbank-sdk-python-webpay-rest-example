import string
import random
from transbank.error.transbank_error import TransbankError
from patpass_comercio import bp
from flask import render_template, request
from transbank.patpass_comercio.transaction import Transaction


@bp.route('inscription')
def patpass_comercio_inscription():
    print("Patpass Comercio Transaction.inscription")
    name = 'nombre'
    first_last_name = 'apellido'
    second_last_name = 'apellido'
    rut = '14140066-5'
    return_url = request.url_root + 'patpass-comercio/end-inscription'
    service_id = random.randrange(1000000, 99999999)
    final_url = request.url_root + 'patpass-comercio/voucher-generated'
    max_amount = 0
    phone_number = random.randrange(1000000, 99999999)
    mobile_number = random.randrange(1000000, 99999999)
    patpass_name = random_string(20)
    person_email = '{}@{}.com'.format(random_string(10), random_string(7))
    commerce_mail = '{}@{}.com'.format(random_string(10), random_string(7))
    address = random_string(20)
    city = random_string(20)

    inscription_request = {
        'return_url': return_url,
        'name': name,
        'first_last_name': first_last_name,
        'second_last_name': second_last_name,
        'rut': rut,
        'service_id': service_id,
        'final_url': final_url,
        'max_amount': max_amount,
        'phone_number': phone_number,
        'mobile_number': mobile_number,
        'patpass_name': patpass_name,
        'person_email': person_email,
        'commerce_mail': commerce_mail,
        'address': address,
        'city': city,
    }

    response = Transaction.inscription(return_url, name, first_last_name, second_last_name, rut, service_id, final_url,
                                       max_amount, phone_number, mobile_number, patpass_name,
                                       person_email, commerce_mail, address, city)

    print(response)

    return render_template('patpass_comercio/inscription.html', request=inscription_request, response=response)


@bp.route('end-inscription', methods=["POST"])
def patpass_comercio_end_inscription():
    token = request.form.get("j_token")
    print("commit for token_ws: {}".format(token))

    return render_template('patpass_comercio/finish-inscription.html', token=token)


@bp.route("status", methods=["POST"])
def patpass_comercio_status():
    token = request.form.get("tokenComercio")
    try:
        response = Transaction.status(token)
        print(response)
        return render_template("patpass_comercio/status.html", token=token, response=response)
    except TransbankError as e:
        print(e.message)


@bp.route('voucher-generated', methods=["POST"])
def patpass_comercio_voucher_generated():
    return render_template('patpass_comercio/voucher-displayed.html')


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))
