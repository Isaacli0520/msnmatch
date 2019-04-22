from django.core.management.base import BaseCommand, CommandError
from courses.models import Course


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		for cs in Course.objects.all():
			cs.delete()
		for line in open("class_offered.txt"):
			line = line.split(" ",1)
			try:
				Course.objects.create(course_number=line[0],course_name=line[1])
			except:
				print ("there was a problem")