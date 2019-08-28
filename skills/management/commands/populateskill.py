from django.core.management.base import BaseCommand, CommandError
from skills.models import Skill
import pandas as pd


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		for skr in Skill.objects.all().exclude(skill_name="dummy"):
			skr.delete()
		skills_csv = pd.read_csv("skills.csv", sep=",")
		for index, row in skills_csv.iterrows():
			print(row["Name"],row["Introduction"],row["Type"])
			try:
				if not Skill.objects.filter(skill_name=row["Name"]).exists():
					Skill.objects.create(skill_name=row["Name"], skill_intro=row["Introduction"], skill_type=row["Type"])
			except:
				print ("Sth is wrong")
		if not Skill.objects.filter(skill_name="dummy").exists():
			Skill.objects.create(skill_name="dummy", skill_intro="", skill_type="Custom")