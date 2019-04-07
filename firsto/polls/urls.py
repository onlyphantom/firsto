from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # eg: /polls/
    path('', views.IndexView.as_view(), name='index'),
    # eg: /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]


# urlpatterns = [
#     # eg: /polls/
#     path('', views.index, name='polls-index'),
#     # eg: /polls/5/
#     # invoke: detail(<HttpRequest>, question_id)
#     # angle brackets "< >" captures and send as kw argument
#     path('<int:question_id>/', views.detail, name='polls-detail'),
#     # eg: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='polls-results'),
#     path('<int:question_id>/vote/', views.vote, name='polls-vote'),
# ]
