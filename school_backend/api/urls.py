from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SchoolViewSet, StudentViewSet, UserList, mongo_logs

router = DefaultRouter()

router.register('students', StudentViewSet, basename='students')
router.register('schools', SchoolViewSet, basename='schools')


urlpatterns = [
    path('', include(router.urls)),
    path('logs/', mongo_logs),
    path('logs/<str:model>/', mongo_logs),
    path('register/', UserList.as_view()),
    path('login/', include('rest_framework.urls', namespace='rest_framework'))
]
