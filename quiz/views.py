# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Min
from django.db.models import Max
from datetime import datetime
from datetime import timedelta
from pytz import timezone
import random
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect

from . import models as quiz_models
from core import models as core_models
from . import admin as admin_models
from . models import QuizHeader
from . models import QuizHeaderDetail
# from django.db.models import Count
from django.db.models import Count, Case, When
from datetime import datetime

# Create your views here.

@login_required
def list_questions(request):
    questions = quiz_models.Question.objects.all()
    return render(request, 'quiz/list_questions.html', {
    'questions': questions
    })

@login_required
def home(request):
    return render(request, 'quiz/home.html', {
    'user': request.user
    })




@login_required
def checkloginValid(request):
    #set the date and time format
    date_format = "%m-%d-%Y %H:%M:%S"

    #convert string to actual date and time
    time1  = datetime.strptime('10-23-2018 10:00:00', date_format)
    time2  = datetime.strptime('10-24-2018 20:00:00', date_format)

    #find the difference between two dates
    diff = time2 - time1


    ''' days and overall hours between two dates '''
    # print ('Days & Overall hours from the above two dates')
    #print days
    days = diff.days
    # print (str(days) + ' day(s)')

    #print overall hours
    days_to_hours = days * 24
    diff_btw_two_times = (diff.seconds) / 3600
    overall_hours = days_to_hours + diff_btw_two_times
    # print (str(overall_hours) + ' hours');



    ''' now print only the time difference '''
    ''' between two times (date is ignored) '''

    # print ('\nTime difference between two times (date is not considered)')

    #like days there is no hours in python
    #but it has seconds, finding hours from seconds is easy
    #just divide it by 3600

    hours = (diff.seconds) / 3600
    print (str(hours) + ' Hours')


    #same for minutes just divide the seconds by 60

    minutes = (diff.seconds) / 60
    # print (str(minutes) + ' Minutes')

    #to print seconds, you know already ;)

    # print (str(diff.seconds) + ' secs')

    if(datetime.now() < time2) and (datetime.now() > time1):
        return True
    else:
        return False


@login_required
def finishquiz(request):
    return render(request, 'quiz/finishquiz.html')


@login_required
def start_quiz(request, quiz_id):
    isTime = checkloginValid(request)
    print("istime=" +str(isTime))
    if(isTime == True):
        quiz = quiz_models.Quiz.objects.get(pk=quiz_id)
        return render(request, 'quiz/start_quiz.html', {
        'quiz': quiz,
        'user': request.user
        })
    else:
        return render(request,'quiz/logintimeup.html')

@login_required
def view_toppers_results(request):
    print("startd toppers")
    quiz_id =1
    headers = quiz_models.QuizHeader.objects.filter(quiz__id = quiz_id)
    for header in headers:
        mark = quiz_models.QuizHeaderDetail.objects.filter(quiz_header = header, response__is_correct_response = True).count()
        header.mark = mark
        completed_in_secs = None
        if header.start_date and header.completed_on:
            completed_in_secs = (header.completed_on - header.start_date).total_seconds()
        if completed_in_secs:
            header.completed_in_secs = completed_in_secs
            header.save()

    top_headers = headers.order_by('-mark', 'completed_in_secs').all()[:50]

    # Calculating the registerd users count
    registered_users_count = core_models.UserProfile.objects.filter(is_superuser=False).count()

    # Calculating the participants count
    participants_count = headers.count()

    return render(request, 'core/dashboard.html', {
    'toppers' : list(top_headers),
    'registered_users_count': registered_users_count,
    'participants_count': participants_count
    })


@login_required
def view_individual_results(request, header_id):
        header = quiz_models.QuizHeader.objects.get(pk=header_id)
        header_details = quiz_models.QuizHeaderDetail.objects.filter(quiz_header = header)
        total_count = header_details.count()
        answered_count = header_details.filter(is_answered=True).count()
        correct_answer_count = header_details.filter(response__is_correct_response = True).count()
        wrong_answer_count = header_details.filter(response__is_correct_response = False).count()

        return render(request, 'quiz/individual_result.html', {
        'header': header,
        'header_details': header_details,
        'total_count': total_count,
        'answered_count': answered_count,
        'correct_answer_count': correct_answer_count,
        'wrong_answer_count': wrong_answer_count
        })


