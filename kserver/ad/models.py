# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from ad import signals


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


class Script(models.Model):
    name = models.CharField(max_length=25)
    file = models.FileField(upload_to="scripts")
    dvm = models.PositiveIntegerField(choices=[(0,"zero"), (1,"one"), (2,"two")])
    osc = models.PositiveIntegerField(choices=[(0,"zero"), (1,"one"), (2,"two")])
    rctrl = models.PositiveIntegerField(choices=[(0,"zero"), (1,"one"), (2,"two")])
    actrl = models.PositiveIntegerField(choices=[(0,"zero"), (1,"one"), (2,"two")])
    eload = models.PositiveIntegerField(choices=[(0,"zero"), (1,"one"), (2,"two")])

    lastModified = models.DateTimeField(auto_now=True, auto_now_add=False)
    firstEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name 

    class Meta:
        ordering = ('name','file','dvm','osc','rctrl','actrl','eload')


class Model(models.Model):
    name = models.CharField(max_length=25)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, blank=False, null=False)
    voltage = models.FloatField(null=False)
    current = models.FloatField(null=False)
    scripts = models.ManyToManyField(Script, blank=True)

    lastModified = models.DateTimeField(auto_now=True, auto_now_add=False)
    firstEntered = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

    class Meta:
        ordering = ('name','product','voltage','current',)


class Station(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False,)
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

    
class Instrument(models.Model):
    name = models.CharField(max_length=25)
    type = models.CharField(max_length=25, 
                            choices=(   ('dvm','DVM'), 
                                        ('osc','OSCILLASCOPE'), 
                                        ('actrl',"ANALOG"), 
                                        ('rctrl',"RELAY"),
                                        ('eload', "E-LOAD")))
    station = models.ForeignKey(Station, on_delete=models.DO_NOTHING, blank=True, null=True)
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
        ordering = ('name','type','station','serialNumber','kepcoNumber','calibrationDate','expirationDate')

class Card(models.Model):
    serial = models.CharField(max_length=10, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    station = models.ForeignKey(Station, on_delete=models.DO_NOTHING,  null=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING, null=True)

    lastModified = models.DateTimeField(auto_now=True, auto_now_add=False)
    firstEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.serial

    def __unicode__(self):
        return self.serial

    class Meta:
        ordering = ('serial','user','station','product','model')


class Log(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=False, null=False)
    script = models.ForeignKey(Script, on_delete=models.DO_NOTHING, blank=False, null=False)
    status = models.CharField(max_length=10, choices=(("FAILED",'FAILED'), ("PASSED",'PASSED')), blank=True, null=True)
    file = models.FileField(upload_to="logs", blank=True, null=True)

    lastModified = models.DateTimeField(auto_now=True, auto_now_add=False)
    firstEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return str(self.file)

    def __unicode__(self):
        return str(self.file)

    class Meta:
        ordering = ('card','script','file','status',)


