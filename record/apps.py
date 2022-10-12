from django.apps import AppConfig


class RecordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'record'

class CourseStudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CourseStudent'
