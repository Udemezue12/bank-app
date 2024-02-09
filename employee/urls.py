from django.urls import path
from . import views, api

app_name = 'employee'
urlpatterns = [
    path('', views.index, name='index'),
    path('customer/', views.customer, name='customer'),
    path('profile/<str:acc>/', views.details, name='details'),
    path('search/', views.search, name='search'),
    path('api/list/', api.CustomerList.as_view(), name='api_customer_list'),
    path('api/customer/', api.GetCustomer.as_view(), name='api_get_customer'),
]
