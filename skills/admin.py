from django.contrib import admin
from .models import Skill
# Register your models here.
    
class SkillRelationInline(admin.TabularInline):
    model = Skill.users.through

class SkillAdmin(admin.ModelAdmin):
    list_display = ['name','pk', 'intro', 'type']
    list_filter = ('type',)
    inlines = [
        SkillRelationInline,
    ]

admin.site.register(Skill, SkillAdmin)