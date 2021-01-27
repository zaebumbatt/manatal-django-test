from django.contrib.auth.models import User
from rest_framework import generics, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Log, School, Student
from .serializers import (LogSerializer, SchoolSerializer, StudentSerializer,
                          UserSerializer)


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def mongo_logs(request, model=None):
    models = {
        'users': 'User',
        'students': 'Student',
        'schools': 'School'
    }
    username = request.query_params.get('username', None)
    obj = request.query_params.get('obj', None)

    if model not in ['users', 'students', 'schools', None]:
        raise ValidationError('Wrong API endpoint')

    if username:
        queryset = Log.objects.filter(username=username)
        if not queryset:
            raise ValidationError('Wrong username')

    if obj:
        queryset = Log.objects.all()
        result = []
        for entry in queryset:
            if entry.data and obj in entry.data.values():
                result.append(entry)
        queryset = result
        if not queryset:
            raise ValidationError('No data with this object')

    elif not model:
        queryset = Log.objects.all()
        if not queryset:
            raise ValidationError('Database is empty')
    else:
        queryset = Log.objects.filter(model=models[model])
        if not queryset:
            raise ValidationError('Model is empty')

    serializer = LogSerializer(queryset, many=True)

    return Response(serializer.data)


class UserList(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class MixinSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    pass


class SchoolViewSet(MixinSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class StudentViewSet(MixinSet):
    queryset = Student.objects.all().select_related('school')
    serializer_class = StudentSerializer
