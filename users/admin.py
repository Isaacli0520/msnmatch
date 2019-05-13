from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from skills.models import Skill
import csv
from django.http import HttpResponse
from .models import Profile
from PIL import ImageFilter
from PIL import Image
from io import BytesIO
import os, sys
import uuid
from django.core.files.uploadedfile import InMemoryUploadedFile

class SkillRelationInline(admin.TabularInline):
    model = Skill.skill_users.through

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



def change_role_mentor(modeladmin, request, queryset):
    for user in queryset:
        user.profile.role = "Mentor"
        user.save()
change_role_mentor.short_description = 'Change Role to Mentor'

def change_role_mentee(modeladmin, request, queryset):
    for user in queryset:
        user.profile.role = "Mentee"
        user.save()
change_role_mentee.short_description = 'Change Role to Mentee'

def export_users(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_list.csv"'
    writer = csv.writer(response)
    writer.writerow(['username','sex', 'email', 'first_name', 'last_name', 'is_staff', 'location', 'role','year','birth_date','major','skills'])
    all_users = queryset.values_list('username','profile__sex', 'email', 'first_name', 'last_name', 'is_staff', 'profile__location', 'profile__role','profile__year','profile__birth_date','profile__major')
    for user in all_users:
        # print(user)
        writer.writerow(list(user) + [" ".join([skr.skill_name for skr in User.objects.get(username=user[0]).skill_set.all()])])
        # writer.writerow(user)
    return response
export_users.short_description = 'Export to csv'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, SkillRelationInline)
    list_display = ('username','get_sex', 'email', 'first_name', 'last_name', 'is_staff', 'get_location', 'get_role','get_year','get_birth_date','get_major')
    list_filter = ('is_staff', 'profile__sex','profile__role','profile__year')
    list_select_related = ('profile', )
    actions = [change_role_mentor, change_role_mentee, export_users, update_avatar]  # <-- Add the list action function here

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

    def get_year(self, instance):
        return instance.profile.year
    get_year.short_description = 'Year'

    def get_birth_date(self, instance):
        return instance.profile.birth_date
    get_birth_date.short_description = 'birth_date'

    def get_major(self, instance):
        return instance.profile.major
    get_major.short_description = 'Major'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)