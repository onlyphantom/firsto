# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F
from .models import Choice, Question


class IndexView(generic.ListView):
    # default: <app name>/<modelname>_list.html -> polls/question_list.html
    template_name = 'polls/index.html'
    # default: 'question_list'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        """Return the last 5 published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    # default: <app name>/<modelname>_detail.html -> polls/question_detail.html
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Exclude questions that aren't published yet/
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def index(request):
#     latest_questions = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_questions': latest_questions}
#     return render(request, 'polls/index.html', context)


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html',
#                   {'question': question, 'elems': ['a', 'b', 'd']})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # selected_choice.votes += 1
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        selected_choice.refresh_from_db()
        # Return HttpResponseRedirect after POST preventing data from posted
        # twice if user hits the Back button
        return HttpResponseRedirect(reverse('polls:results',
                                    args=(question.id,)
        ))
