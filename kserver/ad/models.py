# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group


class Instrument(models.Model):
    name = models.CharField(max_length=25)
    type = models.CharField(max_length=25, 
                            choices=(   ('dvm','DVM'), 
                                        ('osc','OSCILLASCOPE'), 
                                        ('actrl',"ANALOG"), 
                                        ('rctrl',"RELAY"),
                                        ('eload', "E-LOAD")))
    serialNumber = models.CharField(max_length=25)
    kepcoNumber = models.CharField(max_length=25)
    calibrationDate = models.DateField(blank=False)
    expirationDate = models.DateField(blank=False)
    resourceID = models.CharField(max_length=25, blank=True, null=True)
    
    lastModified = models.DateTimeField(auto_now=True, auto_now_add=False)
    firstEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name 

    class Meta:
        ordering = ('name',)


class Script(models.Model):
    name = models.CharField(max_length=25)
    file = models.FileField(upload_to="")
    dvm = models.PositiveIntegerField(choices=[(0,"n/a"), (1,"one"), (2,"two")])
    osc = models.PositiveIntegerField(choices=[(0,"n/a"), (1,"one"), (2,"two")])
    rctrl = models.PositiveIntegerField(choices=[(0,"n/a"), (1,"one"), (2,"two")])
    actrl = models.PositiveIntegerField(choices=[(0,"n/a"), (1,"one"), (2,"two")])
    eload = models.PositiveIntegerField(choices=[(0,"n/a"), (1,"one"), (2,"two")])

    lastModified = models.DateTimeField(auto_now=True, auto_now_add=False)
    firstEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name 

    class Meta:
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=10)

    lastModified = models.DateTimeField(auto_now=True, auto_now_add=False)
    firstEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name 

    def __unicode__(self):
        return self.name 

    class Meta:
        ordering = ('name',)


class Model(models.Model):
    name = models.CharField(max_length=25)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, default=1, blank=False, null=False)
    scripts = models.ManyToManyField(Script, blank=True)
    voltage = models.FloatField(null=False)
    current = models.FloatField(null=False)

    lastModified = models.DateTimeField(auto_now=True, auto_now_add=False)
    firstEntered = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

    class Meta:
        ordering = ('voltage','current',)


class Station(models.Model):
    name = models.CharField(max_length=25, null=False, blank=False)
    instruments = models.ManyToManyField(Instrument, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    groups = models.ManyToManyField(Group, blank=True)

    lastModified = models.DateTimeField(auto_now=True, auto_now_add=False)
    firstEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name 

    class Meta:
        ordering = ('name',)


class Card(models.Model):
    serialNumber = models.CharField(max_length=10)
    
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, default=1, blank=True, null=True)
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING, default=1, blank=True, null=True)
    station = models.ForeignKey(Station, on_delete=models.DO_NOTHING, default=1, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, default=1, blank=True, null=True)
    
    lastModified = models.DateTimeField(auto_now=True, auto_now_add=False)
    firstEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.serialNumber

    def __unicode__(self):
        return self.serialNumber 

    class Meta:
        ordering = ('serialNumber',)





    

