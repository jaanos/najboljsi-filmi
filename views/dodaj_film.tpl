% rebase('osnova')

% if napaka:
<p>Prišlo je do napake!</p>
% end

<form method="post">
Naslov: <input type="text" name="naslov" value="{{naslov}}" /><br />
Dolžina: <input type="text" name="dolzina" value="{{dolzina}}" /><br />
Leto: <input type="text" name="leto" value="{{leto}}" /><br />
Ocena: <input type="text" name="ocena" value="{{ocena}}" /><br />
Metascore: <input type="text" name="metascore" value="{{metascore}}" /><br />
Glasovi: <input type="text" name="glasovi"  value="{{glasovi}}" /><br />
Zaslužek: <input type="text" name="zasluzek" value="{{zasluzek}}" /><br />
Opis: <textarea name="opis">{{opis}}</textarea><br />

Žanri: <select multiple name="zanri">
% for id, naziv in vsi_zanri:
    <option value="{{id}}" {{'selected' if str(id) in zanri else ''}}>{{naziv}}</option>
% end
</select>
<br />

Igralci: <select multiple name="igralci">
% for id, ime in vse_osebe:
    <option value="{{id}}" {{'selected' if str(id) in igralci else ''}}>{{ime}}</option>
% end
</select>
<br />

Režiserji: <select multiple name="reziserji">
% for id, ime in vse_osebe:
    <option value="{{id}}" {{'selected' if str(id) in reziserji else ''}}>{{ime}}</option>
% end
</select>
<br />

<input type="submit" value="Dodaj film">
</form>
