from django.urls import path

from ads import views

urlpatterns = [
              path('', views.AdsListView.as_view()),
              path('<int:pk>/', views.AdDetailView.as_view()),
              path('del/<int:pk>/', views.AdDeleteView.as_view()),
              path('create/', views.AdCreateView.as_view()),
              path('update/<int:pk>/', views.AdUpdateView.as_view()),
              path('<int:pk>/upload_image', views.AdUpdateImageView.as_view()),

              path('categories/', views.CategoriesListView.as_view()),
              path('categories/create/', views.CategoriesCreateView.as_view()),
              path('categories/<int:pk>/', views.CategoryDetailView.as_view()),
              path('categories/update/<int:pk>/', views.CategoriesUpdateView.as_view()),
              path('categories/del/<int:pk>/', views.CategoriesDeleteView.as_view())
              ]
