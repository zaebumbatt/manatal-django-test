from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SchoolViewSet, StudentViewSet, user_registration

router = DefaultRouter()

router.register('students', StudentViewSet, basename='student')
router.register('schools', SchoolViewSet, basename='school')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', user_registration),
    path('login/', include('rest_framework.urls', namespace='rest_framework'))
]