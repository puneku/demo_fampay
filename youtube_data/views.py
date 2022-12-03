from django.shortcuts import render
from django.http import HttpResponse

def home(request):    
    return HttpResponse("<div style='text-align:center'><h1>Hello, Fampay!</h1></div>")

