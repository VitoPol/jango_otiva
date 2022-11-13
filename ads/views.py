import json

from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Categories, Ads, Locations, Users


@csrf_exempt
def index(request):
    return JsonResponse({'test': 'test'}, status=200)


@csrf_exempt
def fill_categories_db(request):
    """Great kostbIl' """
    with open('./datasets/categories.json', 'r') as f:
        data = json.load(f)
    for dt in data:
        Categories(name=dt['name']).save()
    return JsonResponse({'result': 'Success fill categories'}, status=200)


@csrf_exempt
def fill_location_db(request):
    """Great kostbIl' """
    with open('./datasets/locations.json', 'r') as f:
        data = json.load(f)
    for dt in data:
        Categories(name=dt['name'],
                   lat=dt['lat'],
                   lng=dt['lng']
                   ).save()
    return JsonResponse({'result': 'Success fill categories'}, status=200)


@csrf_exempt
def fill_users_db(request):
    """Great kostbIl' """
    with open('./datasets/users.json', 'r') as f:
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
    """Great kostbIl' """
    with open('./datasets/ads.json', 'r') as f:
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


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesView(View):
    def get(self, request):
        categories = Categories.objects.all()
        response = []
        for category in categories:
            response.append({
                'id': category.id,
                'name': category.name
            })
        return JsonResponse(response, safe=False)

    def post(self, request):
        category_data = json.loads(request.body)
        category = Categories()
        category.name = category_data['name']
        category.save()
        return JsonResponse({
            'id': category.id,
            'name': category.name,
        })


class CategoryDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
            return JsonResponse({
                'id': category.id,
                'name': category.name,
            })
        except Http404:
            return JsonResponse({'error': 'Ох, нет объекта:/'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(View):
    def get(self, request):
        ads = Ads.objects.all()
        response = []
        for ad in ads:
            response.append({
                'id': ad.id,
                'name': ad.name,
                'author': ad.author,
                'price': ad.price,
                'description': ad.description,
                'address': ad.address,
                'is_published': ad.is_published
            })
        return JsonResponse(response, safe=False)

    def post(self, request):
        ad_data = json.loads(request.body)
        ad = Ads()
        ad.name = ad_data['name']
        ad.author = ad_data['author']
        ad.price = ad_data['price']
        ad.description = ad_data['description']
        ad.address = ad_data['address']
        ad.is_published = ad_data['is_published']
        ad.save()
        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author,
            'price': ad.price,
            'description': ad.description,
            'address': ad.address,
            'is_published': ad.is_published
        })


class AdDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
            return JsonResponse({
                'id': ad.id,
                'name': ad.name,
                'author': ad.author,
                'price': ad.price,
                'description': ad.description,
                'address': ad.address,
                'is_published': ad.is_published
            })
        except Http404:
            return JsonResponse({'error': 'Ох, нет объекта:/'}, status=404)
