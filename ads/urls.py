from django.urls import path

from ads import views

urlpatterns = [
              path('', views.AdsListView.as_view()),
              path('<int:pk>/', views.AdDetailView.as_view()),
              path('<int:pk>/del/', views.AdDeleteApiView.as_view()),
              path('create/', views.AdCreateView),
              path('<int:pk>/update/', views.AdUpdateApiView.as_view()),
              path('<int:pk>/upload_image', views.AdUpdateImageView.as_view()),

              path('categories/', views.CategoriesListView.as_view()),
              path('categories/create/', views.CategoriesCreateView.as_view()),
              path('categories/<int:pk>/', views.CategoryDetailView.as_view()),
              path('categories/<int:pk>/update/', views.CategoriesUpdateView.as_view()),
              path('categories/<int:pk>/del/', views.CategoriesDeleteView.as_view()),

              path('selections/', views.SelectionView.as_view()),
              path('selections/<int:pk>/', views.SelectionDetailView.as_view()),
              path('selections/create/', views.SelectionCreateView.as_view()),
              path('selections/<int:pk>/update/', views.SelectionUpdateView.as_view()),
              path('selections/<int:pk>/del/', views.SelectionDeleteView.as_view()),
              ]
