from django.core.exceptions import ValidationError
from rest_framework import mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import School, Student
from .serializers import SchoolSerializer, StudentSerializer, UserSerializer


@api_view(['POST'])
@permission_classes((AllowAny, ))
def user_registration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MixinSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
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

    def get_queryset(self, *args, **kwargs):
        school_id = self.kwargs.get("school_pk")
        if school_id is None:
            return Student.objects.all()
        try:
            school = School.objects.get(id=school_id)
        except School.DoesNotExist:
            raise ValidationError('A school with this id does not exist')
        return self.queryset.filter(school=school)
