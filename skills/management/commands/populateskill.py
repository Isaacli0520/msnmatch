from django.core.management.base import BaseCommand, CommandError
from skills.models import Skill
import pandas as pd


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		for skr in Skill.objects.all().exclude(name="dummy"):
			skr.delete()
		skills_csv = pd.read_csv("data/skills.csv", sep=",")
		for index, row in skills_csv.iterrows():
			print(row["Name"],row["Introduction"],row["Type"])
			try:
				if not Skill.objects.filter(name=row["Name"]).exists():
					Skill.objects.create(name=row["Name"], intro=row["Introduction"], type=row["Type"])
			except:
				print ("Sth is wrong")
		if not Skill.objects.filter(name="dummy").exists():
			Skill.objects.create(name="dummy", intro="", type="Custom")