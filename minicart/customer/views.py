from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,View
from .forms import Regform,LogForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
# Create your views here.


class Logview(FormView):
    template_name="log.html" 
    form_class=LogForm
    def post(self,request):
        form_data=LogForm(data=request.POST)
        if form_data.is_valid():
            user=form_data.cleaned_data.get("username")
            pswd=form_data.cleaned_data.get("password")
            user_ob=authenticate(request,username=user,password=pswd)
            if user_ob:
                login(request,user_ob)
                messages.success(request,"Login Successful!!")
                return redirect("home")
        else:
            messages.error(request,"Login Failed!! Invalid Username or password!")
            return render(request,"log.html",{"form":form_data})   
           
# class Logview(View):
#     def get(self,request):
#         form=LogForm()
#         us=request.user
#         return render(request,"log.html",{"form":form,"user":us})
#     def post(self,request):
#         form_data=LogForm(data=request.POST)
#         if form_data.is_valid():
#             user=form_data.cleaned_data.get("username")
#             pswd=form_data.cleaned_data.get("password")
#             user_ob=authenticate(request,username=user,password=pswd)
#             if user_ob:
#                 login(request,user_ob)
#                 messages.success(request,"Login Successful!!")
#                 return redirect("home")
#         else:
#             messages.error(request,"Login Failed!! Invalid Username or password!")
#             return render(request,"log.html",{"form":form_data})
        
# class RegView(View):
#     def get (self,request):
#         form=Regform()
#         return render(request,"reg.html",{"form":form}) 
#     def post(self,request):
#         form_data=Regform(data=request.POST)
#         if form_data.is_valid():
#             form_data.save()
#             return redirect("log")
#         else:
#             return render(request,"reg.html",{"form":form_data})   
    
class RegView(CreateView):
    template_name="reg.html"
    form_class=Regform
    success_url=reverse_lazy("log")
    
class LgOut(View):
    def get(self,request):
        logout(request)
        return redirect("log")
