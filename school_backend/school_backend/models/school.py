from django.db import models
from rest_framework import serializers, viewsets

## Types of the school
SCHOOL_TYPE = [
    ("PRI", 'Primary School'),
    ("SEC", 'Secondary School'),
    ("UNI", 'University'),
    ("COL", 'College'),
    ("HS", 'High School'),
]

class School(models.Model):
    name = models.CharField(max_length=20)
    school_type = models.CharField(choices=SCHOOL_TYPE, max_length=3)
    max_student_nb = models.PositiveIntegerField()

    
# Serializers define the API representation.
class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = School
        fields = ['name','school_type', 'max_student_nb']

# ViewSets define the view behavior.
class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
