from typing import List
from django.db import close_old_connections
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import model_fields
from .models import BusDevice, Card, Chassis, Customer, IOList, Plant, Point, Solenoid, ValveBank
import time

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

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = model_fields['Customer']['form']
    success_url = reverse_lazy('customer-list')

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
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

class LocationCreateView(LoginRequiredMixin, CreateView):
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

class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Plant
    fields = model_fields['Location']['form']
    success_url = reverse_lazy('location-list')

class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Plant
    fields = model_fields['Location']['form']
    success_url = reverse_lazy('location-list')

# io list views
class IOListListView(LoginRequiredMixin, ListView):
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

class IOListCreateView(LoginRequiredMixin, CreateView):
    model = IOList
    fields = model_fields['IOList']['form']
    success_url = reverse_lazy('iolist-list')

    def get_initial(self):
        if 'location_id' in self.kwargs:
            location_id = self.kwargs['location_id']
            location = get_object_or_404(Plant, pk=location_id)
            return {
                'location':location
            }

    def form_valid(self, form):
        self.object = form.save()
        self.object.modified_by = self.request.user
        self.object.modified = time.localtime()
        print(self.object)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class IOListUpdateView(LoginRequiredMixin, UpdateView):
    model = IOList
    fields = model_fields['IOList']['form']
    success_url = reverse_lazy('iolist-list')

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
