from typing import List
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import BusDevice, Card, Chassis, Customer, IOList, Plant, Point, Solenoid, ValveBank

# Create your views here.
class CustomerListView(ListView):
    model = Customer

class CustomerCreateView(CreateView):
    model = Customer

class CustomerUpdateView(UpdateView):
    model = Customer

class CustomerDeleteView(DeleteView):
    model = Customer

# location views

class LocationListView(ListView):
    model = Plant

class LocationCreateView(CreateView):
    model = Plant

class LocationUpdateView(UpdateView):
    model = Plant

class LocationDeleteView(DeleteView):
    model = Plant

# io list views
class IOListListView(ListView):
    model = IOList

class IOListCreateView(CreateView):
    model = IOList

class IOListUpdateView(UpdateView):
    model = IOList

class IOListDeleteView(DeleteView):
    model = IOList

# chassis views
class ChassisListView(ListView):
    model = Chassis

class ChassisCreateView(CreateView):
    model = Chassis

class ChassisUpdateView(UpdateView):
    model = Chassis

class ChassisDeleteView(DeleteView):
    model = Chassis


# card views
class CardListView(ListView):
    model = Card

class CardCreateView(CreateView):
    model = Card

class CardUpdateView(UpdateView):
    model = Card

class CardDeleteView(DeleteView):
    model = Card


# point views
class PointListView(ListView):
    model = Point

class PointCreateView(CreateView):
    model = Point

class PointUpdateView(UpdateView):
    model = Point

class PointDeleteView(DeleteView):
    model = Point


# bank views
class BankListView(ListView):
    model = ValveBank

class BankCreateView(CreateView):
    model = ValveBank

class BankUpdateView(UpdateView):
    model = ValveBank

class BankDeleteView(DeleteView):
    model = ValveBank


# solenoid views
class SolenoidListView(ListView):
    model = Solenoid

class SolenoidCreateView(CreateView):
    model = Solenoid

class SolenoidUpdateView(UpdateView):
    model = Solenoid

class SolenoidDeleteView(DeleteView):
    model = Solenoid


# bus device views
class BusDeviceListView(ListView):
    model = BusDevice

class BusDeviceCreateView(CreateView):
    model = BusDevice

class BusDeviceUpdateView(UpdateView):
    model = BusDevice

class BusDeviceDeleteView(DeleteView):
    model = BusDevice
