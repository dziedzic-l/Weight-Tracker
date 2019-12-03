from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.urls import path

from .views import *

urlpatterns = [
    url(r'^login/$',
        LoginView.as_view(redirect_authenticated_user=True),
        name='login'
    ),
    path('register', register, name='register'),
    path('', home, name="home"),
    path('store', store, name="measure-store"),
    path('api/data', all_time_data),
    path('api/data/<int:year>/<int:month>', monthly_data),
    path('api/data/<int:year>', annual_data),
]
