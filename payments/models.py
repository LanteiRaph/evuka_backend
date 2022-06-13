from django.db import models

# Create your models here.
from django.db import models
from users.models import User
from courses.models import Course

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# M-pesa Payment models
#Used for Analysis , and validation //Not Used
class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'

#This is used to store accepted Mpesa transactions without accessing each field in the body.
class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'

#store successful transactions. 
class MpesaPayment(BaseModel):
    mpesa_payment= models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.first_name

#store succefull payments from paypal 
class PaypalPayments(BaseModel):
    paypal_payments= models.AutoField(primary_key=True)
    orderId= models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    amount= models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        verbose_name = 'Paypal Payments'
        verbose_name_plural = 'Paypal Payments'

    def __str__(self):
        return self.orderId
    
