from typing import List
from django.db import close_old_connections
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from .models import model_fields
from .models import BusDevice, Card, Chassis, Customer, IOList, Plant, Point, Solenoid, ValveBank
import time
from .mixins import NextUrlMixin

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
    success_url = reverse_lazy('customer-list')

class CustomerUpdateView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = Customer
    fields = model_fields['Customer']['form']
    success_url = reverse_lazy('customer-list')

class CustomerDeleteView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = Customer
    fields = model_fields['Customer']['form']
    success_url = reverse_lazy('customer-list')

# location views
class LocationListView(LoginRequiredMixin, ListView):
    model = Plant
    fields = model_fields['Location']['list']

    def get_context_data(self, **kwargs):
        context = super(LocationListView, self).get_context_data(**kwargs)
        context['fields'] = self.fields
        if "customer_id" in self.kwargs:
            customer_id = self.kwargs['customer_id']
            customer_object = get_object_or_404(Customer, pk=customer_id)
            context['object_list'] = Plant.objects.filter(customer=customer_object)
            context['customer'] = customer_object

        return context

class LocationCreateView(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = Plant
    fields = model_fields['Location']['form']
    success_url = reverse_lazy('location-list')

    def get_initial(self):
        if "customer_id" in self.kwargs:
            customer_id = self.kwargs['customer_id']
            customer = get_object_or_404(Customer, pk=customer_id)
            return {
                'customer':customer
            }

class LocationUpdateView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = Plant
    fields = model_fields['Location']['form']
    success_url = reverse_lazy('location-list')

class LocationDeleteView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = Plant
    fields = model_fields['Location']['form']
    success_url = reverse_lazy('location-list')

# io list views
class IOListListView(LoginRequiredMixin, NextUrlMixin, ListView):
    model = IOList
    fields = model_fields['IOList']['list']

    def get_context_data(self, **kwargs):
        context = super(IOListListView, self).get_context_data(**kwargs)
        context['fields'] = self.fields
        if 'location_id' in self.kwargs:
            location_id = self.kwargs['location_id']
            location = get_object_or_404(Plant, pk=location_id)
            context['object_list'] = IOList.objects.filter(plant=location)
            context['location'] = location
        return context

class IOListCreateView(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = IOList
    fields = model_fields['IOList']['form']
    success_url = reverse_lazy('iolist-list')

    def get_initial(self):
        if 'location_id' in self.kwargs:
            location_id = self.kwargs['location_id']
            location = get_object_or_404(Plant, pk=location_id)
            return {
                'plant':location
            }

    def form_valid(self, form):
        self.object = form.save()
        self.object.modified_by = self.request.user
        self.object.modified = time.localtime()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class IOListUpdateView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = IOList
    fields = model_fields['IOList']['form']
    success_url = reverse_lazy('iolist-list')

class IOListDeleteView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = IOList

class FullIOListView(LoginRequiredMixin, NextUrlMixin, TemplateView):
    model = Chassis
    template_name = 'full_iolist.html'
    
    def get_context_data(self, **kwargs):
        context = {}
        if 'iolist_id' in self.kwargs:
            iolist_id = self.kwargs['iolist_id']
            iolist = get_object_or_404(IOList, pk=iolist_id)

            chassis = Chassis.objects.filter(io_list=iolist)
            valve_banks = ValveBank.objects.filter(io_list=iolist)
            bus_devices = BusDevice.objects.filter(io_list=iolist)

            context['chassis'] = chassis
            context['valve_banks'] = valve_banks
            context['bus_devices'] = bus_devices
            
        return context

# chassis views
class ChassisListView(LoginRequiredMixin, ListView):
    model = Chassis
    fields = model_fields['Chassis']['list']

    def get_context_data(self, **kwargs):
        context = super(ChassisListView, self).get_context_data(**kwargs)
        context['fields'] = self.fields
        if 'iolist_id' in self.kwargs:
            iolist_id = self.kwargs['iolist_id']
            iolist = get_object_or_404(IOList, pk=iolist_id)
            context['object_list'] = Chassis.objects.filter(io_list=iolist)
            context['iolist'] = iolist
        return context

class ChassisCreateView(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = Chassis
    fields = model_fields['Chassis']['form']
    success_url = reverse_lazy('chassis-list')

    def get_initial(self):
        if 'iolist' in self.kwargs:
            iolist_id = self.kwargs['iolist']
            iolist = get_object_or_404(IOList, pk=iolist_id)
            return {
                'iolist':iolist
            }

class ChassisUpdateView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = Chassis
    fields = model_fields['Chassis']['form']
    success_url = reverse_lazy('chassis-list')

class ChassisDeleteView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = Chassis

# card views
class CardListView(LoginRequiredMixin, ListView):
    model = Card

class CardCreateView(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = Card

class CardUpdateView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = Card

class CardDeleteView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = Card


# point views
class PointListView(LoginRequiredMixin, ListView):
    model = Point

class PointCreateView(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = Point

class PointUpdateView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = Point

class PointDeleteView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = Point


# bank views
class BankListView(LoginRequiredMixin, ListView):
    model = ValveBank

class BankCreateView(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = ValveBank

class BankUpdateView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = ValveBank

class BankDeleteView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = ValveBank


# solenoid views
class SolenoidListView(LoginRequiredMixin, ListView):
    model = Solenoid

class SolenoidCreateView(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = Solenoid

class SolenoidUpdateView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = Solenoid

class SolenoidDeleteView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = Solenoid


# bus device views
class BusDeviceListView(LoginRequiredMixin, ListView):
    model = BusDevice

class BusDeviceCreateView(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = BusDevice

class BusDeviceUpdateView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = BusDevice

class BusDeviceDeleteView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = BusDevice
