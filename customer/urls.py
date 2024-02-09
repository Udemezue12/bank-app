from django.urls import path
from . import views




app_name = 'customer'


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # path('withdraw/', views.withdraw, name='withdraw'),
    path('withdraw/', views.withdraw, name='withdraw'),

    path('amount/', views.amount, name='amount'),
    path('deposit/', views.deposit, name='deposit'),
    path('amount2/', views.amount2, name='amount2'),
    path('transfer/', views.transfer, name='transfer'),
    path('result/', views.result, name='result'),
    path('edit/', views.edit, name='edit'),
    path('signup/', views.account_signup_view, name='account_signup'),
]
