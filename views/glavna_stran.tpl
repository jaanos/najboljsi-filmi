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
    % if get('prijavljen', False):
    <li>
        <a href="dodaj_film/">Dodaj film</a>
    </li>
    <li>
        <a href="odjava/">Odjavi se</a>
    </li>
    % end
</ul>

% if not get('prijavljen', False):
<form action="prijava/" method="post">
<input type="text" name="uporabnisko_ime" value="" />
<input type="password" name="geslo" value="" />
<input type="submit" value="Prijavi se">
</form>
<form action="registracija/" method="post">
<input type="text" name="uporabnisko_ime" value="" />
<input type="password" name="geslo" value="" />
<input type="submit" value="Registriraj se">
</form>
% end
