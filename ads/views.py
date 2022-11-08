import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Categories, Ads


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
def fill_ads_db(request):
    """Great kostbIl' """
    with open('./datasets/ads.json', 'r') as f:
        data = json.load(f)
    for dt in data:
        Ads(name=dt['name'],
            author=dt['author'],
            price=dt['price'],
            description=dt['description'],
            address=dt['address'],
            is_published=(dt['is_published'] == "TRUE")).save()
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
        category = self.get_object()
        return JsonResponse({
            'id': category.id,
            'name': category.name,
        })


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
