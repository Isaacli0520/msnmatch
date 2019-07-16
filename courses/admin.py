from django.contrib import admin
from .models import Course
# Register your models here.

class CourseUserRelationInline(admin.TabularInline):
    model = Course.users.through

class CourseInstructorRelationInline(admin.TabularInline):
    model = Course.instructors.through

class CustomUserAdmin(admin.ModelAdmin):
    inlines = (CourseUserRelationInline, CourseInstructorRelationInline)
    list_display = ['get_courseNum','type','units', 'title', 'topic']
    list_filter = ('type','mnemonic', 'units',)

    def get_courseNum(self, instance):
        return instance.mnemonic + instance.number
    get_courseNum.short_description = 'Course Number'

admin.site.register(Course, CustomUserAdmin)
