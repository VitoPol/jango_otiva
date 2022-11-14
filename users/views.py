import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from ads.models import Ads
from users.models import Users, Locations


# Create your views here.

class UsersListView(ListView):
    model = Users

    def get(self, request, *args, **kwargs):
        # queryset = Users.objects.prefetch_related("location").annotate(total_ads=Count())
        queryset = Users.objects.annotate(total_ads=Count('ads', filter=Q(ads__is_published=True)))

        paginator = Paginator(queryset, settings.TOTAL_ON_PAGE)
        page_num = int(request.GET.get("page", 1))
        page_obj = paginator.get_page(page_num)

        users = []
        for user in page_obj:
            users.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'password': user.password,
                'role': user.role,
                'age': user.age,
                'locations': list(map(str, user.location.all())),
                "total_ads": user.total_ads
            })
        response = {
            "items": users,
            "page": page_num,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = Users

    def get(self, request, *args, **kwargs):
        queryset = Users.objects.prefetch_related("location")
        user = get_object_or_404(queryset, pk=self.kwargs.get(self.pk_url_kwarg))

        return JsonResponse({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'password': user.password,
            'role': user.role,
            'age': user.age,
            'locations': list(map(str, user.location.all()))
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = Users
    fields = ["first_name", "last_name", "username", "password", "role", "age"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        locations = Locations.objects.filter(pk__in=user_data["locations"])
        user = Users.objects.create(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            password=user_data["password"],
            role=user_data["role"],
            age=user_data["age"],
        )

        user.location.add(*locations)

        return JsonResponse({
            "status": "ok",
            "name": user.first_name,
            "username": user.username,
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = Users
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class UserUpdateView(UpdateView):
#     model = Ads
#     fields = ["name", "author", "price", "description", "is_published", "category"]
#
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#
#         ad_data = json.loads(request.body)
#         author = Users.objects.get(pk=ad_data["author_id"])
#         category = Categories.objects.get(pk=ad_data["category_id"])
#
#         self.object.name = ad_data["name"]
#         self.object.author = author
#         self.object.price = ad_data["price"]
#         self.object.description = ad_data["description"]
#         self.object.is_published = ad_data["is_published"]
#         self.object.category = category
#
#         self.object.save()
#         return JsonResponse({
#             'id': self.object.id,
#             'name': self.object.name,
#             'author': self.object.author.first_name,
#             'price': self.object.price,
#             'description': self.object.description,
#             'is_published': self.object.is_published,
#             'category': self.object.category.name
#         })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = Users
    fields = ["first_name", "last_name", "username", "password", "role", "age"]

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_data = json.loads(request.body)
        # locations = Locations.objects.filter(pk__in=user_data["locations"])

        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.role = user_data["role"]
        self.object.age = user_data["age"]

        for location in user_data["locations"]:
            user_loc, created = Locations.objects.get_or_create(pk=location)
            self.object.location.add(user_loc)

        self.object.save()

        # self.object.location.add(*locations)

        return JsonResponse({
            "name": self.object.first_name,
        })
