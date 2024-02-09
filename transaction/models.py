import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Transaction(models.Model):
    W="Withdrawal"
    D="Deposit"
    T="Account Transfer"
    CHOICES=(
        (W,"Withdrawal"),
        (D,"Deposit"),
        (T,"Account Transfer"),
    )
    previous_balance=models.DecimalField(max_digits=20,decimal_places=2)
    current_balance=models.DecimalField(max_digits=20,decimal_places=2)
    transaction_time=models.DateTimeField(default=datetime.datetime.now)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=20,decimal_places=2)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # transaction_id=models.CharField(max_length=100)
    type=models.CharField(max_length=50,choices=CHOICES)

    def get_transaction_id(self):
      return f"{self.user.username}_{self.pk}"
    
    def __str__(self) -> str:
       return self.transaction_id

