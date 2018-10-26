# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from core import models as core_models

# Create your models here.

QUESTION_TYPES = (
    ('MULTI_SELECT', 'Multi Select'),
    ('MULTI_CHOICE', 'Multi Choice')
)

class Quiz(models.Model):
    """
    It is a quiz model
    """

    quiz_name       = models.CharField(max_length=50)
    description     = models.TextField(max_length=2000)
    duration        = models.IntegerField(null=False, blank=False)
    questions       = models.ManyToManyField('Question')

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizs'

    def __str__(self):

        return self.quiz_name

class Question(models.Model):
    """
    It is a question model which questions can be stored.
    """

    question_text       = models.TextField(max_length=2000,default='')
    question_type       = models.CharField(max_length=50, choices=QUESTION_TYPES)
    is_active           = models.BooleanField(default=True)
    image               = models.ImageField(upload_to='quiz/images', null=True, blank=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):

        return self.question_text

class Response(models.Model):
    """
    """

    question            = models.ForeignKey('Question', related_name = 'response_question', null=True, blank=True)
    response_text       = models.TextField(max_length=200)
    is_correct_response = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Response'
        verbose_name_plural = 'Responses'

    def __str__(self):

        return self.response_text

class QuizHeader(models.Model):
    """
    """

    title               = models.CharField(max_length=255)
    start_date          = models.DateTimeField()
    end_date            = models.DateTimeField()
    duration            = models.IntegerField()
    completed_on        = models.DateTimeField(null=True, blank=True)
    user                = models.ForeignKey(core_models.UserProfile, related_name = 'quizheader_user')
    quiz                = models.ForeignKey('Quiz', related_name = 'quizheader_quiz')
    is_timedout         = models.BooleanField(default=False)
    mark                = models.IntegerField(default=0)
    completed_in_secs   = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'QuizHeader'
        verbose_name_plural = 'QuizHeaders'

    def __str__(self):

        return self.title

class QuizHeaderDetail(models.Model):
    """
    """

    quiz_header         = models.ForeignKey('QuizHeader', related_name = 'quizheaderdetail_quizheader')
    question            = models.ForeignKey('Question', related_name = 'quizheaderdetail_question')
    response            = models.ForeignKey('Response', related_name = 'quizheaderdetail_response', null=True, blank=True)
    is_answered         = models.BooleanField(default=False)
    is_skipped          = models.BooleanField(default=False)
    position            = models.IntegerField()

    class Meta:
        verbose_name = 'QuizHeaderDetail'
        verbose_name_plural = 'QuizHeaderDetails'

    def __str__(self):

        return self.question.question_text
