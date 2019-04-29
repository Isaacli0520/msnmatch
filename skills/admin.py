from django.contrib import admin
from .models import Skill
# Register your models here.
    
class SkillRelationInline(admin.TabularInline):
    model = Skill.skill_users.through

class SkillAdmin(admin.ModelAdmin):
    list_display = ['skill_name', 'skill_intro', 'skill_type']
    list_filter = ('skill_type',)
    inlines = [
        SkillRelationInline,
    ]

admin.site.register(Skill, SkillAdmin)