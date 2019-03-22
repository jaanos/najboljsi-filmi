from django.shortcuts import reverse, render, get_object_or_404, HttpResponseRedirect
from filmiapp.models import Film, FilmForm
from django.contrib.auth.decorators import login_required

def index(request):
    top = Film.objects.all().order_by('-ocena')[:10 ]
    return render(request, 'index.html', {
        'title': 'Top 10 all time',
        'top': top,
    })


def film(request, id):
    f = get_object_or_404(Film, pk=id)
    osebe = {}
    for n in f.nastopanja.all():
        if n.oseba in osebe:
            osebe[n.oseba].append(n.vloga)
        else:
            osebe[n.oseba] = [n.vloga]

    return render(request, 'film.html', {
        'title': f.naslov,
        'film': f,
        'osebe': osebe,
    })

@login_required
def nov_film(request):
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            film = form.save()
            return HttpResponseRedirect(reverse('film', args=(film.pk,)))
    else:
        form = FilmForm()

    return render(request, 'nov-film.html', {
        'title': 'Nov film',
        'form': form,
    })