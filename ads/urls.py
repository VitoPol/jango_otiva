from django.urls import path

from ads import views

urlpatterns = [
              path('', views.AdsView.as_view()),
              path('categories/', views.CategoriesView.as_view()),
              path('categories/<int:pk>/', views.CategoryDetailView.as_view()),
              path('<int:pk>/', views.AdDetailView.as_view()),
              path('fill_users/', views.fill_users_db),
              path('fill_categories/', views.fill_categories_db),
              path('fill_locations/', views.fill_location_db),
              path('fill_ads/', views.fill_ads_db)
              ]
