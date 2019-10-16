from django.contrib import admin
from .models import Course, CourseInstructor, Instructor
# Register your models here.

class CourseUserRelationInline(admin.TabularInline):
    model = Course.users.through

class CourseInstructorRelationInline(admin.TabularInline):
    model = Course.instructors.through

class CustomCourseAdmin(admin.ModelAdmin):
    inlines = (CourseInstructorRelationInline, CourseUserRelationInline) #CourseUserRelationInline,
    list_display = ['get_courseNum','type','units', 'title']
    list_filter = ('type','mnemonic', 'units',)
    search_fields = ["mnemonic", "number", "title"]

    def get_courseNum(self, instance):
        return instance.mnemonic + instance.number
    get_courseNum.short_description = 'Course Number'

class CustomCourseInstructorAdmin(admin.ModelAdmin):
    list_display = ['course','instructor','semester', 'topic']
    list_filter = ('semester',)
    autocomplete_fields = ['course','instructor',]

class CustomInstructorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    search_fields = ['first_name','last_name']


admin.site.register(CourseInstructor, CustomCourseInstructorAdmin)
admin.site.register(Instructor, CustomInstructorAdmin)
admin.site.register(Course, CustomCourseAdmin)
