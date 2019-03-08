from django.shortcuts import render, get_object_or_404
from filmiapp.models import Film

def index(request):
    top = Film.objects.all().order_by('-ocena')[:10 ]
    return render(request, 'index.html', {
        'title': 'Top 10 all time',
        'top': top,
    })


def film(request, id):
    f = get_object_or_404(Film, pk=id)
    return render(request, 'film.html', {
        'title': f.naslov,
        'film': f,
    })
