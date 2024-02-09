import uuid
from decimal import Decimal
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from transaction.models import Transaction
from . import forms, models


# Create your views here.
def index(request):
    if request.user.groups.filter(name='Employee').exists():
        return HttpResponseRedirect(reverse('employee:index'))
    return render(request, "index.html")


@login_required
def register(request):
    user = request.user
    customer = models.Customer(user=user)
    form = forms.CustomerRegistrationForm(
        request.POST or None, instance=customer)
    context = {"customer_form": form,
               "form_url": reverse_lazy('customer:register'),
               "type": "register"
               }
    if request.method == "POST" and form.is_valid():
        customer = form.save(commit=False)
        customer.account_no = customer.acc_no()
        customer.save()

        group_name = 'Customer'
        (group, created) = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Group '{group_name}' was created.")
        else:
            print(f"Group '{group_name}' already exists.")
        user.groups.add(group)

        messages.success(request, "Registration Successfull")
        return HttpResponseRedirect(reverse('customer:index'))
    return render(request, "register.html", context)





@login_required
def edit(request):
    user = get_object_or_404(User, username=request.user.username)
    customer = get_object_or_404(models.Customer, user=user)
    form = forms.CustomerRegistrationForm(
        request.POST or None, instance=customer)
    context = {"customer_form": form,
               "form_url": reverse_lazy('customer:register'),
               "type": "edit"
               }

    if request.method == "PUT" and form.is_valid():
        e = form.save(commit=False)
        e.account_no = request.POST.get("account_no")
        e.user = user
        e .save()
        return HttpResponseRedirect(reverse('customer:index'))
    return render(request, "register.html", context)

@login_required
def amount(request):
    if request.method == 'POST':
        user = models.Customer.objects.get(user=request.user)
        t = Transaction(previous_balance=Decimal(user.balance))

        withdraw1 = request.POST.get('withdraw')
        t.amount = Decimal(withdraw1)
        a = user.get_balance(withdraw1, 1)

        if a == -1:
            messages.error(request, "No Balance!")
        else:
            user.balance = a
            t.current_balance = Decimal(user.balance)
            t.user = request.user
            t.save()

            # Generate a valid UUID for the transaction_id
            t.transaction_id = uuid.uuid4().hex
            t.type = 'Withdrawal'
            t.save()

            user.save()
            return HttpResponseRedirect(reverse('customer:profile'))

    return HttpResponseRedirect(reverse('customer:index'))

@login_required
def amount2(request):
    if request.method == 'POST':
        user = models.Customer.objects.get(user=request.user)
        amount1 = request.POST.get('deposit')

        if amount1 and amount1.strip():
            try:
                deposit_amount = Decimal(amount1)
                new_balance = user.get_balance(deposit_amount, 2)

                if new_balance is not None:
                    t = Transaction.objects.create(
                        user=request.user,
                        previous_balance=Decimal(user.balance),
                        amount=deposit_amount,
                        current_balance=new_balance,
                        type='Deposit'
                    )

                    user.balance = new_balance
                    user.save()

                    # Generate a valid UUID for the transaction_id
                    user.transaction_id = uuid.uuid4().hex
                    user.type = 'Withdrawal'
                    user.save()

                    messages.success(request, f"Successfully deposited {deposit_amount}")
                else:
                    messages.error(request, "Invalid deposit amount")
            except ValueError:
                messages.error(request, "Invalid deposit amount")
        else:
            messages.error(request, "Please provide a valid deposit amount")

    return HttpResponseRedirect(reverse('customer:profile'))

    


@login_required
def profile(request):
    user = User.objects.filter(username=request.user.username)
    context = {
        "data": user
    }
    return render(request, 'profile.html')


@login_required
def withdraw(request):
    user = get_object_or_404(User, username=request.user.username)
    customer = get_object_or_404(models.Customer, user=user)
    initial_data = {'amount': customer.default_withdrawal_amount()}
    form = forms.WithdrawForm(request.POST or None, initial=initial_data)
    context = {
        "withdraw_form": form,
        "form_url": reverse_lazy('customer:withdraw'),
        "type": "withdraw"
    }

    if request.method == "POST" and form.is_valid():
        amount_withdrawn = form.cleaned_data['amount']
        customer.balance = amount_withdrawn
        customer.save()
        return HttpResponseRedirect(reverse('customer:index'))
    else:
        return render(request, "withdraw.html", context)


@login_required
def transfer(request):
    (user, created) = User.objects.get_or_create(username=request.user.username)
    (customer, customer_created) = models.Customer.objects.get_or_create(user=user, defaults={'balance': 0.0})

    form = forms.TransferForm(request.POST or None)
    context = {
        'transfer_form': form,
        'form_url': reverse_lazy('customer:transfer'),
        "type": 'transfer'
    }

    if request.method == 'POST' and form.is_valid():
        amount_transferred = form.cleaned_data['amount']
        recipient_account_number = form.cleaned_data['recipient_account_number']

        customer.balance = getattr(customer, 'balance', 0.0)  # Set default balance if not present
        customer.balance -= amount_transferred
        customer.save()

        recipient_customer = get_object_or_404(
            models.Customer, acc_no=recipient_account_number)
        recipient_customer.balance = getattr(recipient_customer, 'balance', 0.0)
        recipient_customer.balance += amount_transferred
        recipient_customer.save()

        return HttpResponseRedirect(reverse('customer:index'))

    return render(request, "transfer.html", context=context)




