from django.core.management.base import BaseCommand, CommandError
from skills.models import Skill
import pandas as pd


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		for skr in Skill.objects.all():
			skr.delete()
		skills_csv = pd.read_csv("skills.csv")
		for index, row in skills_csv.iterrows():
			# print(row["Name"],row["Introduction"],row["Type"])
			try:
				Skill.objects.create(skill_name=row["Name"], skill_intro=row["Introduction"], skill_type=row["Type"])
			except:
				print ("Sth is wrong")