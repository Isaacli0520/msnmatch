from django.core.management.base import BaseCommand, CommandError
from courses.models import Course, Instructor, CourseUser, CourseInstructor
from msnmatch import settings
from functools import cmp_to_key
from msnmatch.utils import cmp_semester


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for instructor in Instructor.objects.all():
            cs_instr = CourseInstructor.objects.filter(instructor=instructor).first()
            if not cs_instr:
                if CourseUser.objects.filter(course_instructor = cs_instr).first():
                    print("There is a review related to the to-be-deleted Instructor")
                else:
                    print("Instructor Deleted", instructor)
                    instructor.delete()