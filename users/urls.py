from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views

urlpatterns = [
    path('', views.UsersListView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('<int:pk>/', views.UserDetailView.as_view()),
    path('del/<int:pk>/', views.UserDeleteView.as_view()),
    path('create/', views.UserCreateView.as_view()),
    path('update/<int:pk>/', views.UserUpdateView.as_view()),
]
