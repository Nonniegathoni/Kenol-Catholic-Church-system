from flask import Flask, Blueprint, request
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64

auth = Blueprint('auth', __name__)

consumer_key='SdRSFd91nYPYG33F1dV7tI1iwuMwi2Mb'
consumer_secret='G7dc3ldokokExWwl'
base_url='https://89d3-102-219-208-62.ngrok-free.app/'

# access token
@auth.route('/access_token')
def token():
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    consumer_key='SdRSFd91nYPYG33F1dV7tI1iwuMwi2Mb'
    consumer_secret='G7dc3ldokokExWwl'

    r= requests.get(mpesa_auth_url, auth=HTTPBasicAuth( consumer_key, consumer_secret))
    data =r.json()
    return data['access_token']

# register url
@auth.route('/register_ulr')
def register():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" %ac_token()}
    req_body={
            "ShortCode": "600383",
            "ResponseType":"Completed",
            "ConfirmationURL":base_url+"/c2b/confirmation",
            "ValidationURL":base_url+"/c2b/validation"

    }
    response_data = requests.post(
        mpesa_endpoint,
        json = req_body,
        headers=headers 
        )
    return response_data.json()

@auth.route('/c2b/confirmation')
def confirm():
    # get data
    data = request.get_json()
    #write to file
    file = open('confirm.json', 'a')
    file.write(json.dumps(data))
    file.close()
    return{
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }

@auth.route('/c2b/validation')
def validation():
    # get data
    data = request.get_json()
    #write to file
    file = open('confirm.json', 'a')
    file.write(json.dumps(data))
    file.close()
    return{
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
   
# simulate
@auth.route('simulate')
def simulate():
    mpesa_endpoint="https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    access_token = ac_token()
    headers = {"Authorization": "Bearer %s" %access_token}
    request_body={
        "ShortCode":"600383",
        "CommandID":"CustomerPayBillOnline",
        "BillRefNumber":"TestPay1",
        "Msisdn":"254796314895",
        "Amount": 100
    }

    simulate_response = request.post(mpesa_endpoint, json = request_body, headers = headers)
    return simulate_response.json()


def ac_token():
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    consumer_key='SdRSFd91nYPYG33F1dV7tI1iwuMwi2Mb'
    consumer_secret='G7dc3ldokokExWwl'

    r= requests.get(mpesa_auth_url, auth=HTTPBasicAuth( consumer_key, consumer_secret))
    data =r.json()
    return data['access_token']

@auth.route('/checkout', methods=['GET','POST'])
def checkout():
    if request.method == 'POST':
        amount = request.form.get('amount')
        phone= request.form.get('phone')

        endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        access_token = ac_token()
        headers = { "Authorization": "Bearer %s" % access_token }
        my_endpoint = base_url + "/lnmo"
        Timestamp = datetime.now()
        times = Timestamp.strftime("%Y%m%d%H%M%S")
        password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + times
        datapass = base64.b64encode(password.encode('utf-8'))

        data = {
            "BusinessShortCode": "174379",
            "Password": password,
            "Timestamp": times,
            "TransactionType": "CustomerPayBillOnline",
            "PartyA": phone,
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": my_endpoint,
            "AccountReference": "TestPay",
            "TransactionDesc": "HelloTest",
            "Amount": amount
        }
        res = requests.post(endpoint, json = data, headers = headers)
        return res.json()
    
@auth.route('/lnmo', methods=['POST'])
def incoming():
    data=request.get_json()
    print(data)
    return ("Ok")