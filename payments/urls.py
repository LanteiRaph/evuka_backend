from . import views
from django.urls import path

app_name='payments'

urlpatterns = [
    path('access/token/',views.getAccessToken.as_view(), name='get_mpesa_access_token'),
    path('online/lipa/', views.lipa_na_mpesa_online.as_view(), name='lipa_na_mpesa'),
    path('mpesa/confirm/', views.mpesa_confirmation.as_view(), name='mpesa_confirm'),


    
]
