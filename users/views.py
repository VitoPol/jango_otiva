import json

from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from users.models import Users


# Create your views here.

class UsersListView(ListView):
    model = Users

    def get(self, request, *args, **kwargs):
        queryset = Users.objects.prefetch_related("location")

        paginator = Paginator(queryset, settings.TOTAL_ON_PAGE)
        page_num = request.GET.get("page")
        page_obj = paginator.get_page(page_num)

        users = []
        for user in page_obj:
            users.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.author.last_name,
                'username': user.username,
                'password': user.password,
                'role': user.role,
                'age': user.age,
                'locations': list(map(str, user.location.all()))
            })
        response = {
            "items": users,
            "page": int(page_num),
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False)


# class UserDetailView(DetailView):
#     model = Ads
#
#     def get(self, request, *args, **kwargs):
#         queryset = Ads.objects.select_related("author", "category").all()
#         ad = get_object_or_404(queryset, pk=self.kwargs.get(self.pk_url_kwarg))
#
#         return JsonResponse({
#             'id': ad.id,
#             'name': ad.name,
#             'author': ad.author.first_name,
#             'price': ad.price,
#             'description': ad.description,
#             'is_published': ad.is_published,
#             'image': ad.image.url if ad.image else None,
#             'category': ad.category.name,
#         })
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class UserCreateView(CreateView):
#     model = Ads
#     fields = ["name", "author", "price", "description", "is_published", "image", "category"]
#
#     def post(self, request, *args, **kwargs):
#         ad_data = json.loads(request.body)
#         author = Users.objects.get(pk=ad_data["author_id"])
#         category = Categories.objects.get(pk=ad_data["category_id"])
#         ad = Ads.objects.create(
#             name=ad_data["name"],
#             author=author,
#             price=ad_data["price"],
#             description=ad_data["description"],
#             is_published=ad_data["is_published"],
#             # image=ad_data["image"],
#             category=category
#         )
#         return JsonResponse({
#             "status": "ok",
#             "name": ad.name,
#             "author": ad.author.first_name
#         })
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class UserDeleteView(DeleteView):
#     model = Users
#     success_url = "/"
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({"status": "ok"}, status=200)
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