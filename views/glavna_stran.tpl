% rebase('osnova')

<h1 class="title">Pozdravljeni na strani filmov. Na voljo vam je:</h1>

<form action="iskanje/" method="get">
<input type="text" name="naslov" value="" />
<input type="submit" value="Išči">
</form>

<ul>
% for desetletje, url in desetletja:
    <li>
        <a href="{{ url }}">
            Najboljši filmi desetletja {{ desetletje }}–{{ desetletje + 9}}
        </a>
    </li>
% end
</ul>

<p>
<a href="dodaj_film/">Dodaj film</a>
</p>
