from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

import os
import stripe

secret_key = os.environ.get('STRIPE_SECRET_KEY')
# print('SECRET KEY: ', secret_key)
stripe.api_key = secret_key

# Create your views here.
@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='pln', payment_method_types=['card'], receipt_email='test@example.com'
    )
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)

@api_view(['POST'])
def save_stripe_info(request):
    data = request.data
    email = data['email']
    charge = data['charge']
    payment_method_id = data['payment_method_id']
    extra_msg = ''
    print('CHARGE: ', charge)
    # Checking if customer with provided email already exists
    customer_data = stripe.Customer.list(email=email).data

    # if the array is empty the email has not been used yet
    if len(customer_data) == 0:
        # Creating a customer
        customer = stripe.Customer.create(
            email=email, payment_method=payment_method_id
        )
    else:
        customer = customer_data[0]
        extra_msg = 'Customer already existed.'

    stripe.PaymentIntent.create(
        customer=customer,
        payment_method=payment_method_id,
        currency='USD',
        amount=int(charge)*100,
        confirm=True,
        return_url='http://localhost:3000'
    )

    return Response(status=status.HTTP_200_OK,
                    data={
                        'message': 'Success',
                        'data': {'customer_id': customer.id,
                                'extra_msg': extra_msg}
                    })
