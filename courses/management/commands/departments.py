from django.core.management.base import BaseCommand, CommandError
from courses.models import Course, Instructor, CourseUser, CourseInstructor
import re
import os
import csv

departments = {
	"Commerce":["COMM", "ECON", "ENTP"],
	"Science":["ASTR", "BIOL", "CHEM", "EVSC", "PHYS", "PSYC"],
	"Humanity":["AMST", "ANTH", "ARH", "ARTH", "CLAS", "EDIS", "HIEU", "HILA"
	,"HIUS", "PHIL", "PLAD", "PLAP", "PLIR", "PLPT", "PPOL", "RELB", "RELG",
	"RELI", "RELJ", "SOC"],
	"Mathematics":["APMA", "MATH", "STAT"],
	"Engineering":["CHE", "CS", "ECE", "ENGR", "MAE", "MSE", "STS", "BME", "CE", "CPE"],
	"Architecture":["ARCH", "ARH", "MDST", "PLAN"],
	"Language":["CHTR", "CPLT", "ENGL", "ENWR", "FREN", "GERM", "GETR", "JAPN", "KOR",
	"RUTR", "SATR", "SLAV", "SPAN"],
	"ART":["ARTS", "DANC", "DRAM", "MUEN", "MUSI"],
	"Others":["COLA", "EDIS", "EGMT", "FORU", "KINE", "USEM", "WGS"]
}
mnemonics = ['AAS', 'MATH', 'ANTH', 'SWAH', 'MDST', 'ARAD', 'ARAH', 'ARTH', 'ARTS',
'ARAB', 'ARTR', 'HEBR', 'HIND', 'MESA', 'MEST', 'PERS', 'SANS', 'SAST', 'SATR', 'URDU', 'ASTR',
'MUBD', 'MUEN', 'MUPF', 'MUSI', 'BIOL', 'HBIO', 'PHIL', 'CHEM', 'PHYS', 'CLAS', 'GREE', 'LATI',
'PLAD', 'PLAP', 'PLCP', 'PLIR', 'PLPT', 'DANC', 'DRAM', 'PHS', 'PHSE', 'CHIN', 'CHTR', 'EAST',
'JAPN', 'JPTR', 'KOR', 'TBTN', 'PSYC', 'ECON', 'RELA', 'RELB', 'RELC', 'RELG', 'RELH', 'RELI',
'RELJ', 'RELS', 'CPLT', 'ENAM', 'ENCR', 'ENCW', 'ENEC', 'ENGL', 'ENGN', 'ENLP', 'ENLT', 'ENMC',
 'ENMD', 'ENNC', 'ENPG', 'ENPW', 'ENRN', 'ENSP', 'ENWR', 'POL', 'RUSS', 'RUTR', 'SLAV', 'SLTR',
 'EVAT', 'EVEC', 'EVGE', 'EVHY', 'EVSC', 'SOC', 'CREO', 'FRTR', 'FREN', 'ITAL', 'ITTR', 'KICH',
 'PORT', 'POTR', 'SPAN', 'GERM', 'GETR', 'STAT', 'HIAF', 'HIEA', 'HIEU', 'HILA', 'HIME', 'HISA',
 'HIST', 'HIUS', 'EDHS', 'USEM', 'WGS', 'ASL', 'INST', 'AMST', 'JWST', 'ARCY', 'LAST', 'COGS',
 'COLA', 'LASE', 'CS', 'LING', 'LNGS', 'ARH', 'ELA', 'NESC', 'ARCH', 'PLAN', 'EURS', 'PST',
 'GDS', 'GSGS', 'GSMS', 'GSSJ', 'GSVS', 'PAVS', 'FORU', 'EGMT', 'ES', 'NUCO', 'APMA', 'CPE',
 'ECE', 'BME', 'EP', 'MSE', 'CHE', 'MAE', 'CE', 'STS', 'SYS', 'ENGR', 'EDIS', 'EDLF', 'KINE',
 'ALAR', 'LAR', 'PLAC', 'SARC', 'AM', 'LAW', 'GBUS', 'BIMS', 'BIOC', 'BIOP', 'CELL', 'MED',
 'GCOM', 'MICR', 'PATH', 'PHAR', 'PHY', 'COMM', 'GCNL', 'GNUR', 'NUIP', 'NURS', 'ENTP', 'LPPA',
 'LPPL', 'LPPP', 'LPPS', 'DS', 'AIR', 'AIRS', 'CASS', 'EDNC', 'HSCI', 'IMP', 'MISC', 'NAS',
 'NASC', 'PPL', 'UNST', "ESL",]

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		dd = {}
		ignore_list = []
		for k,v in 	departments.items():
			for item in v:
				dd[item] = k
		for cs in Course.objects.all():
			if cs.mnemonic not in dd:
				if cs.mnemonic not in ignore_list:
					ignore_list.append(cs.mnemonic)
				cs.category = "Others"
			else:
				cs.category =  dd[cs.mnemonic]
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