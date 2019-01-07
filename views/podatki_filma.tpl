% rebase('osnova')

<h1>{{ naslov }} <small>({{ leto }})</small></h1>
<p>
dolžina: {{dolzina}} min<br />
ocena: {{ocena}}/10<br />
žanri: {{', '.join(zanri)}}<br />
% if len(reziserji) == 1:
    režiser: {{reziserji[0][1]}}<br />
% elif len(reziserji) > 1:
    režiserji: {{', '.join(x for _, x in reziserji)}}<br />
% end
% if len(igralci) == 1:
    igra: {{igralci[0][1]}}<br />
% elif len(reziserji) > 1:
    igrajo: {{', '.join(x for _, x in igralci)}}<br />
% end
