from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core import serializers

from skills.models import Skill
from friendship.models import Follow
from .models import Profile, PlanProfile, PlanProfileVersion, Authenticator

from msnmatch.utils import custom_md5
from msnmatch import settings

from PIL import ImageFilter
from PIL import Image
from io import BytesIO
import csv
import os
import sys
import uuid

def export_users_new(modeladmin, request, queryset):
    json_str = serializers.serialize('json', queryset, fields=('username','profile__sex', 'email', 'first_name', 'last_name', 'is_staff', 'profile__location','profile__major','profile__major_two','profile__minor','profile__picture'))
    response = HttpResponse(json_str, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=msnmatch_users.json'
    return response
export_users_new.short_description = 'Export users to json'

class SkillRelationInline(admin.TabularInline):
    model = Skill.users.through

class FollowRelationInline(admin.TabularInline):
    model = Follow
    fk_name = 'follower'

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


def compressImage_new(uploadedImage, resize_bool, quality):
    imageTemporary = Image.open(uploadedImage)
    outputIoStream = BytesIO()
    if resize_bool:
        if imageTemporary.size[0] < 300 or imageTemporary.size[1] < 300:
            tmp_w, tmp_h = imageTemporary.size[0], imageTemporary.size[1]
        else:
            tmp_w = int(imageTemporary.size[0]/5)
            tmp_h = int(imageTemporary.size[1]/5)
        imageTemporary = imageTemporary.resize((tmp_w, tmp_h), Image.LANCZOS)
    imageTemporary = imageTemporary.filter(ImageFilter.GaussianBlur(radius=10))
    print("debug picture format:",imageTemporary.format)
    if imageTemporary.format == "PNG":
        imageTemporary = imageTemporary.convert("RGB")
    imageTemporary.save(outputIoStream , format='JPEG', quality=quality)
    outputIoStream.seek(0)
    uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % str(uuid.uuid4()), 'image/jpeg', sys.getsizeof(outputIoStream), None)
    return uploadedImage

def update_avatar(modeladmin, request, queryset):
    for user in queryset:
        if user.profile.picture:
            user.profile.avatar = compressImage_new(user.profile.picture, True, 60)
            user.save()
update_avatar.short_description = 'Update User Images'

def update_graduate_year(modeladmin, request, queryset):
    for user in queryset:
        if user.profile.year:
            user.profile.graduate_year = str(2024 - int(user.profile.year[0]))
            user.save()
update_graduate_year.short_description = 'Update User Graduate Year'

def change_role_mentor(modeladmin, request, queryset):
    for user in queryset:
        user.profile.role = "Mentor"
        user.save()
change_role_mentor.short_description = 'Change Role to Mentor'

def change_role_none(modeladmin, request, queryset):
    for user in queryset:
        user.profile.role = ""
        user.save()
change_role_none.short_description = 'Change Role to None'

def change_role_mentee(modeladmin, request, queryset):
    for user in queryset:
        user.profile.role = "Mentee"
        user.save()
change_role_mentee.short_description = 'Change Role to Mentee'

def change_matched(modeladmin, request, queryset):
    for user in queryset:
        user.profile.matched = False
        user.save()
change_matched.short_description = 'Change matched to False'

def export_users(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_list.csv"'
    writer = csv.writer(response)
    writer.writerow(['username','sex', 'wechat_id', 'email', 'first_name', 'last_name', 'location', 'role','graduate_year','major',])
    all_users = queryset.values_list('username','profile__sex', 'profile__wechat', 'email', 'first_name', 'last_name', 'profile__location', 'profile__role','profile__graduate_year','profile__major')
    for user in all_users:
        # print(user)
        writer.writerow(list(user))
        # writer.writerow(user)
    return response
export_users.short_description = 'Export to csv'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, SkillRelationInline, FollowRelationInline)
    list_display = ('username','get_sex', 'email', 'first_name', 'last_name', 'is_staff', 'get_location' ,'get_matched', 'get_role', 'get_graduate_year','get_birth_date','get_major')
    list_filter = ('is_staff', 'profile__sex','profile__role','profile__graduate_year', 'profile__matched')
    list_select_related = ('profile', )
    actions = [change_role_mentor, change_role_mentee, change_role_none, export_users, export_users_new, update_avatar, update_graduate_year, change_matched]  # <-- Add the list action function here

    def get_form(self, request, obj=None, **kwargs):
        # if request.user.is_superuser:
        #     kwargs['form'] = MySuperuserForm
        return super().get_form(request, obj, **kwargs)

    def get_location(self, instance):
        return instance.profile.location
    get_location.short_description = 'Location'

    def get_sex(self, instance):
        return instance.profile.sex
    get_sex.short_description = 'Sex'

    def get_role(self, instance):
        return instance.profile.role
    get_role.short_description = 'Role'

    def get_graduate_year(self, instance):
        return instance.profile.graduate_year
    get_graduate_year.short_description = 'Graduate Year'

    def get_birth_date(self, instance):
        return instance.profile.birth_date
    get_birth_date.short_description = 'Birth Date'

    def get_matched(self, instance):
        return instance.profile.matched
    get_matched.short_description = 'Matched'

    def get_major(self, instance):
        return instance.profile.major
    get_major.short_description = 'Major'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class PlanProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'latest')

class PlanProfileVersionAdmin(admin.ModelAdmin):
    list_display = ('plan_profile', 'version')

class AuthenticatorAdmin(admin.ModelAdmin):
    list_display = ('username', 'access_token', 'auth_id', 'date_created')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(PlanProfile, PlanProfileAdmin)
admin.site.register(PlanProfileVersion, PlanProfileVersionAdmin)
admin.site.register(Authenticator, AuthenticatorAdmin)