# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS

class Lecture(models.Model):
    title = models.TextField(blank=True, null=True)
    speaker = models.TextField(blank=True, null=True)
    time = models.DateTimeField(null=False)
    place = models.TextField(blank=True, null=True)
    university = models.TextField(blank=True, null=True)
    update_time = models.DateField(null=False)
    link = models.TextField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'lecture'

    def __unicode__(self):
        return unicode(self.title)


class LectureForm(ModelForm):
    class Meta:
        model = Lecture
        # fields = ['title', 'speaker', 'time', 'place', 'university', 'update_time', 'link']
        fields = '__all__'
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }