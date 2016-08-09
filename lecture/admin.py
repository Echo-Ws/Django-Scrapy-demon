from django.contrib import admin

from .models import Lecture


class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'time', 'place', 'university', 'update_time', 'link')
    list_filter = ['update_time']
    search_fields = ['title']

admin.site.register(Lecture, LectureAdmin)

