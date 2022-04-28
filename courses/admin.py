from django.contrib import admin
from .models import Course,Comment,Topic, Episode,Section

# Register your models here.
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Topic)
admin.site.register(Episode)
admin.site.register(Section)


