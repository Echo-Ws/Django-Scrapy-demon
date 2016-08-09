from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Lecture

# Create your views here.


def page(contact_list, request):
    paginator = Paginator(contact_list, 5)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
        print contacts
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return contacts


def upTime(request):
    page = request.GET.get('page')



    return render(request, 'lecture/index.html', {
        'lecture_list': page(Lecture.objects.order_by("time"), request),
        'messageT': "downT/",
    })


def downTime(request):
    return render(request, 'lecture/index.html', {
        'lecture_list': page(Lecture.objects.order_by("-time"), request),
        'messageT': "upT/",
    })


def upU(request):
    return render(request, 'lecture/index.html', {
        'lecture_list': page(Lecture.objects.order_by("update_time"), request),
        'messageU': "downU/",
    })


def downU(request):
    return render(request, 'lecture/index.html', {
        'lecture_list': page(Lecture.objects.order_by("-update_time"), request),
        'messageU': "upU/",
    })