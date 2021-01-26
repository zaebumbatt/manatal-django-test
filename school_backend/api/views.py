from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import School, Student
from .mongodb_connector import schools, students, users
from .serializers import SchoolSerializer, StudentSerializer, UserSerializer


def check_object_in_record(obj, record):
    obj = obj.lower()
    find = False
    if isinstance(record, list):
        for data in record:
            result = [str(entry).lower() for entry in data.values()]
            if obj in result:
                find = True
    else:
        result = [str(entry).lower() for entry in record.values()]
        if obj in result:
            find = True
    return True if find else False


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def mongo_logs(request, model=None):
    models = (users, students, schools)
    username = request.query_params.get('username', None)
    obj = request.query_params.get('obj', None)

    if model not in ['users', 'students', 'schools', None]:
        return Response('Wrong API endpoint')

    if username:
        result = []
        for col in models:
            for res in col.find():
                del res['_id']
                if list(res.values())[0]['username'] == username:
                    result.append(res)
        if not result:
            return Response('No data with this username')
        return JsonResponse(result, safe=False)

    if obj:
        result = []
        for col in models:
            for res in col.find():
                del res['_id']
                record = list(res.values())[0]['data']
                if check_object_in_record(obj, record):
                    result.append(res)
        if not result:
            return Response('No data with this object')
        return JsonResponse(result, safe=False)

    if not model:
        result = []
        for col in models:
            for res in col.find():
                del res['_id']
                result.append(res)
        if not result:
            return Response('Database is empty')
        return JsonResponse(result, safe=False)

    if model == 'users':
        col = users
    elif model == 'students':
        col = students
    elif model == 'schools':
        col = schools

    result = []
    for res in col.find():
        del res['_id']
        result.append(res)

    return JsonResponse(result, safe=False)


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