# @login_required
# def result(request):
#     user = get_object_or_404(models.Customer, user=request.user)
#     amount = Decimal(request.POST.get("amount"))
#     recipient_account_number = str(request.POST.get("acc"))

   
#     sender_transaction = Transaction.objects.create(
#         user=request.user,
#         previous_balance=user.balance,
#         amount=amount,
#         current_balance=user.get_balance(amount, 1)
#     )

#     if sender_transaction.current_balance == -1:
#         messages.error(request, "No Balance!")
#         return HttpResponseRedirect(reverse('customer:profile'))

#     user.balance = sender_transaction.current_balance
#     user.save()

    
#     recipient_user = get_object_or_404(User, username=get_object_or_404(models.Customer, account_no=recipient_account_number).user.username)
#     recipient_transaction = Transaction.objects.create(
#         user=recipient_user,
#         previous_balance=recipient_user.customer.balance,
#         amount=amount,
#         current_balance=recipient_user.customer.get_balance(amount, 2)
#     )

#     recipient_user.customer.balance = recipient_transaction.current_balance
#     recipient_user.customer.save()

#     return HttpResponseRedirect(reverse('customer:profile'))

# @login_required
# def amount2(request):
#     user = get_object_or_404(models.Customer, user=request.user)
#     # if created:
#     #    print(f"User'{created}' was created.")
#     # else:
#     #    print(f" User '{user}' already exists.")
#     t=Transaction(previous_balance=Decimal(user.balance))
#     amount= request.POST.get('deposit')
#     t.amount = Decimal(amount)
#     user.balance=user.get_balance(amount,2)
#     t.current_balance = Decimal(user.balance)
#     t.user = request.user
#     t.save()
#     t.transaction_id = t.get_transaction_id()
#     t.type='Deposit'
#     t.save()
#     user.save()
#     return HttpResponseRedirect(reverse('customer:profile'))


# @login_required
# def deposit(request):
#     user=models.Customer.objects.get(user=request.user)
#     #print(user.balance)
#     context={
#         "balance":user.balance
#     }
#     return render(request, 'deposit.html', context)

# @login_required
# def deposit(request):
#     user = get_object_or_404(models.Customer, user=request.user)
#     context = {
#         "balance": user.balance
#     }
#     return render(request, 'deposit.html', context)



@login_required

def deposit(request):
    user = request.user
    try:
        customer = models.Customer.objects.get(user=user)
        context = {
            "balance": customer.balance
        }
        return render(request, 'deposit.html', context)
    except models.Customer.DoesNotExist:
        return render(request, 'error.html', {'message': 'Customer record not found for the current user.'})


def account_signup_view(request):
    if request.method == 'POST':
       
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            return redirect('index')  
    else:
        
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})




@login_required
def result(request):
    try:
        user = get_object_or_404(models.Customer, user=request.user)
        amount_str = request.POST.get("amount")
        if amount_str is None:
            messages.error(request, "Amount not provided.")
            return HttpResponseRedirect(reverse('customer:profile'))

        amount = Decimal(amount_str)
        recipient_account_number = str(request.POST.get("acc"))

        sender_balance_before = user.balance
        sender_transaction = Transaction.objects.create(
            user=request.user,
            previous_balance=sender_balance_before,
            amount=amount,
            current_balance=user.get_balance(amount, 1)
        )

        if sender_transaction.current_balance is None:
            messages.error(request, "No Balance! (Sender)")
            return HttpResponseRedirect(reverse('customer:profile'))

        user.balance = sender_transaction.current_balance
        user.save()

        recipient_customer = get_object_or_404(models.Customer, account_no=recipient_account_number)
        recipient_balance_before = recipient_customer.balance

        recipient_current_balance = recipient_customer.get_balance(amount, 2)

        if recipient_current_balance is not None:
            recipient_transaction = Transaction.objects.create(
                user=recipient_customer.user,
                previous_balance=recipient_balance_before,
                amount=amount,
                current_balance=recipient_current_balance
            )

            recipient_customer.balance = recipient_current_balance
            recipient_customer.save()
        else:
            messages.error(request, "Recipient has insufficient funds.")
            # Rollback sender's transaction
            user.balance = sender_balance_before
            user.save()
            return HttpResponseRedirect(reverse('customer:profile'))

    except Exception as e:
        messages.error(request, f"Error: {e}")
        return HttpResponseRedirect(reverse('customer:profile'))

    return HttpResponseRedirect(reverse('customer:profile'))
