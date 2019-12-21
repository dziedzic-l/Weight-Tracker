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
    path('api/measures', annual_measures),
    path('api/measures/<int:year>', monthly_measures),
    path('api/measures/<int:year>/<int:month>', daily_measures),
]
