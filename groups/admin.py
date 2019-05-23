from django.contrib import admin
from .models import Group, GroupFollowRelation
# Register your models here.
    
class GroupRelationInline(admin.TabularInline):
    model = Group.group_users.through

class GroupRelationInlineTags(admin.TabularInline):
    model = Group.group_tags.through

class GroupRelationInlineFollow(admin.TabularInline):
    model = GroupFollowRelation

class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'group_type']
    list_filter = ('group_type',)
    inlines = [
        GroupRelationInline,
        GroupRelationInlineTags,
        GroupRelationInlineFollow,
    ]

admin.site.register(Group, GroupAdmin)


class GroupFollowingRelationships(admin.ModelAdmin):
    list_display = ['user', 'group']
    list_filter = ('group',)
    
admin.site.register(GroupFollowRelation, GroupFollowingRelationships)