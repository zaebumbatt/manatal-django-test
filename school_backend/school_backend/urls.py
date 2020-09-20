"""school_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from school_backend.models.student import Student, StudentViewSet
from school_backend.models.school import School, SchoolViewSet
from rest_framework_nested import routers


router = routers.DefaultRouter()

router.register(r'students', StudentViewSet)
router.register(r'schools', SchoolViewSet)

schools_router = routers.NestedSimpleRouter(router, r'schools', lookup='school')
schools_router.register(r'students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(schools_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]