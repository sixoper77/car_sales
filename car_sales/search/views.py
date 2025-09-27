from django.shortcuts import render
from main.models import Cars
from django.db.models import Q
from django.http import JsonResponse

def search(request):
    print(request)