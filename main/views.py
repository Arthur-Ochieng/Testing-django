from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from main.EmailBackEnd import EmailBackEnd

# Create your views here.
def home(request):
    return render (request, 'index.html')

def loginPage(request):
    return render (request, 'main/login.html')

def problem(request):
    return render (request, 'index.html')

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("&lt;h2&gt;Method Not Allowed&lt;/h2&gt;")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
    if user != None:
        login(request, user)
        user_type = user.user_type

        if user_type == '1':
            return redirect('admin_home')

        elif user_type == '2':
            return redirect('sacco_admin_home')

        elif user_type == '3':
            return redirect('member_home')

        else:
            messages.error(request, "Invalid Login!")
            return redirect('login')

    else:
        messages.error(request, "Invalid Login Credentials")
        return redirect('login')

def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: " +request.user.email+ "User Type: " +request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return redirect ('login')