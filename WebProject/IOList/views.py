from typing import List
from django.db import close_old_connections
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, RedirectView
from django.views.generic.base import TemplateView
from .models import model_fields
from .models import BusDevice, Card, Chassis, Customer, IOList, Plant, Point, Solenoid, ValveBank
import time
from .mixins import NextUrlMixin

PERMISSION_DENIED_MESSAGE = "You must log in to view this content"

def add_leading_zeros(number, places):
    # convert the number to a string
    _n_str = str(number)
    _delta = places - len(_n_str)
    for i in range(0, _delta):
        _n_str = "0" + _n_str
    return _n_str

def increment_string(input_string):

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    letters = [
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                'W', 'X', 'Y', 'Z'
            ]

    # find if character ends in a number or letter
    if input_string[len(input_string)-1] in numbers:
        # NUMBER MODE
        # start from the right and find the index of the
        # last number character
        break_index = None
        for i in range(0, len(input_string)):
            j = len(input_string) - (i + 1)
            if input_string[j] in numbers:
                continue
            else:
                break_index = j
                break
        
        # if the last character is the only one that
        # is a number, then assign that to the break
        # index.
        if break_index is None:
            break_index = len(input_string) - 1
        # end if

        # gets the sub string
        sub_string = input_string[break_index+1:]
        sub_string_len = len(sub_string)

        # converts it to an integer
        _int = int(sub_string)

        # adds one to the integer
        new_int = _int + 1

        # converts the integer back to a string
        new_substring = str(new_int)

        # check and make sure the new substring is
        # the same length. If they are not, add leading
        # zeros
        if len(sub_string) > len(new_substring):
            _delta = len(sub_string) - len(new_substring)
            for i in range(0, _delta):
                new_substring = "0" + new_substring
            # end for
        # end if

        # recompose the string, and return it
        return input_string[0:break_index+1] + new_substring

    else:
        # LETTER MODE
        # loop through string from the right, until it finds
        # a character that is not "Z", or finds an integer
        start_position = None
        for i in range(0, len(input_string)):
            j = len(input_string) - (i + 1)
            if input_string[j].upper() in letters:
                if input_string[j].upper() != 'Z':
                    start_position = j
                    break
                else:
                    continue
                # end if
            else:
                start_position = j
                break
            # end if
        # end for
        #print('start_position = %s' % start_position)
        #print('len = %s' % len(tag_string))

        # loop through and add the letters
        new_string = input_string
        if input_string[start_position] not in letters and input_string[-1].upper() == 'Z':
            new_string = input_string + 'A'
        else:
            for i in range(start_position, len(input_string)):
                if input_string[i].upper() == 'Z':
                    # swaps the string
                    new_string = new_string[0:i] + 'A' + new_string[i+1:]
                else:
                    char_index = letters.index(input_string[i])
                    new_char = letters[char_index+1]
                    new_string = new_string[0:i] + new_char + new_string[i+1:]
        return new_string
    # end if
# end increment string

class HomeRedirectView(RedirectView):
    pattern_name = 'customer-list'

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
    success_url = reverse_lazy('iolist-list')

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

            context['iolist'] = iolist
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
        if 'iolist_id' in self.kwargs:
            iolist_id = self.kwargs['iolist_id']
            iolist = get_object_or_404(IOList, pk=iolist_id)
            return {
                'io_list':iolist
            }

class ChassisUpdateView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = Chassis
    fields = model_fields['Chassis']['form']
    success_url = reverse_lazy('chassis-list')

class ChassisDeleteView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = Chassis
    success_url = reverse_lazy('chassis-list')

# card views
class CardListView(LoginRequiredMixin, ListView):
    model = Card

class CardCreateView(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = Card
    fields = model_fields['Card']['form']
    success_url = reverse_lazy('cards-list')

    def get_initial(self):
        if 'chassis' in self.kwargs:
            chassis = get_object_or_404(Chassis, pk=self.kwargs['chassis'])
            next_slot = chassis.next_slot
            return_dict = {
                'chassis':chassis,
                'slot':next_slot,
                'make':'Allen Bradley'
            }

            return_dict['name'] = chassis.name.upper() + "S" + add_leading_zeros(next_slot,2)
            return return_dict

class CardUpdateView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = Card
    fields = model_fields['Card']['form']
    success_url = reverse_lazy('cards-list')


class CardDeleteView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = Card
    success_url = reverse_lazy('card-list')

# point views
class PointListView(LoginRequiredMixin, ListView):
    model = Point
    fields = model_fields['Point']['list']

class PointCreateView(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = Point
    fields = model_fields['Point']['form']
    success_url = reverse_lazy('point-list')

    def get_initial(self):
        if 'card_id' in self.kwargs:
            card_id = self.kwargs['card_id']
            card = get_object_or_404(Card, pk=card_id)
            name = card.chassis.name.upper() + "S" + add_leading_zeros(card.slot, 2) + "P" + add_leading_zeros(card.next_point, 2)

            # gets the type if there are other points specified
            types = card.point_set.all().values_list('type', flat=True)

            _return_object = {
                'card':card,
                'number':card.next_point,
                'tag':name,
                'description_1':'Spare',
            }
            
            if len(types) > 0:
                _return_object['type'] = types[0]
                for i in Point.TYPES:
                    if i[0] == types[0]:
                        _return_object['description_2'] = i[1]
                        break

            return _return_object

class PointUpdateView(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = Point
    fields = model_fields['Point']['form']
    success_url = reverse_lazy('iolist-list')

class PointDeleteView(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = Point

    # this deletes the record without confirmation
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

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
