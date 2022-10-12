from django.contrib import admin

from .models import CourseStudent, Record
# Register your models here.
admin.site.register(Record)
admin.site.register(CourseStudent)
