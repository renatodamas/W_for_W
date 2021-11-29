
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from wfm.base.models import Depoimento


def home(request):
    depoimentos = Depoimento.objects.select_related('usuario')
    return render(request, 'base/index.html', context={'depoimentos': depoimentos})


def testimonials(request):
    depoimentos = Depoimento.objects.select_related('usuario')
    return render(request, 'base/testimonials.html', context={'depoimentos': depoimentos})
