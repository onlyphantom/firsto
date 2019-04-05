from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # eg: /polls/
    path('', views.index, name='polls-index'),
    # eg: /polls/5/
    # invoke: detail(<HttpRequest>, question_id)
    # angle brackets "< >" captures and send as kw argument
    path('<int:question_id>/', views.detail, name='polls-detail'),
    # eg: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='polls-results'),
    # eg: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='polls-vote'),
]
