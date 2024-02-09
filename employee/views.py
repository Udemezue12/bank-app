from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from transaction.models import Transaction
from bank_app.decorators import group_required  
from customer.models import Customer 
from .filters import  TransactionFilter

@login_required
@group_required('Employee')
def index(request):
    return render(request,"ehome.html")
@login_required
@group_required('Employee')
def customer(request):
    customers = Customer.objects.all()
    paginator = Paginator(customers, 10)
    page = request.GET.get('page', 1)

    try:
        customers = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        customers = paginator.page(1)

    context = {"customers": customers}
    return render(request, 'customer.html', context)

def details(request, acc):
    customer = get_object_or_404(Customer, account_no=acc)
    context = {"data": customer}
    return render(request, "profile.html", context)

@login_required
@group_required('Employee')
def search(request):
    tlist=Transaction.objects.all()
    tfilter=TransactionFilter(request.GET, queryset=tlist)

    context={
        'filter':tfilter
    }
    return render(request, 'search/tlist.html',context)