@login_required
def quiz_live(request, quiz_id):
    quiz = quiz_models.Quiz.objects.get(pk=quiz_id)
    quizheader = quiz_models.QuizHeader.objects.filter(user=request.user, quiz=quiz).first()

    # if request.method == 'POST':
    # Working on existing header
    if quizheader:

        headerdetails = quiz_models.QuizHeaderDetail.objects.all()
        min_position = headerdetails.aggregate(Min('position'))['position__min']
        max_position = headerdetails.aggregate(Max('position'))['position__max']

        previous_position = -1
        current_position = -1
        next_position = -1
        position = 0

        if request.method == 'POST':
            position = int(request.POST.get('position'))
            response_id = request.POST.get('response_id')
            form_action = request.POST.get('form_action')

            if form_action == 'Next':

                detail = quiz_models.QuizHeaderDetail.objects.filter(quiz_header=quizheader, position=position).first()
                if detail.is_answered:
                    position += 1
                else:
                    if response_id:
                        response_id = int(response_id)
                        response = quiz_models.Response.objects.get(pk=response_id)
                        detail.response = response
                        detail.is_answered = True
                        detail.is_skipped = False
                        detail.save()
                        position += 1

            elif form_action == 'Previous':
                position -= 1

            elif form_action == 'Finish':
                detail = quiz_models.QuizHeaderDetail.objects.filter(quiz_header=quizheader, position=position).first()
                quizheader.completed_on = datetime.now()
                quizheader.save()
                if detail.is_answered:
                    return render(request, 'quiz/home.html')
                else:
                    if response_id:
                        response_id = int(response_id)
                        response = quiz_models.Response.objects.get(pk=response_id)
                        detail.response = response
                        detail.is_answered = True
                        detail.is_skipped = False
                        detail.save()

                    return render(request, 'quiz/thankupage.html')
                    # url = reverse('individual_result', args=(quizheader.id,))
                    # return HttpResponseRedirect(url)
                        #return render(request, 'quiz/thankupage.html')

        if position <= min_position:
            previous_position = -1
            current_position = position
            next_position = (position + 1)
        elif position >= max_position:
            previous_position = (position - 1)
            current_position = position
            next_position = -1
        else:
            previous_position = (position - 1)
            current_position = position
            next_position = (position + 1)

        first_header_detail = quiz_models.QuizHeaderDetail.objects.filter(quiz_header=quizheader, position=current_position).first()
        if first_header_detail:
            question = first_header_detail.question
            responses = quiz_models.Response.objects.filter(question=question)
        # print("quizheader.end_date" +str(quizheader.end_date))
        if quizheader.end_date:
            end_date= quizheader.end_date.astimezone(timezone('Asia/Kolkata'))
            end_time = end_date.strftime("%b %d, %Y %H:%M:%S")

        # print(end_time)
        # print(quizheader.end_date)
        if quizheader.completed_on:
            return render(request,'quiz/testcompleted.html')
        print("end_time" +str(end_time))
        return render(request, 'quiz/quiz_live.html', {
            'quiz': quiz,
            'answered_response': first_header_detail.response,
            'question': question,
            'responses': responses,
            'previous_position': previous_position,
            'current_position': current_position,
            'next_position': next_position,
            'end_time':end_time,
            'question_number': first_header_detail.position + 1
        })

    # else:
        # Invalid request
    else:
        # Working on new header
        if not quizheader:
            newheader = QuizHeader()
            newheader.title = quiz.quiz_name
            newheader.start_date = datetime.now()
            # local_tz = timezone('Asia/Kolkata')
            # end_date = local_tz.localize(datetime.now() + timedelta(minutes=quiz.duration), is_dst=None)
            # end_time = end_date.strftime("%b %d, %Y %H:%M:%S")

            # newheader.end_date = datetime.now() + timedelta(minutes=quiz.duration)
            newheader.end_date = datetime.now()  + timedelta(minutes=quiz.duration)
            newheader.duration = quiz.duration
            newheader.user = request.user
            newheader.quiz = quiz
            newheader.save()
            quizheader = newheader

            # Getting question ids
            questionids = []
            for q in quiz.questions.all():
                questionids.append(q.id)

            random.shuffle(questionids)

            # Insert header detail record for each questions with position
            position = 0
            question = None
            responses = None
            header_detail = None
            for qid in questionids:
                newheaderdetail = QuizHeaderDetail()
                newheaderdetail.quiz_header = quizheader
                newheaderdetail.question = quiz.questions.all().get(pk=qid)
                newheaderdetail.response = None
                newheaderdetail.is_answered = False
                newheaderdetail.is_skipped = False
                newheaderdetail.position = position
                newheaderdetail.save()

                if position == 0 and question is None:
                    header_detail = newheaderdetail
                    question = newheaderdetail.question
                    responses = quiz_models.Response.objects.filter(question=question)

                position += 1
            print("quizheader.end_date else" +str(quizheader.end_date))
            if quizheader.end_date:
                local_tz = timezone('Asia/Kolkata')
                end_date = local_tz.localize(quizheader.end_date, is_dst=None)
                end_time = end_date.strftime("%b %d, %Y %H:%M:%S")

            if quizheader.completed_on:
                return render(request,'quiz/testcompleted.html')

            return render(request, 'quiz/quiz_live.html', {
                'quiz': quiz,
                'question': question,
                'responses': responses,
                'previous_position': None,
                'current_position': 0,
                'next_position': 1,
                'end_time':end_time,
                'question_number': header_detail.position + 1
            })

    return render(request, 'quiz/quiz_live.html', {
    'quiz': None,
    'question': None,
    'responses': None
    })
