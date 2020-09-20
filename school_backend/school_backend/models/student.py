from django.db import models
from school_backend.models.school import School
from django.core.exceptions import ValidationError
import uuid
from rest_framework import serializers, viewsets

## Refuse new students if the limit has been reached
def restrict_amount(value):
    if Student.objects.filter(school=value).count() >= value.max_student_nb:
        raise ValidationError(
            'School already has maximal amount of students ' + str(value.max_student_nb))

class Student(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    student_identification = models.UUIDField(
        default=uuid.uuid4, editable=False)
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, validators=(restrict_amount, ))

# Serializers define the API representation.
class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name',
                  'student_identification', 'school']


# ViewSets define the view behavior. 
## Retrieves all students if there is no param, else retrieve schools' students, if the school does not exist => error
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().select_related('school')
    serializer_class = StudentSerializer

    def get_queryset(self, *args, **kwargs):
        school_id = self.kwargs.get("school_pk")
        if school_id is None :
            return Student.objects.all() 
        try:
            school = School.objects.get(id=school_id)
        except School.DoesNotExist:
            raise ValidationError('A school with this id does not exist')
        return self.queryset.filter(school=school)
