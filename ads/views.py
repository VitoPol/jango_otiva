import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ads import models


@csrf_exempt
def index(request):
    return JsonResponse({'test': 'test'}, status=200)


@csrf_exempt
def add_data_to_db(request):
    with open('./datasets/categories.json', 'r') as f:
        data = json.load(f)
    for dt in data:
        models.Categories(name=dt['name']).save()
    return JsonResponse({'test': 'add_data'}, status=200)
