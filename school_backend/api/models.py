from django.core.exceptions import ValidationError
from django.db import models

SCHOOL_TYPE = [
    ("PRI", 'Primary School'),
    ("SEC", 'Secondary School'),
    ("UNI", 'University'),
    ("COL", 'College'),
    ("HS", 'High School'),
]


def restrict_amount(value):
    if Student.objects.filter(school=value).count() >= value.max_students:
        raise ValidationError(
            ('School already has maximal amount of students '
             + str(value.max_students)), code='invalid'
        )


class School(models.Model):
    name = models.CharField(max_length=20, unique=True)
    school_type = models.CharField(choices=SCHOOL_TYPE, max_length=3)
    max_students = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        validators=(restrict_amount,)
    )
