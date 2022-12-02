import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from ads.models import Categories
from users.models import Locations, Users


@csrf_exempt
def fill_categories_db(request):
    """
    Заполнение таблицы БД данными из json файла
    """
    with open('categories.json', 'r') as f:
        data = json.load(f)
    for dt in data:
        Categories(name=dt['name']).save()
    return JsonResponse({'result': 'Success fill categories'}, status=200)


@csrf_exempt
def fill_location_db(request):
    """
    Заполнение таблицы БД данными из json файла
    """
    with open('locations.json', 'r') as f:
        data = json.load(f)
    for dt in data:
        Locations(name=dt["name"],
                  lat=dt["lat"],
                  lng=dt["lng"]
                  ).save()
    return JsonResponse({'result': 'Success fill categories'}, status=200)


@csrf_exempt
def fill_users_db(request):
    """
    Заполнение таблицы БД данными из json файла
    """
    with open('users.json', 'r') as f:
        data = json.load(f)
    for dt in data:
        location = get_object_or_404(Locations, pk=dt["location_id"])
        user = Users(first_name=dt['first_name'],
                     last_name=dt['last_name'],
                     username=dt['username'],
                     password=dt['password'],
                     role=dt['role'],
                     age=dt['age']
                     )
        user.save()
        user.location.add(location)
    return JsonResponse({'result': 'Success fill users'}, status=200)


@csrf_exempt
def fill_ads_db(request):
    """
    Заполнение таблицы БД данными из json файла
    """
    with open('ads.json', 'r') as f:
        data = json.load(f)
    for dt in data:
        author = get_object_or_404(Users, pk=dt['author_id'])
        category = get_object_or_404(Categories, pk=dt["category_id"])
        Ads(name=dt['name'],
            author=author,
            price=dt['price'],
            description=dt['description'],
            is_published=(dt['is_published'] == "TRUE"),
            image=dt["image"],
            category=category
            ).save()
    return JsonResponse({'result': 'Success fill ads'}, status=200)