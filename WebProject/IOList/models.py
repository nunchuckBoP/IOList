from enum import unique
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import math

model_fields = {
    'Customer':
        {
            'list':['name'],
            'form':['name'],
        },
    'Location':
        {
            'list':['customer', 'short_name', 'street', 'line2', 'city', 'state', 'zip_code'],
            'form':['customer', 'short_name', 'street', 'line2', 'city', 'state', 'zip_code'],
        },
    'IOList':
        {
            'list':['plant', 'name', 'controller', 'created', 'created_by', 'modified', 'modified_by'],
            'form':['plant', 'name', 'controller'],
        },
    'Chassis':
        {
            'list':['io_list', 'make', 'part_number', 'description', 'name', 'address'],
            'form':['io_list', 'make', 'part_number', 'description', 'name', 'address'],
        },
    'Card':
        {
            'list':['chassis', 'name', 'make', 'part_number', 'description', 'slot'],
            'form':['chassis', 'name', 'make', 'part_number', 'description', 'slot', 'address_template'],
        },
    'Point':
        {
            'list':['tag', 'address', 'description_1', 'description_2', 'description_3', 'description_4'],
            'form':['card', 'number', 'type', 'tag', 'description_1', 'description_2', 'description_3', 
            'description_4', 'user_address'],
        },
    'ValveBank':
        {
            'list':['io_list', 'name', 'address', 'make', 'part_number', 'description', 'data_format', 'valve_count', 'address_template'],
            'form':['io_list', 'name', 'address', 'make', 'part_number', 'description', 'data_format', 'valve_count', 'address_template'],
        },
    'Solenoid':
        {
            'list':['bank', 'number', 'tag', 'description_1', 'description_2', 'description_3', 'description_4', 'user_address'],
            'form':['bank', 'number', 'tag', 'description_1', 'description_2', 'description_3', 'description_4', 'user_address'],
        },
    'BusDevice':
        {
            'list':['io_list', 'make', 'part_number', 'description', 'address', 'chassis', 'tag', 'description_1', 'description_2', 'description_3'],
            'form':['io_list', 'make', 'part_number', 'description', 'address', 'chassis', 'tag', 'description_1', 'description_2', 'description_3'],
        }
}

def validate_unique_tag(iolist, tag, update_object=None):
    # returns true or false, if false, the user
    # should raise a validation error

    # first look in the points tabls
    _points = Point.objects.filter(
        card__chassis__io_list=iolist,
        tag=tag
    )
    if _points.exists():
        #if type(update_object) is not Point or len(_points) > 1 \
        #    or _points[0].pk != update_object.pk:
        #    return False
        if type(update_object) is not Point or update_object.pk is None \
            or len(_points) > 1 or _points[0].pk != update_object.pk:
            return False

    # second look in the bus device table
    _bus_devices = BusDevice.objects.filter(
        io_list=iolist, tag=tag
    )
    if _bus_devices.exists():
        if type(update_object) is not BusDevice or update_object.pk is None \
            or len(_bus_devices) > 1 or _bus_devices[0].pk != update_object.pk:
            return False

    # third look in the solenoid table
    _solenoids = Solenoid.objects.filter(
        bank__io_list=iolist, tag=tag
    )
    if _solenoids.exists():
        if type(update_object) is not Solenoid or update_object.pk is None \
            or len(_solenoids) > 1 or _solenoids[0].pk != update_object.pk:
            return False

    # if it got here, then it is validated
    return True
    
# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=140, unique=True)
    def __str__(self):
        return self.name

    @property
    def locations(self):
        return Plant.objects.filter(customer=self).count()

class Plant(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    short_name = models.CharField(verbose_name="Short Name", max_length=100, blank=False, null=False)
    street = models.CharField(verbose_name="Address Line 1", max_length=140, blank=True, null=True)
    line2 = models.CharField(verbose_name="Address Line 2", max_length=140, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=5, blank=True, null=True)
    zip_code = models.CharField(verbose_name="Zip Code", max_length=25, blank=True, null=True)

    def __str__(self):
        return self.short_name

    class Meta:
        unique_together = ('customer', 'short_name')

class IOList(models.Model):
    # one i.o list per controller
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="IO List Name", max_length=82)
    controller = models.CharField(verbose_name="Controller Name", max_length=256, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='IOList_Created_By')
    modified = models.DateTimeField(blank=False, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='IOList_Modified_By')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('plant', 'name')

class Device(models.Model):
    make = models.CharField(verbose_name="Make / Manufacturer", max_length=256)
    part_number = models.CharField(verbose_name="Part / Catalog Number", max_length=256)
    description = models.CharField(verbose_name="Description", max_length=256, blank=True, null=True)

    def __str__(self):
        return self.part_number

    class Meta:
        abstract = True

class Chassis(Device):
    io_list = models.ForeignKey(IOList, on_delete=models.CASCADE)
    name = models.CharField(max_length=26)
    address = models.CharField(max_length=20)

    @property
    def next_slot(self):
        slots = Card.objects.filter(chassis=self).values_list("slot", flat=True)
        if len(slots) > 0:
            for i in range(1, max(slots)+1):
                if i in slots:
                    continue
                else:
                    return i
            # end for
            return i+1
        else:
            return 1

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('io_list', 'address')
        ordering = ['address']

