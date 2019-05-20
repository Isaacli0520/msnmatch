from django.contrib import admin
from .models import Group
# Register your models here.
    
class GroupRelationInline(admin.TabularInline):
    model = Group.group_users.through

class GroupRelationInlineTags(admin.TabularInline):
    model = Group.group_tags.through

class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'group_type']
    list_filter = ('group_type',)
    inlines = [
        GroupRelationInline,
        GroupRelationInlineTags,
    ]

admin.site.register(Group, GroupAdmin)