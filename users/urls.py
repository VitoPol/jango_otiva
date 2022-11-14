from django.urls import path

from users import views

urlpatterns = [
              path('', views.UsersListView.as_view()),
              # path('<int:pk>/', views.UserDetailView.as_view()),
              # path('del/<int:pk>/', views.UserDeleteView.as_view()),
              # path('create/', views.UserCreateView.as_view()),
              # path('update/<int:pk>/', views.UserUpdateView.as_view())
              ]