class ValveBank(Device):
    io_list = models.ForeignKey(IOList, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=20)

    SINT_DATA = 4
    INT_DATA = 8
    FORMATS = [
        (SINT_DATA, "SINT DATA"),
        (INT_DATA, "INT DATA")
    ]
    data_format = models.IntegerField(choices=FORMATS)
    valve_count = models.IntegerField()
    address_template = models.CharField(max_length=82, blank=True, null=True)

    def next_valve_number(self):
        solenoid_numbers = Solenoid.objects.filter(bank=self).values_list("number", flat=True)
        if len(solenoid_numbers) > 0:
            for i in range(0, max(solenoid_numbers)+1):
                if i in solenoid_numbers:
                    continue
                else:
                    return i
            # end for
            return i+1
        else:
            return 0

    class Meta:
        unique_together = ('io_list', 'address')
        ordering = ['address']

class Solenoid(models.Model):
    bank = models.ForeignKey(ValveBank, on_delete=models.CASCADE)
    number = models.IntegerField()
    tag = models.CharField(max_length=26)
    description_1 = models.CharField(verbose_name="Desc 1", max_length=26, blank=True, null=True)
    description_2 = models.CharField(verbose_name="Desc 2", max_length=26, blank=True, null=True)
    description_3 = models.CharField(verbose_name="Desc 3", max_length=26, blank=True, null=True)
    description_4 = models.CharField(verbose_name="Desc 4", max_length=26, blank=True, null=True)
    user_address = models.CharField(verbose_name="User Specified Address", max_length=82, blank=True, null=True)

    def __group__(self):
        return math.floor(self.number / self.bank.data_format)

    def __bit__(self):
        return self.number % self.bank.data_format

    @property
    def slot(self):
        return self.__group__()

    @property
    def point(self):
        return self.__bit__()

    @property
    def spare_tag(self):
        return self.bank.name + "SP" + str(self.number)

    @property
    def address(self):
        if self.user_address is not None:
            return self.user_address
        else:
            if self.bank.address_template is not None:
                _address_string = self.bank.address_template.upper()
                if "$RACK$" in self.bank.address_template:
                    _address_string = _address_string.replace("$RACK$", self.bank.name)
                if "$TYPE$" in self.bank.address_template:
                    _address_string = _address_string.replace("$TYPE$", "O")
                if "$GROUP$" in self.bank.address_template:
                    _address_string = _address_string.replace("$GROUP$", str(self.__group__()))
                if "$BIT$" in self.bank.address_template:
                    _address_string = _address_string.replace("$BIT$", str(self.__bit__()))
            else:
                _address_string = self.bank.name + ":O.OutputArea[" + str(self.__group__()) + "]." + str(self.__bit__())
        return _address_string

    def validate_unique(self, *args, **kwargs):
        super(Solenoid, self).validate_unique(*args, **kwargs)
        if hasattr(self, "bank") and hasattr(self, "tag"):
            _validated = validate_unique_tag(self.bank.io_list, self.tag, update_object=self)
            if not _validated:
                raise ValidationError(
                        message = "Tag collision on io list.",
                        code="unique_together"
                    )

    class Meta:
        unique_together = ('bank', 'number')
        ordering = ['number']

class Card(Device):
    name = models.CharField(max_length=140)
    chassis = models.ForeignKey(Chassis, on_delete=models.CASCADE)
    slot = models.IntegerField()

    # address template
    # variables $RACK$, $SLOT$, $TYPE$, $POINT$
    address_template = models.CharField(verbose_name="Point Address Template", max_length=256, null=True, blank=True)
    
    @property
    def next_point(self):
        points = Point.objects.filter(card=self).values_list('number', flat=True)
        if len(points) > 0:
            for i in range(0, max(points)+1):
                if i in points:
                    continue
                else:
                    return i
                # end if
            # end for
            return i+1
        else:
            return 0

    class Meta:
        unique_together = ('chassis', 'slot')
        ordering = ['slot']

