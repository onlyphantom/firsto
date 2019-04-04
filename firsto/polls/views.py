# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def abcview(request):
    return HttpResponse("This is a secondary view.")
