from django.urls import path, include

from . import views

urlpatterns = [
    # path('', views.ListCreateCourse.as_view(), name='course_list'),
    # path('<int:pk>/', views.RetrieveUpdateDestroyCourse.as_view(), name='course_detail'),
    # path('<course_pk>/pod/', views.ListCreatePod.as_view(), name='pod_list'),
    # path('<course_pk>/pod/<int:pk>/', views.RetrieveUpdateDestroyPod.as_view(), name='pod_detail'),
    path('images/', views.ListImage.as_view(), name='image_list'),
    path('images/<location>/', views.ListImage.as_view(), name='image_list'),
]