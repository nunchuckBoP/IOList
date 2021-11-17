"""WebProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView
from .views import LocationListView, LocationCreateView, LocationUpdateView, LocationDeleteView
from .views import IOListListView, IOListCreateView, IOListUpdateView, IOListDeleteView
from .views import ChassisListView, ChassisCreateView, ChassisUpdateView, ChassisDeleteView
from .views import CardListView, CardCreateView, CardUpdateView, CardDeleteView
from .views import PointListView, PointCreateView, PointUpdateView, PointDeleteView
from .views import BankListView, BankCreateView, BankUpdateView, BankDeleteView
from .views import SolenoidListView, SolenoidCreateView, SolenoidUpdateView, SolenoidDeleteView
from .views import BusDeviceListView, BusDeviceCreateView, BusDeviceUpdateView, BusDeviceDeleteView

urlpatterns = [
#    path('admin/', admin.site.urls),

    # customer views
    path('customer/list/', CustomerListView.as_view(), name='customer-list'),
    path('customer/create/', CustomerCreateView.as_view(), name='customer-create'),
    path('customer/update/<pk>/', CustomerUpdateView.as_view(), name='customer-update'),
    path('customer/delete/<pk>/', CustomerDeleteView.as_view(), name='customer-delete'),

    # location views
    path('location/list/', LocationListView.as_view(), name='location-list'),
    path('location/create/', LocationCreateView.as_view(), name='location-create'),
    path('location/update/<pk>/', LocationUpdateView.as_view(), name='location-update'),
    path('location/delete/<pk>/', LocationDeleteView.as_view(), name='location-delete'),

    # io list views
    path('iolist/list/', IOListListView.as_view(), name='iolist-list'),
    path('iolist/create/', IOListCreateView.as_view(), name='iolist-create'),
    path('iolist/update/<pk>/', IOListUpdateView.as_view(), name='iolist-update'),
    path('iolist/delete/<pk>/', IOListDeleteView.as_view(), name='iolist-delete'),

    # chassis views
    path('chassis/list/', ChassisListView.as_view(), name='chassis-list'),
    path('chassis/create/', ChassisCreateView.as_view(), name='chassis-create'),
    path('chassis/update/<pk>/', ChassisUpdateView.as_view(), name='chassis-update'),
    path('chassis/delete/<pk>/', ChassisDeleteView.as_view(), name='chassis-delete'),

    # card views
    path('card/list/', CardListView.as_view(), name='card-list'),
    path('card/create/', CardCreateView.as_view(), name='card-create'),
    path('card/update/<pk>/', CardUpdateView.as_view(), name='card-update'),
    path('card/delete/<pk>/', CardDeleteView.as_view(), name='card-delete'),

    # point views
    path('point/list/', PointListView.as_view(), name='point-list'),
    path('point/create/', PointCreateView.as_view(), name='point-create'),
    path('point/update/<pk>/', PointUpdateView.as_view(), name='point-update'),
    path('point/delete/<pk>/', PointDeleteView.as_view(), name='point-delete'),

    # valve bank views
    path('bank/list/', BankListView.as_view(), name='bank-list'),
    path('bank/create/', BankCreateView.as_view(), name='bank-create'),
    path('bank/update/<pk>/', BankUpdateView.as_view(), name='bank-update'),
    path('bank/delete/<pk>/', BankDeleteView.as_view(), name='bank-delete'),

    # solenoid views
    path('solenoid/list/', SolenoidListView.as_view(), name='solenoid-list'),
    path('solenoid/create/', SolenoidCreateView.as_view(), name='solenoid-create'),
    path('solenoid/update/<pk>/', SolenoidUpdateView.as_view(), name='solenoid-update'),
    path('solenoid/delete/<pk>/', SolenoidDeleteView.as_view(), name='solenoid-delete'),

    # bus device views
    path('busdevice/list/', BusDeviceListView.as_view(), name='busdevice-list'),
    path('busdevice/create/', BusDeviceCreateView.as_view(), name='busdevice-create'),
    path('busdevice/update/<pk>/', BusDeviceUpdateView.as_view(), name='busdevice-update'),
    path('busdevice/delete/<pk>/', BusDeviceDeleteView.as_view(), name='busdevice-delete'),

]