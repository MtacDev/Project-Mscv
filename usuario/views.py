from django.shortcuts import render
import requests
# Create your views here.

def acclogin(request):
    return render(request, "accTemplate/login.html")


