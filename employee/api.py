from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from customer.models import Customer
from .serializers import CustomerSerializer  # Import your serializer

class GetCustomer(generics.ListAPIView):
    def get(self, request, format=None, *args, **kwargs):
        try:
            account_no = request.GET.get('acc') 
            customer = Customer.objects.get(account_no=account_no)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except MultiValueDictKeyError:
            return Response({'error': 'acc parameter is missing in the request.'}, status=400)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found.'}, status=404)

class CustomerList(APIView):
    def get(self, request):
        customers=Customer.objects.all()
        s=CustomerSerializer(customers, many=True)
        return Response(s.data)

    def post(self,request):
        pass
