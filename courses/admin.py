from django.contrib import admin
from .models import Course, CourseInstructor, Instructor, CourseUser, Bug
from django.http import HttpResponse
import csv
# Register your models here.

def export_comments(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="hsmp_comments.csv"'
    writer = csv.writer(response)
    writer.writerow(["pk", "user", "course", "instructor", "semester", "topic", "text", "rating_instr", "rating_course", "date"])
    for q in queryset:
        if q.take == "taken":
            tmp_row = [q.pk, q.user, q.course, q.instructor, q.course_instructor.semester,
                       q.course_instructor.topic, q.text, q.rating_instructor, q.rating_course, q.date]
            writer.writerow(tmp_row)
    return response
export_comments.short_description = 'Export to text'

class CourseUserRelationInline(admin.TabularInline):
    model = Course.users.through

class CourseInstructorRelationInline(admin.TabularInline):
    model = Course.instructors.through

class CustomCourseAdmin(admin.ModelAdmin):
    inlines = (CourseInstructorRelationInline,) #CourseUserRelationInline,
    list_display = ['get_courseNum','type','units', 'title', 'last_taught']
    list_filter = ('type','mnemonic', 'units', 'last_taught')
    search_fields = ["mnemonic", "number", "title"]

    def get_courseNum(self, instance):
        return instance.mnemonic + instance.number
    get_courseNum.short_description = 'Course Number'

class CustomCourseInstructorAdmin(admin.ModelAdmin):
    list_display = ['course','instructor','semester', 'topic']
    list_filter = ('semester',)
    search_fields = ["course__mnemonic","course__number","course__title",]
    autocomplete_fields = ['course','instructor',]

class CustomCourseUserAdmin(admin.ModelAdmin):
    list_display = ['course','user', 'instructor','take', 'text', 'date']
    list_filter = ('take',)
    actions = [export_comments]

class CustomInstructorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'last_taught']
    list_filter = ('last_taught',)
    search_fields = ['first_name','last_name']

class BugAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created']


admin.site.register(Bug, BugAdmin)
admin.site.register(CourseInstructor, CustomCourseInstructorAdmin)
admin.site.register(Instructor, CustomInstructorAdmin)
admin.site.register(Course, CustomCourseAdmin)
admin.site.register(CourseUser, CustomCourseUserAdmin)
