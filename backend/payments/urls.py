# from django.conf.urls import url
from payments.views import test_payment, save_stripe_info
from django.urls import path

urlpatterns = [
    path('test-payment/', test_payment, name='test-payment'),
    path('save-stripe-info/', save_stripe_info, name='save-stripe-info')
    # url(r'^test-payment/$', test_payment),
]