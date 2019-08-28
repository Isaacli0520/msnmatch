from django.core.management.base import BaseCommand, CommandError
from courses.models import Course, Instructor, CourseUser, CourseInstructor, Department
import re
import os
import csv

departments = {"College of Art & Science" : {
	"African-American & African Studies": ["AAS", "SWAH"],
	"American Sign Language": ["ASL"],
	"American Studies": ["AMST"],
	"Anthropology": ["ANTH"],
	"Art": ["ARAD", "ARAH", "ARTH", "ARTS", "CASS"],
	"Astronomy": ["ASTR"],
	"Biology": ["BIOL", "HBIO"],
	"Chemistry": ["CHEM"],
	"Classics": ["CLAS", "GREE", "LATI"],
	"Cognitive Science": ["COGS"],
	"College Advising Seminars": ["COLA"],
	"Computer Science": ["CS"],
	"Drama": ["DANC", "DRAM"],
	"East Asian Languages, Literatures & Cultures": ["CHIN", "CHTR", "EALC", "EAST", "JAPN", "JPTR", "KOR", "KRTR", "TBTN"],
	"East Asian Studies": ["EAST"],
	"Economics": ["ECON"],
    "Engagement": ["EGMT"],
	"English": ["CPLT", "ENAM", "ENCR", "ENEC", "ENGL", "ENGN", "ENLS", "ENLT", "ENMC", "ENMD", "ENNC", "ENPG", "ENPW", "ENRN", "ENSP", "ENWR", "ESL"],
	"Environmental Sciences": ["EVAT", "EVEC", "EVGE", "EVHY", "EVSC"],
	"Environmental Thought & Practice": ["ETP"],
    "Forum": ["FORU"],
	"French Language & Literature": ["FREN", "FRTR"],
	"German Languages & Literatures": ["GERM", "GETR", "YIDD"],
	"Global Development Studies": ["GDS"],
	"History": ["HIAF", "HIEA", "HIEU", "HILA", "HIME", "HISA", "HIST", "HIUS", "ARCY"],
	"Jewish Studies": ["JWST"],
	"Latin American Studies": ["LAST"],
	"Liberal Arts Seminars": ["LASE"],
	"Linguistics": ["LING", "LNGS"],
	"Mathematics": ["MATH"],
	"Media Studies": ["MDST"],
	"Medieval Studies": ["MSP"],
	"Middle Eastern & South Asian Languages & Cultures": ["ARAB", "ARTR", "HEBR", "HETR", "HIND", "MESA", "MEST", "PERS", "PETR", "SANS", "SAST", "SATR", "URDU"],
	"Middle Eastern Studies": ["MEST"],
	"Music": ["MUBD", "MUEN", "MUPF", "MUSI"],
	"Neuroscience": ["NESC"],
	"Pavilion Seminars": ["PAVS"],
	"Philosophy": ["PHIL"],
	"Physics": ["PHYS"],
	"Political & Social Thought": ["PST"],
	"Political Philosophy, Policy, & Law": ["PPL"],
	"Politics": ["PLAD", "PLAP", "PLCP", "PLIR", "PLPT"],
	"Psychology": ["PSYC"],
	"Public Health Sciences": ["PHS"],
	"Religious Studies": ["RELA", "RELB", "RELC", "RELG", "RELH", "RELI", "RELJ", "RELS"],
	"Slavic Languages & Literatures": ["POL", "RUSS", "RUTR", "SLAV", "SLFK", "SLTR"],
	"Sociology": ["SOC"],
	"South Asian Studies": ["BENG", "SAST"],
	"Spanish, Italian & Portuguese": ["ITAL", "ITTR", "PORT", "SPAN", "POTR", "SPTR",],
	"Statistics": ["STAT"],
	"Women, Gender, and Sexuality": ["SWAG", "WGS"],
    "Writing": ["ENCW"],
},
"School of Engineering and Applied Science":{
	"Applied Mathematics": ["APMA"],
	"Biomedical Engineering": ["BME"],
	"Chemical Engineering": ["CHE"],
	"Civil & Environmental Engineering": ["CE"],
	"Computer Science": ["CS"],
	"Electrical & Computer Engineering": ["ECE", "CPE"],
	"General Engineering": ["ENGR"],
	"Materials Science & Engineering": ["EP", "MSE"],
	"Mechanical & Aerospace Engineering": ["AM", "MAE"],
	"Science, Technology & Society": ["STS"],
	"Systems & Information Engineering": ["SYS"],
},
"Others":{
	"Batten School of Leadership and Public Policy": ["PPOL", "LPPA", "LPPL", "LPPP", "LPPS"],
	"Curry School of Education": ["EDHS", "EDIS", "EDLF", "KINE", "PHYE"],
	"Darden School of Business": ["GBUS"],
	"Interdisciplinary Studies": ["IMP", "INST", "ISBU", "ISCP", "ISHU", "ISLS", "ISPS", "ISSS"],
	"McIntire School of Commerce": ["COMM", "GCOM"],
	"ROTC": ["AIRS", "MISC", "NASC"],
	"School of Architecture": ["ALAR", "ARAH", "ARCH", "ARH", "LAR", "PLAC", "PLAN", "SARC"],
	"School of Continuing and Professional Studies": ["ACCT", "BUS", "CJ", "HR", "IT", "NCAR", "NCBM", "NCED", "NCFA", "NCFL", "NCLE", "NCPD", "NCPH", "NCPR", "NCSS", "NCTH", "PC", "PSED", "PSEW", "PSHP", "PSMT", "PSPA", "PSPL", "PSPM", "PSWD"],
	"School of Law": ["LAW"],
	"School of Medicine": ["BIMS", "BIOC", "BIOE", "BIOP", "CELL", "MED", "MICR", "PATH", "PHAR", "PHY"],
	"School of Nursing": ["GCNL", "GNUR", "NUCO", "NUIP", "NURS"],
	"Semester at Sea": ["SEMS"],
	"University Seminars": ["USEM"],
	"Others": ["CREO", "DS", "ELA", "GSGS", "GSSJ", "GSVS", "HSCI", "ISIN", "KICH", "PHSE", "PSHM", "UNST", "ZFOR", "EDNC", "ISGE", 'ENLP', 'ENTP', 'EURS', 'GSMS'],
}
}

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		dd = {}
		ignore_list = []
		for school, department in departments.items():
			for department_name,v in department.items():
				if Department.objects.filter(name=department_name, school=school).first() == None:
					tmp_department = Department.objects.create(name=department_name, school=school)
				else:
					tmp_department = Department.objects.filter(name=department_name, school=school).first()
				for item in v:
					dd[item] = tmp_department
		for cs in Course.objects.all():
			if cs.mnemonic not in dd:
				if cs.mnemonic not in ignore_list:
					ignore_list.append(cs.mnemonic)
			else:
				cs.department =  dd[cs.mnemonic]
			cs.save()
		print(ignore_list)

def read_category():
	with open("data/category.txt") as rf:
		lines = rf.readlines()
		ret_dict = {}
		ret_dd = {}
		for i in range(0, len(lines), 2):
			ret_dict[lines[i].strip()] = lines[i + 1].strip()
		for k,v in ret_dict.items():
			ret_dd[v] = k
		print(ret_dd)
		return ret_dd