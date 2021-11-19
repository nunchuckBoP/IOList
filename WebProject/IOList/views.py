from typing import List
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import model_fields
from .models import BusDevice, Card, Chassis, Customer, IOList, Plant, Point, Solenoid, ValveBank

PERMISSION_DENIED_MESSAGE = "You must log in to view this content"

# Create your views here.
class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    login_url = None
    permission_denied_message = PERMISSION_DENIED_MESSAGE
    raise_exception = False

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields = model_fields['Customer']['list']

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer

# location views
class LocationListView(LoginRequiredMixin, ListView):
    model = Plant

class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Plant

class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Plant

class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Plant

# io list views
class IOListListView(LoginRequiredMixin, ListView):
    model = IOList

class IOListCreateView(LoginRequiredMixin, CreateView):
    model = IOList

class IOListUpdateView(LoginRequiredMixin, UpdateView):
    model = IOList

class IOListDeleteView(LoginRequiredMixin, DeleteView):
    model = IOList

# chassis views
class ChassisListView(LoginRequiredMixin, ListView):
    model = Chassis

class ChassisCreateView(LoginRequiredMixin, CreateView):
    model = Chassis

class ChassisUpdateView(LoginRequiredMixin, UpdateView):
    model = Chassis

class ChassisDeleteView(LoginRequiredMixin, DeleteView):
    model = Chassis


# card views
class CardListView(LoginRequiredMixin, ListView):
    model = Card

class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card

class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card


# point views
class PointListView(LoginRequiredMixin, ListView):
    model = Point

class PointCreateView(LoginRequiredMixin, CreateView):
    model = Point

class PointUpdateView(LoginRequiredMixin, UpdateView):
    model = Point

class PointDeleteView(LoginRequiredMixin, DeleteView):
    model = Point


# bank views
class BankListView(LoginRequiredMixin, ListView):
    model = ValveBank

class BankCreateView(LoginRequiredMixin, CreateView):
    model = ValveBank

class BankUpdateView(LoginRequiredMixin, UpdateView):
    model = ValveBank

class BankDeleteView(LoginRequiredMixin, DeleteView):
    model = ValveBank


# solenoid views
class SolenoidListView(LoginRequiredMixin, ListView):
    model = Solenoid

class SolenoidCreateView(LoginRequiredMixin, CreateView):
    model = Solenoid

class SolenoidUpdateView(LoginRequiredMixin, UpdateView):
    model = Solenoid

class SolenoidDeleteView(LoginRequiredMixin, DeleteView):
    model = Solenoid


# bus device views
class BusDeviceListView(LoginRequiredMixin, ListView):
    model = BusDevice

class BusDeviceCreateView(LoginRequiredMixin, CreateView):
    model = BusDevice

class BusDeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = BusDevice

class BusDeviceDeleteView(LoginRequiredMixin, DeleteView):
    model = BusDevice
