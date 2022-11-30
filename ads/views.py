import json

from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.decorators import api_view, permission_classes

from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Categories, Ads, Selection
from ads.permissions import SelectionUpdatePermission, AdsUpdatePermission
from ads.serializers import AdDetailViewSerializer, SelectionViewSerializer, SelectionDetailViewSerializer, \
    SelectionCreateViewSerializer, AdDeleteViewSerializer
from users.models import Locations, Users


@csrf_exempt
def index(request):
    return JsonResponse({'text': 'Otiva REST API on Django REST framework'}, status=200)


@csrf_exempt
def fill_categories_db(request):
    """
    Заполнение таблицы БД данными из json файла
    """
    with open('./datasets/categories.json', 'r') as f:
        data = json.load(f)
    for dt in data:
        Categories(name=dt['name']).save()
    return JsonResponse({'result': 'Success fill categories'}, status=200)


@csrf_exempt
def fill_location_db(request):
    """
    Заполнение таблицы БД данными из json файла
    """
    with open('./datasets/locations.json', 'r') as f:
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
    """
    Заполнение таблицы БД данными из json файла
    """
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
        categories = Categories.objects.all().order_by("name")
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
        queryset = Ads.objects.select_related("author", "category").all().order_by("-price")
        category_search = request.GET.get('cat', None)
        if category_search:
            queryset = queryset.filter(category__id__icontains=category_search)
        ads_search = request.GET.get('text', None)
        if ads_search:
            queryset = queryset.filter(name__icontains=ads_search)
        place_search = request.GET.get('location', None)
        if place_search:
            queryset = queryset.filter(author__location__name__icontains=place_search)
        price_from, price_to = request.GET.get('price_from', None), request.GET.get('price_to', None)
        if price_from and price_to:
            queryset = queryset.filter(price__range=(price_from, price_to))

        paginator = Paginator(queryset, settings.TOTAL_ON_PAGE)
        page_num = int(request.GET.get("page", 1))
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
            "page": page_num,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False)


class AdDetailView(RetrieveAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdDetailViewSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def AdCreateView(request, *args, **kwargs):
    ad_data = json.loads(request.body)
    author = Users.objects.get(pk=ad_data["author_id"])
    category = Categories.objects.get(pk=ad_data["category_id"])
    ad = Ads.objects.create(
        name=ad_data["name"],
        author=author,
        price=ad_data["price"],
        description=ad_data["description"],
        is_published=ad_data["is_published"],
        category=category
    )
    return JsonResponse({
        "status": "ok",
        "name": ad.name,
        "author": ad.author.first_name
    })


class AdDeleteApiView(DestroyAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdDeleteViewSerializer
    permission_classes = [IsAuthenticated, AdsUpdatePermission]


class AdUpdateApiView(UpdateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdDeleteViewSerializer
    permission_classes = [IsAuthenticated, AdsUpdatePermission]


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


class SelectionView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionViewSerializer


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailViewSerializer


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateViewSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return Selection.objects.update(owner=request.user.id)


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateViewSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateViewSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]
