from django.urls import path
app_name = 'myapp'
from myapp.views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup', register, name='signup'),
    path('login', custom_login, name='login'),
    path('activate/<uidb64>/<token>', activate, name='activate')
]
