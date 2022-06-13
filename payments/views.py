from urllib import response
import requests
from requests.auth import HTTPBasicAuth
import json
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.http.response import HttpResponseBadRequest, HttpResponseNotAllowed
from rest_framework.views import APIView
from rest_framework import status
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPassword
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment, PaypalPayments

#get the access token, secured access to access safaricomms api for payaments.
class getAccessToken(APIView):
    #Returns an access token from safaricom.
    def get(self, request):
        consumer_key = 'yaRJg4mqUCVk8irj79FPsCTXc12Hj9Tu'
        consumer_secret = '7GXwGcqK08SBIpBh'
        api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

        r = requests.get(api_URL, auth=HTTPBasicAuth(
            consumer_key, consumer_secret))
        mpesa_access_token = json.loads(r.text)
        validated_mpesa_access_token = mpesa_access_token['access_token']

        return Response({"access_token": validated_mpesa_access_token})

#Make online payment, push sdk to user form confrimation
class lipa_na_mpesa_online(APIView):
    def sdkPush(self, phoneNumber):
        MpesaAccessToken_ = MpesaAccessToken()
        access_token = MpesaAccessToken_.getAccessToken()
        print(access_token)
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer iAjOMQg3zv6sU5uOLrtmAZPk8wFg'
        }
        request = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": phoneNumber,  # replace with your phone number to get stk push
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phoneNumber,  # replace with your phone number to get stk push
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Evuka e-Education",
            "TransactionDesc": "Testing stk push"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return json.loads(response.text)

    def get(self, request):
        response = self.sdkPush(254111850032)
        return Response(json.loads(response.text))

    def post(self, request):
        payload = json.loads(request.body)
        #extract the body of the 
        phoneNumber = payload.phoneNumber
        #make the request to safaricom server to push sdk.
        response = self.sdkPush(int(phoneNumber))
        #respnd back to the user 
        return Response(response)

class RegisterUrls(APIView):
    def get(request):
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
        headers = {"Authorization": "Bearer %s" % access_token}
        options = {"ShortCode": LipanaMpesaPassword.Business_short_code,
                "ResponseType": "Completed",
                "ConfirmationURL": "http://127.0.0.1:8000/payments/confirmation",
                "ValidationURL": "http://127.0.0.1:8000/api/payments/validation"}
        response = requests.post(api_url, json=options, headers=headers)
        return Response(response.text)


def call_back(request):
    pass


def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return Response(dict(context))

class mpesa_confirmation(APIView):
    def post(request):
        mpesa_body = request.body.decode('utf-8')
        mpesa_payment = json.loads(mpesa_body)
        payment = MpesaPayment(
            first_name=mpesa_payment['FirstName'],
            last_name=mpesa_payment['LastName'],
            middle_name=mpesa_payment['MiddleName'],
            description=mpesa_payment['TransID'],
            phone_number=mpesa_payment['MSISDN'],
            amount=mpesa_payment['TransAmount'],
            reference=mpesa_payment['BillRefNumber'],
            organization_balance=mpesa_payment['OrgAccountBalance'],
            type=mpesa_payment['TransactionType'],
        )
        payment.save()
        context = {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }
        return Response(dict(context))




#  orderId= models.CharField(max_length=60)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     courses = models.ManyToManyField(Course)
#     amount= models.DecimalField(max_digits=10, decimal_places=2)
class PaypalConfrim(APIView):
    def post(self, request):
        payload = json.loads(request.body)
        #create the payment record 
        payment = PaypalPayments(orderId=payload.orderId)

        
