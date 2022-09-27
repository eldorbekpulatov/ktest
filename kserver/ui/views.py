from django.urls import reverse
from django.views import generic
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# this is for login request
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# local imports
from .forms import *
from ad.models import *
from .decorator import class_view_decorator



def logout_view(request):
    logout(request)
    return redirect('login')


class LoginView(View):
    template_name = "login/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('powerSelect')
        else:
            # sends in the login form
            form = UserForm(None)
            form.fields["username"].widget.attrs.update(
                {'placeholder': 'Enter Username'})
            form.fields["password"].widget.attrs.update(
                {'placeholder': 'Enter Password'})
            return render(request, self.template_name, {'form': form})

    def post(self, request):
        # logs in the user
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                # try to see if the user wanted to go somewhere before the log in
                if request.GET.get('next') != None:
                    return HttpResponseRedirect(request.GET.get('next'))
                else:
                    return redirect('powerSelect')
        return redirect('login')


@class_view_decorator(login_required)
class PowerSupplySelectView(View):
    template_name = "navigation/forms/powerSelect.html"

    def get(self, request):
        user = request.user
        form = PowerSupplyForm()
        context = {"user":user, "form":form}
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        form = PowerSupplyForm(request.POST)
        if form.is_valid():
            powerSupply = get_object_or_404(Product, id=form.data["powerSupply"])
            return redirect('modelSelect', powerSupply=powerSupply, psId=powerSupply.pk)
        return redirect('powerSelect')


@class_view_decorator(login_required)
class ModelSelectView(View):
    template_name = "navigation/forms/modelSelect.html"

    def get(self, request, powerSupply, psId):
        user = request.user
        ps = get_object_or_404(Product, id=psId)
        form = ModelTypeForm(None, ps)
        
        context = { "user":user, "form":form, "backURL":"/ui/"}
        return render(request, self.template_name, context)

    def post(self, request, powerSupply, psId):
        user = request.user
        ps = get_object_or_404(Product, id=psId)
        form = ModelTypeForm(request.POST, ps)
        
        if form.is_valid():
            mt = get_object_or_404(Model, id=form.data["modelTypeSelected"])
            return redirect('testSelect', powerSupply=ps, psId=psId, maxVolt=int(mt.voltage), maxCurr=int(mt.current), mtId=mt.pk)
        return redirect('modelSelect', powerSupply=ps, psId=ps.pk)


@class_view_decorator(login_required)
class TestSelectView(View):
    template_name = "navigation/forms/testSelect.html"

    def get(self, request, powerSupply, psId, maxVolt, maxCurr, mtId):
        user = request.user
        ps = get_object_or_404(Product, id=psId)
        mt = get_object_or_404(Model, id=mtId)
        tests = mt.scripts.all()
        context = { "user":user, "powerSupply":ps, "modelType":mt, 
                    "testScripts":tests, "backURL":"/ui/{}:{}/".format(ps,ps.pk)}
        return render(request, self.template_name, context)

    def post(self, request, powerSupply, id):
        user = request.user
        ps = get_object_or_404(Product, id=id)
        form = ModelTypeForm(request.POST,ps)
        
        if form.is_valid():
            modelType = get_object_or_404(Model, id=form.data["modelTypeSelected"])
            print(modelType)
            # return redirect('modelSelect', powerSupply=powerSupply, id=powerSupply.pk)
        return redirect('powerSelect')


# @class_view_decorator(login_required)
# class TestStationSelect(View):
#     template_name = "navigation/stations/stationSelect.html"

#     def get(self, request):
#         user = request.user
#         form = TestStationForm()
#         context = {"user":user, "form":form}
#         return render(request, self.template_name, context)

#     def post(self, request):
#         user = request.user
#         form = TestStationForm(request.POST)
#         if form.is_valid():
#             testStation = get_object_or_404(TestStation, id=form.data["testStation"])
#             return redirect('stationView', tsId=testStation.pk)
#         return redirect('stationSelect')


# @class_view_decorator(login_required)
# class TestStationView(View):
#     template_name = "navigation/stations/stationView.html"

#     def get(self, request, tsId):
#         user = request.user
#         station = get_object_or_404(TestStation, id=tsId)
#         context = {"user":user, "station":station}
#         return render(request, self.template_name, context)

#     def post(self, request):
#         return redirect('stationSelect')