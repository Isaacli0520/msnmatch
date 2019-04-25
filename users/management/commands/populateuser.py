from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from string import ascii_lowercase
from random import shuffle, random, randint
from courses.models import Relation, Course
from users.models import MAJOR_CHOICES, YEAR_CHOICES

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		for user in User.objects.all():
			if user.last_name == "test":
				user.delete()
		# all_classes = sorted(Course.objects.all(), key=lambda x: random())
		# sem = randint(0,1)
		# for l in ascii_lowercase:
		# 	tmp_user = User.objects.create_user(username=l,first_name=l, last_name='test',
		# 						 email=l+'@virginia.edu')
		# 	tmp_year = randint(1,3)
		# 	tmp_user.profile.year = YEAR_CHOICES[tmp_year][0]
		# 	tmp_user.save()
		# 	taking_cs_num = randint(4,6)
		# 	taken_cs_num = sum([randint(4,6) for yr in range(2*(tmp_year-1) + sem)])
		# 	all_classes = sorted(Course.objects.all(), key=lambda x: random())
		# 	for j in range(taken_cs_num):
		# 		Relation.objects.create(user=tmp_user, course=all_classes[j], take="taken")
		# 	for j in range(taking_cs_num):
		# 		Relation.objects.create(user=tmp_user, course=all_classes[j + taken_cs_num], take="taking")

