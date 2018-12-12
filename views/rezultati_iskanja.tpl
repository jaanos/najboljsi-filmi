% rebase('osnova')

Iskanje niza '{{ niz }}' je obrodilo naslednje sadove:

<ul>
% for (id, naslov, leto, url) in filmi:
    <li><a href="{{ url }}">{{ naslov }} ({{ leto }})</a></li>
% end
</ul>
