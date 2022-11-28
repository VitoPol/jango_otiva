from rest_framework.permissions import BasePermission

from ads.models import Selection, Ads


class SelectionUpdatePermission(BasePermission):
    message = "У вас нет прав на редактирование чужих выборок =("

    def has_permission(self, request, view):
        owner_id = Selection.objects.get(pk=view.kwargs["pk"]).owner_id
        if owner_id == request.user.id:
            return True
        return False


class AdsUpdatePermission(BasePermission):
    message = "У вас нет прав на редактирование чужих объявлений =("

    def has_permission(self, request, view):
        author_id = Ads.objects.get(pk=view.kwargs["pk"]).author_id
        if author_id == request.user.id or request.user.role in ['moderator', 'admin']:
            return True
        return False