class Point(models.Model):
    DISCRETE_INPUT = "DI"
    DISCRETE_OUTPUT = "DO"
    ANALOG_INPUT = "AI"
    ANALOG_OUTPUT = "AO"
    RTD_INPUT = "RTD"
    THERMOCOUPLE = "TC"
    HIGH_SPEED_COUNT = "HSC"

    TYPES = [
        (DISCRETE_INPUT, "Discrete Input"),
        (DISCRETE_OUTPUT, "Discrete Output"),
        (ANALOG_INPUT, "Analog Input"),
        (ANALOG_OUTPUT, "Analog Output"),
        (RTD_INPUT, "RTD Input"),
        (THERMOCOUPLE, "Thermocouple, Input"),
        (HIGH_SPEED_COUNT, "High Speed Count Input")
    ]

    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    number = models.IntegerField()
    type = models.CharField(max_length=6, choices=TYPES)
    tag = models.CharField(max_length=26)
    description_1 = models.CharField(verbose_name="Desc 1", max_length=26, blank=True, null=True)
    description_2 = models.CharField(verbose_name="Desc 2", max_length=26, blank=True, null=True)
    description_3 = models.CharField(verbose_name="Desc 3", max_length=26, blank=True, null=True)
    description_4 = models.CharField(verbose_name="Desc 4", max_length=26, blank=True, null=True)
    user_address = models.CharField(verbose_name="User Specified Address", max_length=82, blank=True, null=True)

    def __io_type__(self):
        inputs = [self.DISCRETE_INPUT, self.ANALOG_INPUT, self.RTD_INPUT,
                    self.THERMOCOUPLE, self.HIGH_SPEED_COUNT]
        outputs = [self.DISCRETE_OUTPUT, self.ANALOG_OUTPUT]

        if self.type in inputs:
            return "I"
        elif self.type in outputs:
            return "O"
        else:
            raise Exception("Unsupported Data Type: %s" % self.type)

    @property
    def spare_tag(self):
        if self.card.slot < 10:
            _slot_string = "S0" + str(self.card.slot)
        else:
            _slot_string = "S" + str(self.card.slot)

        if self.number < 10:
            _number_string = "P0" + str(self.number)
        else:
            _number_string = "P" + str(self.number)
        
        return self.card.chassis.name + _slot_string + _number_string

    @property
    def address(self):
        if self.user_address is None:
            if self.card.address_template is None:
                if self.type == self.DISCRETE_INPUT:
                    _string = self.card.chassis.name + ":I.Data[" + str(self.card.slot) + "]." + str(self.number) 
                elif self.type == self.DISCRETE_OUTPUT:
                    _string = self.card.chassis.name + ":O.Data[" + str(self.card.slot) + "]." + str(self.number)
                elif self.type == self.ANALOG_INPUT:
                    _string = self.card.chassis.name + ":" + str(self.card.slot) + ":I.Ch" + str(self.number) + "Data"
                elif self.type == self.ANALOG_OUTPUT:
                    _string = self.card.chassis.name + ":" + str(self.card.slot) + ":O.Ch" + str(self.number) + "Data"
                elif self.type == self.RTD_INPUT:
                    _string = self.card.chassis.name + ":" + str(self.card.slot) + ":I.Ch" + str(self.number) + "Data"
                elif self.type == self.THERMOCOUPLE:
                    _string = self.card.chassis.name + ":" + str(self.card.slot) + ":I.Ch" + str(self.number) + "Data"
                elif self.type == self.HIGH_SPEED_COUNT:
                    _string = self.card.chassis.name + ":" + str(self.card.slot) + ":I.Ch" + str(self.number) + "Data"
                else:
                    pass
            else:

                # get the card address template if there is one, and upper case it
                _address_template = self.card.address_template
                _string = _address_template

                if "$RACK$" in _address_template:
                    _string = _string.replace("$RACK$", self.card.chassis.name)
                if "$CHASSIS$" in _address_template:
                    _string = _string.replace("$CHASSIS$", self.card.chassis.name)
                if "$TYPE$" in _address_template:
                    _string = _string.replace("$TYPE$", self.__io_type__())
                if "$SLOT$" in _address_template:
                    _string = _string.replace("$SLOT$", str(self.card.slot))
                if "$NUMBER$" in _address_template:
                    _string = _string.replace("$NUMBER$", str(self.number))
                if "$POINT$" in _address_template:
                    _string = _string.replace("$POINT$", str(self.number))
        else:
            _string = self.user_address
            
        return _string

    def validate_unique(self, *args, **kwargs):
        super(Point, self).validate_unique(*args, **kwargs)
        if hasattr(self, 'card') and hasattr(self, 'tag'):

            # we should only call this on a create or if the tag has changed
            _valid = validate_unique_tag(self.card.chassis.io_list, self.tag, update_object=self)
            
            if not _valid:
                raise ValidationError(
                     message = "Tag collision on io list.",
                     code="unique_together"
                )

    class Meta:
        unique_together = ('card', 'number')
        ordering = ['number']

class BusDevice(Device):
    io_list = models.ForeignKey(IOList, on_delete=models.CASCADE)
    address = models.CharField(max_length=26)
    chassis = models.CharField(verbose_name="Chassis/Rack Name", max_length=20)
    tag = models.CharField(max_length=26)
    description_1 = models.CharField(verbose_name="Desc 1", max_length=26, blank=True, null=True)
    description_2 = models.CharField(verbose_name="Desc 2", max_length=26, blank=True, null=True)
    description_3 = models.CharField(verbose_name="Desc 3", max_length=26, blank=True, null=True)
    description_4 = models.CharField(verbose_name="Desc 4", max_length=26, blank=True, null=True)

    def validate_unique(self, *args, **kwargs):
        super(BusDevice, self).validate_unique(*args, **kwargs)
        if hasattr(self, 'io_list') and hasattr(self, 'tag'):
            _valid = validate_unique_tag(self.io_list, self.tag, update_object=self)
            if not _valid:
                raise ValidationError(
                     message = "Tag collision on io list.",
                     code="unique_together"
                )
    
    class Meta:
        unique_together = ('io_list', 'tag')
        ordering = ['address']