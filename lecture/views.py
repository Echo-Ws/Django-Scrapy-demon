from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Lecture

# Create your views here.


def index(request):
    return render(request, 'lecture/index.html')


def content(request):
    o = request.GET.get('o')

    q = request.GET.get('q')
    if q:
        try:
            contact_list = Lecture.objects.filter(title__icontains=q)
        except Lecture.DoesNotExist:
            return render(request, 'lecture/index.html')
    else:
        contact_list = Lecture.objects

    contact_list = contact_list.order_by(o)
    paginator = Paginator(contact_list, 30)
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

    return render(request, 'lecture/content.html', {
        'lecture_list': contacts,
    })