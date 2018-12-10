"""ATP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from rest import views


router = routers.SimpleRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'pods', views.PodViewSet)
router.register(r'blueprints', views.BlueprintViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'access-tokens', views.AccessTokenViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include(('rest_framework.urls'), namespace='rest_framework')),
    # path('api/v1/myapp/', include(('rest.urls', 'myapp'), namespace='myapp')),
    path('api/v1/', include((router.urls, 'rest'), namespace='apiv1')),
    path('rest-auth/', include('rest_auth.urls')),
]
