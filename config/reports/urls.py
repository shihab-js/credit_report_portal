from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.dashboard, name = 'dashboard'),
    path('upload/', views.upload_report, name='upload_report'),
    path('search/', views.search_report, name='search_report'),
    path('request_report/', views.request_report, name='request_report'),
    path('download_report/', views.download_report, name='download_report'),
    path('view/<int:pk>/', views.view_report, name='view_report'),
    path('accounts/', include('django.contrib.auth.urls')),
]