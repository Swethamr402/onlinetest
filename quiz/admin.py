# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models

# Register your models here.

class QuizAdmin(admin.ModelAdmin):
    list_display      = ('quiz_name', 'questions_count')

    def questions_count(self, obj):
        return obj.questions.count()

class ResponseInline(admin.TabularInline):
    model       = models.Response
    extra       = 4
    fields      = ['response_text', 'is_correct_response']

# admin.site.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    save_on_top     = True
    fields          = ('question_text', 'question_type', 'image', 'is_active')
    inlines         = [ResponseInline]

class QuizHeaderAdmin(admin.ModelAdmin):
    list_display    = ('title', 'start_date', 'end_date', 'duration', 'completed_on', 'completed_in_secs','mark','user', 'quiz', 'is_timedout')

class QuizHeaderDetailAdmin(admin.ModelAdmin):
    list_display    = ('user_name', 'full_name', 'quiz_header', 'question', 'response', 'is_correct_answer', 'is_skipped', 'position')
    search_fields   = ('quiz_header__user__username',)

    def user_name(self, obj):
        return obj.quiz_header.user.username

    def full_name(self, obj):
        return '%s %s' % (obj.quiz_header.user.first_name, obj.quiz_header.user.last_name)

    def is_correct_answer(self, obj):
        if obj.response:
            return obj.response.is_correct_response
        return "Not yet answered"


admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.QuizHeader, QuizHeaderAdmin)
admin.site.register(models.QuizHeaderDetail, QuizHeaderDetailAdmin)
