from enum import unique
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=140, unique=True)
    def __str__(self):
        return self.name

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
    name = models.CharField(verbose_name="Controller / IO List Name", max_length=82)

    def __str__(self):
        return self.name

class Device(models.Model):
    make = models.CharField(verbose_name="Make / Manufacturer", max_length=256)
    part_number = models.CharField(verbose_name="Part / Catalog Number", max_length=256)
    description = models.CharField(verbose_name="Description", max_length=256, blank=True, null=True)

    def __str__(self):
        return self.part_number

class Chassis(Device):
    io_list = models.ForeignKey(IOList, on_delete=models.CASCADE)
    name = models.CharField(max_length=26)
    address = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('io_list', 'address')

class ValveBank(Chassis):
    SINT_DATA = 4
    DINT_DATA = 8
    FORMATS = [
        (SINT_DATA, "SINT DATA"),
        (DINT_DATA, "DINT_DATA")
    ]
    data_format = models.IntegerField(choices=FORMATS)
    valve_count = models.IntegerField()

class Card(Device):
    rack = models.ForeignKey(Chassis, on_delete=models.CASCADE)
    slot = models.IntegerField()

    # address template
    # variables $RACK$, $SLOT$, $TYPE$, $POINT$
    address_template = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        unique_together = ('rack', 'slot')

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
    def address(self):


        if self.user_address is None:
            if self.card.address_template is None:
                if self.type == self.DISCRETE_INPUT:
                    _string = self.card.rack.name + ":I.Data[" + str(self.slot) + "]." + str(self.number) 
                elif self.type == self.DISCRETE_OUTPUT:
                    _string = self.card.rack.name + ":O.Data[" + str(self.slot) + "]." + str(self.number)
                elif self.type == self.ANALOG_INPUT:
                    _string = self.card.rack.name + ":" + str(self.card.slot) + ":I.Ch" + str(self.number) + "Data"
                elif self.type == self.ANALOG_OUTPUT:
                    _string = self.card.rack.name + ":" + str(self.card.slot) + ":O.Ch" + str(self.number) + "Data"
                elif self.type == self.RTD_INPUT:
                    _string = self.card.rack.name + ":" + str(self.card.slot) + ":I.Ch" + str(self.number) + "Data"
                elif self.type == self.THERMOCOUPLE:
                    _string = self.card.rack.name + ":" + str(self.card.slot) + ":I.Ch" + str(self.number) + "Data"
                elif self.type == self.HIGH_SPEED_COUNT:
                    _string = self.card.rack.name + ":" + str(self.card.slot) + ":I.Ch" + str(self.number) + "Data"
                else:
                    pass
            else:

                # get the card address template if there is one, and upper case it
                _address_template = self.card.address_template.upper()
                _string = _address_template

                if "$RACK$" in _address_template:
                    _string = _string.replace("$RACK$", self.card.rack.name)
                if "$TYPE$" in _address_template:
                    _string = _string.replace("$TYPE$", self.__io_type__())
                if "$SLOT$" in _address_template:
                    _string = _string.replace("$SLOT$", str(self.card.slot))
                if "$NUMBER$" in _address_template:
                    _string = _string.replace("$NUMBER$", str(self.number))
        else:
            _string = self.user_address
            
        return _string

    def validate_unique(self, *args, **kwargs):
        super(Point, self).validate_unique(*args, **kwargs)
        
        if hasattr(self, 'card') and hasattr(self, 'tag'):
            # checks if the same tag exists in the other tables
            _t1 = self.__class__.objects.filter(
                card__rack__io_list=self.card.rack.io_list, 
                tag=self.tag
            )
            _t2 = BusDevice.objects.filter(
                tag=self.tag
            )
            if _t1.exists() or _t2.exists():
                raise ValidationError(
                    message = "Tag collision with either bus device or point table.",
                    code="unique_together"
                )   

class BusDevice(Device):
    io_list = models.ForeignKey(IOList, on_delete=models.CASCADE)
    address = models.CharField(max_length=26)
    tag = models.CharField(max_length=26)
    description_1 = models.CharField(verbose_name="Desc 1", max_length=26, blank=True, null=True)
    description_2 = models.CharField(verbose_name="Desc 2", max_length=26, blank=True, null=True)
    description_3 = models.CharField(verbose_name="Desc 3", max_length=26, blank=True, null=True)
    description_4 = models.CharField(verbose_name="Desc 4", max_length=26, blank=True, null=True)

    def validate_unique(self, *args, **kwargs):
        super(BusDevice, self).validate_unique(*args, **kwargs)
        if hasattr(self, 'io_list') and hasattr(self, 'tag'):
            _t1 = self.__class__.objects.filter(
                io_list=self.io_list, tag=self.tag
            )
            _t2 = Point.objects.filter(
                card__rack__io_list = self.io_list, tag=self.tag
            )
            if _t1.exists() or _t2.exists():
                raise ValidationError(
                    message = "Tag collision with either bus device or point table.",
                    code="unique_together"
                )
