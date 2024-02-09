from decimal import Decimal
from django.db import models

from django.contrib.auth.models import User
from django_countries.fields import CountryField



class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    state = models.CharField(max_length=255)
    email = models.EmailField(null=False)

    country = models.CharField(max_length=255,  null=True, choices=CountryField(
    ).choices + [('', 'Select Country')])
    street=models.CharField(max_length=200)
    city=models.CharField(max_length=255)
    zip = models.CharField(max_length=100)
    balance=models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Balance", default=0.0)
    account_no=models.CharField(max_length=200,editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    pin_code=models.IntegerField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def acc_no(self):
       return f"ACC{self.pk}"

    def get_balance(self,amount,code):
        amount = Decimal(amount)
        balance = Decimal(self.balance)

        if code == 1 and balance > amount:
            return balance - amount
        elif code != 1:
            return balance + amount
        else:
            return -1
        
    def default_withdrawal_amount(self):
        return self.balance / 2
        

    

    class Meta:
        ordering = ['first_name', 'last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]

    

    





