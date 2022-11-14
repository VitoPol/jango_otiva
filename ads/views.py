import json

from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Categories, Ads
from users.models import Locations, Users


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


class CategoriesListView(ListView):
    model = Categories

    def get(self, request, *args, **kwargs):
        categories = Categories.objects.all()
        response = []
        for category in categories:
            response.append({
                'id': category.id,
                'name': category.name
            })
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesCreateView(CreateView):
    model = Categories
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        category = Categories.objects.create(name=category_data["name"])
        return JsonResponse({
            'id': category.id,
            'name': category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesUpdateView(UpdateView):
    model = Categories
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        cat_data = json.loads(request.body)
        self.object.name = cat_data["name"]

        self.object.save()
        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesDeleteView(DeleteView):
    model = Categories
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class CategoryDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(self.model, pk=self.kwargs.get(self.pk_url_kwarg))
        return JsonResponse({
            'id': category.id,
            'name': category.name,
        })


class AdsListView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        queryset = Ads.objects.select_related("author", "category").all()

        paginator = Paginator(queryset, settings.TOTAL_ON_PAGE)
        page_num = request.GET.get("page")
        page_obj = paginator.get_page(page_num)

        ads = []
        for ad in page_obj:
            ads.append({
                'id': ad.id,
                'name': ad.name,
                'author': ad.author.first_name,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'image': ad.image.url if ad.image else None,
                'category': ad.category.name
            })
        response = {
            "items": ads,
            "page": int(page_num),
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False)


class AdDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        queryset = Ads.objects.select_related("author", "category").all()
        ad = get_object_or_404(queryset, pk=self.kwargs.get(self.pk_url_kwarg))

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author.first_name,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None,
            'category': ad.category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ads
    fields = ["name", "author", "price", "description", "is_published", "image", "category"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        author = Users.objects.get(pk=ad_data["author_id"])
        category = Categories.objects.get(pk=ad_data["category_id"])
        ad = Ads.objects.create(
            name=ad_data["name"],
            author=author,
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            # image=ad_data["image"],
            category=category
        )
        return JsonResponse({
            "status": "ok",
            "name": ad.name,
            "author": ad.author.first_name
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ads
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ads
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        author = Users.objects.get(pk=ad_data["author_id"])
        category = Categories.objects.get(pk=ad_data["category_id"])

        self.object.name = ad_data["name"]
        self.object.author = author
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.is_published = ad_data["is_published"]
        self.object.category = category

        self.object.save()
        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author': self.object.author.first_name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'category': self.object.category.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateImageView(UpdateView):
    model = Ads
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES["image"]

        self.object.save()

        return JsonResponse({
            "name": self.object.name,
            "image": self.object.image.url if self.object.image else None
        })
